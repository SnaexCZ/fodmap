import json

path_cz = 'c:/Users/Fany/Desktop/FODMAP/monash_full_export_cz.json'
with open(path_cz, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Dictionary for mapping structural components
# Form: "Category, Ingredient" -> "Adjective Noun"
# Example: "Otruby, rýže" -> "Rýžové otruby"

replacements = {
    # Otruby
    "Otruby, rýže, nezpracované, nevařené": "Rýžové otruby, syrové",
    "Otruby, pšenice, zpracované, tepelně neupravené": "Pšeničné otruby, zpracované",
    
    # Mouka
    "Mouka, pšenice": "Pšeničná mouka",
    "Mouka, žito": "Žitná mouka",
    "Mouka, rýže": "Rýžová mouka",
    "Mouka, rýže, hnědá": "Rýžová mouka (hnědá rýže)",
    "Mouka, oves": "Ovesná mouka",
    "Mouka, pohanka": "Pohanková mouka",
    "Mouka, kokos": "Kokosová mouka",
    "Mouka, maniok": "Manioková mouka",
    "Mouka, kaštan": "Kaštanová mouka",
    "Mouka, ječmen": "Ječná mouka",
    "Mouka, čirok": "Čiroková mouka",
    "Mouka, sója": "Sójová mouka",
    "Mouka, amarant": "Amarantová mouka",
    "Mouka, lupina": "Lupinová mouka",
    "Mouka, teff": "Teffová mouka",
    
    # Mléko
    "Mléko, mandle": "Mandlové mléko",
    "Mléko, oves": "Ovesné mléko",
    "Mléko, rýže": "Rýžové mléko",
    "Mléko, sója (sójové boby)": "Sójové mléko (ze sójových bobů)",
    "Mléko, sója (sójový protein)": "Sójové mléko (ze sójového proteinu)",
    "Mléko, makadamové": "Makadamové mléko",
    "Mléko, kokos": "Kokosové mléko",
    
    # Jogurt
    "Jogurt, sója": "Sójový jogurt",
    "Jogurt, kokos": "Kokosový jogurt",
    "Jogurt, kozí": "Kozí jogurt",
    "Jogurt, řecký": "Řecký jogurt",
    
    # Sýr
    "Sýr, mozzarella": "Mozzarella",
    "Sýr, parmazán": "Parmezán",
    "Sýr, ricotta": "Ricotta",
    "Sýr, haloumi": "Halloumi",
    "Sýr, fetta": "Feta sýr",
    "Sýr, modrý": "Modrý sýr (Niva)",
    "Sýr, švýcarský": "Švýcarský sýr (Ementál)",
    
    # Chléb
    "Chléb, žito": "Žitný chléb",
    "Chléb, oves, kvásek": "Ovesný kváskový chléb",
    "Chléb, pšenice, bílá": "Pšeničný chléb, bílý",
    "Chléb, pšenice, celozrnné": "Pšeničný chléb, celozrnný",
    "Chléb, pšenice, smíšená zrna / vícezrnná": "Pšeničný chléb, vícezrnný",
    
    # Čaj a káva
    "Čaj, černý": "Černý čaj",
    "Čaj, zelený": "Zelený čaj",
    "Čaj, bílý": "Bílý čaj",
    "Čaj, heřmánek": "Heřmánkový čaj",
    "Čaj, máta": "Mátový čaj",
    "Čaj, pampeliška": "Pampeliškový čaj",
    "Čaj, fenykl": "Fenyklový čaj",
    "Káva, espresso": "Espresso káva",
    
    # Zelenina a ovoce, kde je Noun, noun
    "Zelí, červené": "Červené zelí",
    "Zelí, bílé / obyčejné": "Bílé zelí",
    "Zelí, savojové": "Hlávková kapusta",
    "Paprika, zelená": "Zelená paprika",
    "Paprika, červená": "Červená paprika",
    "Paprika, oranžová": "Oranžová paprika",
    "Paprika, žlutá": "Žlutá paprika",
    "Cibule, bílá": "Bílá cibule",
    "Cibule, španělská / červená": "Červená cibule",
    "Cibule, jarní / jarní cibulka": "Jarní cibulka",
    "Fazole, zelené": "Zelené fazole",
    "Meloun, hořký": "Hořký meloun",
    "Houby, enoki": "Enoki houby",
    "Houby, shiitake": "Shiitake houby",
    "Houby, hříbky": "Hříbky",
    
    # Chipsy / Sušenky
    "Chipsy, kukuřice, obyčejné": "Kukuřičné chipsy",
    "Chipsy, bramborové lupínky, obyčejné": "Bramborové chipsy",
    "Sušenka / sušenka, čokoláda": "Čokoládová sušenka",
    "Sušenka / sušenka, obyčejná": "Obyčejná sušenka",
    
    # Ostatní
    "Ocet, jablečný mošt": "Jablečný ocet",
    "Ocet, balsamico": "Balsamikový ocet",
    "Ocet, bílý": "Bílý ocet",
    "Ocet, červené víno": "Vinný ocet (červený)",
    "Víno, bílé": "Bílé víno",
    "Víno, červené": "Červené víno",
    "Víno, šumivé": "Šumivé víno",
    "Škrob, brambory": "Bramborový škrob",
    "Škrob, tapioka": "Tapiokový škrob",
    "Tofu (sojový tvaroh)": "Tofu",
    
    # Vločky
    "Vločky, rýže, nevařené": "Rýžové vločky, syrové",
    "Vločky, quinoa, tepelně neupravené": "Quinoové vločky, syrové",
    "Vločky, pohanka, vařené": "Pohankové vločky, vařené",
    
    # Ořechy
    "Mandle, loupané": "Mandle, loupané",
    "Oříšek, kešu": "Kešu ořechy",
    "Ořech, Brazílie": "Para ořechy",
    "Lískové ořechy, loupané": "Lískové ořechy",
    "Makadamové ořechy, vyloupané": "Makadamové ořechy",
    "Ořech, ořech, vyloupaný": "Vlašské ořechy, loupané",
    "Oříšek, pistácie": "Pistácie",
    "Piniové oříšky, vyloupané": "Piniové oříšky"
}

count = 0
for item in data:
    name = item.get("name", "")
    for bad, good in replacements.items():
        if bad in name:
            name = name.replace(bad, good)
            
    # Obecnější struktura
    # "Mouka, "
    if name.startswith("Mouka, bezlepková, "):
        name = name.replace("Mouka, bezlepková, ", "Bezlepková mouka, ")
    # "Kuskus, "
    if name.startswith("Kuskus, pšenice"):
        name = name.replace("Kuskus, pšenice", "Pšeničný kuskus")
    
    if item.get("name") != name:
        item["name"] = name
        count += 1

with open(path_cz, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print("Structural fixes applied to", count, "items.")
