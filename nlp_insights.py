import os
from transformers import pipeline

generator = pipeline("text2text-generation", model="google/flan-t5-large")

def generate_insight(p, category):
    description = (
        f"The food has {p.get('nutriments', {}).get('energy-kcal_100g')} calories. "
        f"It has {p.get('nutriments', {}).get('sugars_100g')} grams of sugar. "
        f"It has {p.get('nutriments', {}).get('proteins_100g')} grams of protein. "
        f"It has {p.get('nutriments', {}).get('fat_100g')} grams of fat. "
        f"It has: {p.get('nutriments', {}).get('salt_100g')} grams of salt. "
        f"It has: {p.get('nutriments', {}).get('fiber_100g')} grams of fiber. "
        f"Its ingredients are {p.get('ingredients_text')}."
    )

    prompt = "Determine if this food is healthy or unhealthy based on its nutritional information. "
    prompt += description

    result = generator(prompt, max_length = 20)
    print(result[0]["generated_text"])
    return result[0]["generated_text"]
