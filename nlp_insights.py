import os
from transformers import pipeline

# Load locally (downloads once, then cached in ~/.cache/huggingface)
generator = pipeline("text2text-generation", model="google/flan-t5-large")

def generate_insight(p, category):
    # Build a structured description
    description = (
        f"Food product: {p.get('product_name')}\n"
        f"Category: {category}\n"
        f"Calories: {p.get('nutriments', {}).get('energy-kcal_100g')} kcal\n"
        f"Sugar: {p.get('nutriments', {}).get('sugars_100g')} g\n"
        f"Proteins: {p.get('nutriments', {}).get('proteins_100g')} g\n"
        f"Fat: {p.get('nutriments', {}).get('fat_100g')} g\n"
        f"Salt: {p.get('nutriments', {}).get('salt_100g')} g\n"
        f"Fiber: {p.get('nutriments', {}).get('fiber_100g')} g\n"
        f"Nutriscore Grade: {p.get('nutriscore_grade'),}\n"
        f"Ecoscore Grade {p.get('ecoscore_grade')}\n"
        f"Ingredients{p.get('ingredients_text')} \n"
    )

    # Prompt for summarization / analysis
    prompt = (
        f"Please answer the following question and give the reasoning for your answer in less than 50 words:\n"
        f"Is the following food healthy or unhealthy?:\n\n"
        f"{description}\n"
    )

    result = generator(prompt, max_new_tokens=100, do_sample=False)
    print(result[0]["generated_text"])
    return result[0]["generated_text"]
