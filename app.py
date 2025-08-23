import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

load_dotenv()

DB_CONFIG = {
"dbname": os.getenv("PGDATABASE"),
"user": os.getenv("PGUSER"),
"password": os.getenv("PGPASSWORD"),
"host": os.getenv("PGHOST"),
"port": int(os.getenv("PGPORT"))
}

def filter_products(min_calories=None, max_calories=None,
                    min_protein=None, max_protein=None, min_sugar=None, max_sugar=None,
                    min_fat=None, max_fat=None, min_salt=None, max_salt=None, 
                    min_fiber=None, max_fiber=None, category=None, country=None):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    query = "SELECT product_name, brand, category, calories, fat, sugar, protein, \
    image_url, salt, fiber, country, insights FROM foods WHERE TRUE"
    params = []

    if category:
        query += " AND category = %s"
        params.append(category)
    if country:
        query += " AND country = %s"
        params.append(country)
    if min_calories is not None:
        query += " AND calories >= %s"
        params.append(min_calories)
    if max_calories is not None:
        query += " AND calories <= %s"
        params.append(max_calories)
    if min_protein is not None:
        query += " AND protein >= %s"
        params.append(min_protein)
    if max_protein is not None:
        query += " AND protein <= %s"
        params.append(max_protein)
    if min_sugar is not None:
        query += " AND sugar >= %s"
        params.append(min_sugar)
    if max_sugar is not None:
        query += " AND sugar <= %s"
        params.append(max_sugar)
    if min_fat is not None:
        query += " AND fat >= %s"
        params.append(min_fat)
    if max_fat is not None:
        query += " AND fat <= %s"
        params.append(max_fat)
    if min_salt is not None:
        query += " AND salt >= %s"
        params.append(min_salt)
    if max_salt is not None:
        query += " AND salt <= %s"
        params.append(max_salt)
    if min_fiber is not None:
        query += " AND fiber >= %s"
        params.append(min_fiber)
    if max_fiber is not None:
        query += " AND fiber <= %s"
        params.append(max_fiber)

    query += " ORDER BY RANDOM() LIMIT 200;"
    cur.execute(query, params)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

@app.route("/", methods=["GET", "POST"])
def index():
    products = []
    categories = ["snacks", "beverages", "meats", "desserts", "meals", "dairies", "canned foods", 
                  "breads", "fats", "fruits and vegetables based foods", "cereals and their products",
                  "nuts and their products"] 
    countries = ["canada","france","united states","united kingdom","ireland","australia","norway","sweden","mauritius"]

    if request.method == "POST":
        category = request.form.get("category")
        country = request.form.get("country")
        min_calories = request.form.get("min_calories", type=float)
        max_calories = request.form.get("max_calories", type=float)
        min_protein = request.form.get("min_protein", type=float)
        max_protein = request.form.get("max_protein", type=float)
        min_sugar = request.form.get("min_sugar", type=float)
        max_sugar = request.form.get("max_sugar", type=float)
        min_fat = request.form.get("min_fat", type=float)
        max_fat = request.form.get("max_fat", type=float)
        min_salt = request.form.get("min_salt", type=float)
        max_salt = request.form.get("max_salt", type=float)
        min_fiber = request.form.get("min_fiber", type=float)
        max_fiber = request.form.get("max_fiber", type=float)


        products = filter_products(
            min_calories=min_calories,
            max_calories=max_calories,
            min_protein=min_protein,
            max_protein=max_protein,
            min_sugar=min_sugar,
            max_sugar=max_sugar,
            min_fat=min_fat,
            max_fat=max_fat,
            min_salt=min_salt,
            max_salt=max_salt,
            min_fiber=min_fiber,
            max_fiber=max_fiber,
            category=category,
            country=country
        )

    return render_template("index.html", products=products, categories=categories, countries=countries)

if __name__ == "__main__":
    app.run(debug=True)
