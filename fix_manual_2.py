import json

path_cz = 'c:/Users/Fany/Desktop/FODMAP/monash_full_export_cz.json'
with open(path_cz, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Seznam oprav pro nejhorší doslovné překlady
manual_mapping = {
    "Zlato, avokádo": "Avokádový olej",
    "Olej, avokádo": "Avokádový olej",
    "Cukr, palma": "Palmový cukr",
    "Cukr, syrové": "Surový (přírodní) cukr",
    "Cukr, kámen (třtina)": "Kandysový cukr (třtinový)",
    "Bylinky, bazalkový, thajský, čerstvý": "Thajská bazalka, čerstvá",
    "Bylinky, bazalkový, čerstvý": "Bazalka, čerstvá",
    "Bylinky, petrželový, čerstvý": "Petrželka, čerstvá",
    "Bylinky, tymiánový, čerstvý": "Tymián, čerstvý",
    "Bylinky, rozmarýnový, čerstvý": "Rozmarýn, čerstvý",
    "Bylinky, šalvějový, čerstvý": "Šalvěj, čerstvá",
    "Bylinky, mátový, čerstvý": "Máta, čerstvá",
    "Bylinky, koprový, čerstvý": "Kopr, čerstvý",
    "Bylinky, oregano, čerstvé": "Oregáno, čerstvé",
    "Bylinky, estragon, čerstvý": "Estragon, čerstvý",
    "Olej, oliva, česnek infuze": "Olivový olej s česnekem",
    "Tequila, stříbro": "Tequila (stříbrná)",
    "Tequila, zlatá": "Tequila (zlatá)",
    "Whiskey / Bourbon / Skotská": "Whisky / Bourbon",
    "Víno, lepkavé": "Dezertní víno",
    "Šťáva, citron, čerstvě vymačkaná": "Citronová šťáva, čerstvá",
    "Šťáva, limetka, čerstvá": "Limetková šťáva, čerstvá",
    "Šťáva, pomeranč, čerstvě vymačkaná": "Pomerančová šťáva, čerstvá",
    "Sýr, Monterey Jacku": "Sýr Monterey Jack",
    "Sýr, Chaloupka": "Sýr Cottage",
    "Sýr, chaloupka": "Sýr Cottage"
}

for item in data:
    name = item.get("name", "")
    for bad, good in manual_mapping.items():
        if bad in name:
            name = name.replace(bad, good)
    
    # Oprava kategorie pro bylinky
    if "Herb," in name:
         name = name.replace("Herb,", "Bylinka,")
    
    item["name"] = name

with open(path_cz, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
