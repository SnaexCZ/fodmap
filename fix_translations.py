import json
import re

input_file = "c:/Users/Fany/Desktop/FODMAP/monash_full_export_cz.json"

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

replacements = {
    r"Jablkové, růžové": "Jablko, odrůda Pink Lady",
    r"^Jablkové,\s*": "Jablko, ",
    r"^Sýrový,\s*": "Sýr, ",
    r"^Sýrové,\s*": "Sýr, ",
    r"^Fazolové,\s*": "Fazole, ",
    r"^Okurkové,\s*": "Okurka, ",
    r"Bramborový, sladký / kumara, pomeranč, neloupaný, syrový": "Batáty / sladké brambory, oranžové, neloupané, syrové",
    r"^Bramborový,\s*": "Brambory, ",
    r"^Bramborové,\s*": "Brambory, ",
    r"^Smetanový,\s*": "Smetana, ",
    r"^Smetanové,\s*": "Smetana, ",
    r"^Bylinkový,\s*": "Bylinky, ",
    r"^Bylinkové,\s*": "Bylinky, ",
    r"^Čokoládové,\s*": "Čokoláda, ",
    r"^Ořechové, mandlové,\s*": "Mandle, ",
    r"^Ořechové, kešu,\s*": "Kešu ořechy, ",
    r"^Ořechové, lískové,\s*": "Lískové ořechy, ",
    r"^Ořechové, makadamové,\s*": "Makadamové ořechy, ",
    r"^Ořechové, arašídové,\s*": "Arašídy, ",
    r"^Ořechové, pekanové,\s*": "Pekanové ořechy, ",
    r"^Ořechové, borovicové,\s*": "Piniové oříšky, ",
    r"^Ořechové, pistáciové,\s*": "Pistácie, ",
    r"^Srdečná,\s*pomerančová": "Sirup, pomerančový",
    r"černé oči": "černé oko",
    r"pomerančový,\s*lahůdkový styl": "oranžový, plátkový",
    r",\s*lahůdkový styl": ", plátkový",
    r"vyčerpaný": "okapaný",
    r"vyčerpané": "okapané",
    r"americký, pomerančový": "americký, oranžový",
    r"veganský \(sojový\)": "veganský (sójový)",
}

count = 0
for item in data:
    if "name" in item:
        orig = item["name"]
        new_name = orig
        for pattern, repl in replacements.items():
            new_name = re.sub(pattern, repl, new_name)
        if new_name != orig:
            item["name"] = new_name
            count += 1
            
    if "_category_name" in item:
        if item["_category_name"] == "Občerstvení, bary & Soubory cookie":
            item["_category_name"] = "Svačinky, tyčinky a sušenky"
            count += 1
            
    if "serves" in item:
        for serve in item["serves"]:
            if "title" in serve:
                orig_title = serve["title"]
                new_title = orig_title.replace("1 soubor", "1 sušenka").replace("soubory cookie", "sušenky").replace("soubor cookie", "sušenka")
                if new_title != orig_title:
                    serve["title"] = new_title
                    count += 1

with open(input_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Fixed {count} instances.")
