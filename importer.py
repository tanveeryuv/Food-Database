import time
import math
import requests
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import os
from nlp_insights import generate_insight


load_dotenv()


DB_CONFIG = {
"dbname": os.getenv("PGDATABASE"),
"user": os.getenv("PGUSER"),
"password": os.getenv("PGPASSWORD"),
"host": os.getenv("PGHOST"),
"port": int(os.getenv("PGPORT")),
}

SEARCH_URL = "https://world.openfoodfacts.org/cgi/search.pl"
PAGE_SIZE_DEFAULT = 100


SCHEMA_SQL = open("schema.sql", "r", encoding="utf-8").read()




def init_db():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(SCHEMA_SQL)
    conn.commit()
    cur.close()
    conn.close()




def fetch_page(categories=None, countries=None, page=1, page_size=PAGE_SIZE_DEFAULT):
    params = {
        "action": "process",
        "json": 1,
        "sort_by": "unique_scans_n",
        "page": page,
        "page_size": page_size,
    }
    # Add multiple categories
    for i, cat in enumerate(categories):
        params[f"tagtype_{i}"] = "categories"
        params[f"tag_contains_{i}"] = "contains"
        params[f"tag_{i}"] = cat

    # Add multiple countries
    offset = len(categories)
    for j, country in enumerate(countries):
        params[f"tagtype_{offset+j}"] = "countries"
        params[f"tag_contains_{offset+j}"] = "contains"
        params[f"tag_{offset+j}"] = country
        
    retries = 3
    for attempt in range(retries):
        try:
            r = requests.get(SEARCH_URL, params, timeout=60)
            r.raise_for_status()
            data = r.json()
            print(f"Found {len(data.get('products', []))} products")
            for p in data.get("products", []):
                print(p.get("product_name"))
            return data
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(5)  # wait 5 seconds before retry
    raise Exception("Failed to fetch data after 3 attempts")
    
UPSERT_SQL = """
INSERT INTO foods (
barcode, product_name, brand, category, calories, fat, sugar, protein,
salt, fiber, nutriscore_grade, ecoscore_grade, ingredients, country, image_url, insights
) VALUES %s
ON CONFLICT (barcode) DO UPDATE SET
product_name = EXCLUDED.product_name,
brand = EXCLUDED.brand,
category = EXCLUDED.category,
calories = EXCLUDED.calories,
fat = EXCLUDED.fat,
sugar = EXCLUDED.sugar,
protein = EXCLUDED.protein,
salt = EXCLUDED.salt,
fiber = EXCLUDED.fiber,
nutriscore_grade = EXCLUDED.nutriscore_grade,
ecoscore_grade = EXCLUDED.ecoscore_grade,
ingredients = EXCLUDED.ingredients,
country = EXCLUDED.country,
image_url = EXCLUDED.image_url,
insights = EXCLUDED.insights,
imported_at = CURRENT_TIMESTAMP
"""
def import_products(categories=None, countries=None, max_pages=5, page_size=PAGE_SIZE_DEFAULT):
    print(f"Importing categories={categories!r}, countries={countries!r}")
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    total = 0
    for category in categories:
        for country in countries:
            print(f"\n📦 Importing category='{category}' country='{country}'")

            for page in range(1, max_pages + 1):
                try:
                    data = fetch_page([category], [country], page=page, page_size=page_size)
                except Exception as e:
                    print(f"❌ Failed page {page}: {e}")
                    break

                products = data.get("products", [])
                if not products:
                    print("⚠️ No more products.")
                    break
                rows = []
                for p in products:
                    insights = generate_insight(p, category)
                    rows.append((
                        p.get("code"),
                        p.get("product_name"),
                        ", ".join(p.get("brands", "").split(",")) if p.get("brands") else None,
                        category,
                        p.get("nutriments", {}).get("energy-kcal_100g"),
                        p.get("nutriments", {}).get("fat_100g"),
                        p.get("nutriments", {}).get("sugars_100g"),
                        p.get("nutriments", {}).get("proteins_100g"),
                        p.get("nutriments", {}).get("salt_100g"),
                        p.get("nutriments", {}).get("fiber_100g"),
                        p.get("nutriscore_grade"),
                        p.get("ecoscore_grade"),
                        p.get("ingredients_text"),
                        country,
                        p.get("image_url"),
                        insights
                    ))

                execute_values(cur, UPSERT_SQL, rows)
                conn.commit()
                total += len(rows)
                print(f"✅ Page {page}: {len(rows)} products imported.")

    cur.close()
    conn.close()
    print(f"\nDone. Total imported: {total}")

if __name__ == "__main__":
    init_db()
    categories = os.getenv("OFF_CATEGORIES", "chocolate,snacks").split(",")
    countries = os.getenv("OFF_COUNTRIES", "canada,united-states").split(",")

    import_products(categories, countries, max_pages=int(os.getenv("OFF_MAX_PAGES", 5)), 
                    page_size=int(os.getenv("OFF_PAGE_SIZE", PAGE_SIZE_DEFAULT)))
    