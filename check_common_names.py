import json

with open('monash_full_export.json', 'r', encoding='utf-8') as f:
    en_data = json.load(f)

with open('monash_full_export_cz.json', 'r', encoding='utf-8') as f:
    cz_data = json.load(f)

en_dict = {item['food_id']: item for item in en_data}
cz_dict = {item['food_id']: item for item in cz_data}

common_ids = set(en_dict.keys()) & set(cz_dict.keys())

print("Kontrola mezinárodních názvů (Gin, Vodka, atd.) v CZ verzi:\n")

test_items = ['Gin', 'Vodka', 'Falafel', 'Marshmallow', 'Hummus', 'Sushi', 'Pizza', 'Pasta', 'Cappuccino', 'Espresso']

for food_id in sorted(common_ids):
    en_name = en_dict[food_id]['name']
    cz_name = cz_dict[food_id]['name']
    
    # Check if any test item is in the English name
    for test_item in test_items:
        if test_item.lower() in en_name.lower():
            print(f"ID: {food_id}")
            print(f"  EN: {en_name}")
            print(f"  CZ: {cz_name}")
            print()
