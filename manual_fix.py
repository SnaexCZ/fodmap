import json

path_cz = 'c:/Users/Fany/Desktop/FODMAP/monash_full_export_cz.json'
with open(path_cz, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Finální manuální korekce od AI (přímý zásah do dat)
corrections = {
    "Kakaové hroty": "Kakaové boby (drcené)",
    "Agar agar": "Agar (rostlinná želatina)",
    "Čokoláda, tmavé": "Čokoláda, hořká",
    "Čokoláda, mléko": "Čokoláda, mléčná",
    "Ovocná kůže": "Ovocné plátky (sušené)",
    "Sýr, chaloupka": "Sýr Cottage",
    "Houba, knoflík": "Žampiony",
    "Kukuřice, dítě": "Mini kukuřice",
    "Víno, lepkavé": "Víno, dezertní",
    "Voda z pomerančových květů": "Voda z pomerančových květů (Orange blossom water)",
    "Růžová voda": "Růžová voda",
    "Kůže fazolového tvarohu": "Tofu kůže (Yuba)",
    "Želé, tráva, konzervy": "Bylinné želé (Grass jelly)",
    "Smetana, čistý": "Smetana (čistá)",
    "Smetana, kyselý": "Zakysaná smetana",
    "Bramborový, sladký": "Batáty (sladké brambory)",
    "Houba, červená borovice": "Ryzec pravý",
    "Houba, kluzký jack": "Klouzek",
    "Taco shell": "Taco skořápka",
    "Wontonův obal": "Wonton těsto",
    "Ovesné krupice": "Ovesné kroupy",
    "Snídaňové cereálie, pufovaná nebo popučená rýže": "Burisony (pufovaná rýže)"
}

# Projdeme vše a aplikujeme lidskou logiku na gramatiku
for item in data:
    name = item.get("name", "")
    # Oprava koncovek a specifických pojmů
    for bad, good in corrections.items():
        if bad in name:
            name = name.replace(bad, good)
    
    # Sjednocení názvosloví (Adjektivum -> Substantivum na začátku)
    if name.startswith("Jablkové,"): name = name.replace("Jablkové,", "Jablko,")
    if name.startswith("Sýrový,"): name = name.replace("Sýrový,", "Sýr,")
    if name.startswith("Fazolové,"): name = name.replace("Fazolové,", "Fazole,")
    if name.startswith("Okurkové,"): name = name.replace("Okurkové,", "Okurka,")
    if name.startswith("Bramborové,"): name = name.replace("Bramborové,", "Brambory,")
    if name.startswith("Smetanové,"): name = name.replace("Smetanové,", "Smetana,")
    if name.startswith("Bylinkové,"): name = name.replace("Bylinkové,", "Bylinky,")
    
    item["name"] = name

with open(path_cz, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
