import json
import re

input_file = "c:/Users/Fany/Desktop/FODMAP/monash_full_export_cz.json"

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

replacements = {
    # Bad direct translations
    r"Růžová voda": "Voda z růží (Růžová voda)",
    r"Voda z pomerančových květů": "Voda z pomerančových květů (Orange blossom water)",
    r"Želé, tráva, konzervy": "Bylinné želé (Grass jelly), konzervované",
    r"Kůže fazolového tvarohu": "Tofu kůže (Yuba)",
    r"Fazole, černé oči": "Fazole, černé oko",
    r"vyčerpaný": "okapaný",
    r"vyčerpané": "okapané",
    r"vyčerpaná": "okapaná",
    
    # Adjectives to Nouns
    r"^Jablkové,\s*": "Jablko, ",
    r"^Jablková,\s*": "Jablko, ",
    r"^Sýrový,\s*": "Sýr, ",
    r"^Sýrové,\s*": "Sýr, ",
    r"^Fazolové,\s*": "Fazole, ",
    r"^Fazolová,\s*": "Fazole, ",
    r"^Okurkové,\s*": "Okurka, ",
    r"^Okurková,\s*": "Okurka, ",
    r"^Bramborový,\s*": "Brambory, ",
    r"^Bramborové,\s*": "Brambory, ",
    r"^Smetanový,\s*": "Smetana, ",
    r"^Smetanové,\s*": "Smetana, ",
    r"^Bylinkový,\s*": "Bylinky, ",
    r"^Bylinkové,\s*": "Bylinky, ",
    r"^Čokoládové,\s*": "Čokoláda, ",
    r"^Čokoládový,\s*": "Čokoláda, ",
    r"^Zeleninový,\s*": "Zelenina, ",
    r"^Zeleninové,\s*": "Zelenina, ",
    r"^Ovocný,\s*": "Ovoce, ",
    r"^Ovocné,\s*": "Ovoce, ",
    r"^Pšeničný,\s*": "Pšenice, ",
    r"^Pšeničné,\s*": "Pšenice, ",
    r"^Rýžový,\s*": "Rýže, ",
    r"^Rýžové,\s*": "Rýže, ",
    r"^Rajčatový,\s*": "Rajče, ",
    r"^Rajčatové,\s*": "Rajčata, ",
    r"^Mrkvový,\s*": "Mrkev, ",
    r"^Mrkvové,\s*": "Mrkev, ",
    r"^Mléčný,\s*": "Mléko, ",
    r"^Mléčné,\s*": "Mléko, ",
    r"^Kukuřičný,\s*": "Kukuřice, ",
    r"^Kukuřičné,\s*": "Kukuřice, ",
    
    # Nuts
    r"^Ořechové, mandlové,\s*": "Mandle, ",
    r"^Ořechové, kešu,\s*": "Kešu ořechy, ",
    r"^Ořechové, lískové,\s*": "Lískové ořechy, ",
    r"^Ořechové, makadamové,\s*": "Makadamové ořechy, ",
    r"^Ořechové, arašídové,\s*": "Arašídy, ",
    r"^Ořechové, pekanové,\s*": "Pekanové ořechy, ",
    r"^Ořechové, borovicové,\s*": "Piniové oříšky, ",
    r"^Ořechové, pistáciové,\s*": "Pistácie, ",
    r"^Ořechové, vlašské,\s*": "Vlašské ořechy, ",
    r"^Ořechový,\s*": "Ořechy, ",
    r"^Ořechové,\s*": "Ořechy, ",
    
    # Miscellaneous specific fixes
    r"Bramborový, sladký / kumara, pomeranč, neloupaný, syrový": "Batáty / sladké brambory, oranžové, neloupané, syrové",
    r"Srdečná,\s*pomerančová": "Sirup, pomerančový",
    r"pomerančový,\s*lahůdkový styl": "oranžový, plátkový",
    r",\s*lahůdkový styl": ", plátkový",
    r"americký, pomerančový": "americký, oranžový",
    r"veganský \(sojový\)": "veganský (sójový)",
    r"soubory cookie": "sušenky",
    r"soubor cookie": "sušenka",
    r"1 soubor": "1 sušenka",
    r"1 soubory": "1 sušenka",
    r",\s*syrový$": ", syrové",
    
    # Translating "Bread, ..."
    r"Chlébové,\s*": "Chléb, ",
    r"Chlébový,\s*": "Chléb, ",
    
    # Meat / fish
    r"Hovězí maso": "Hovězí maso",
    r"Vepřové maso": "Vepřové maso",
    r"Kuřecí maso": "Kuřecí maso",
}

def clean_text(text):
    if not text:
        return text
    new_text = text
    for pattern, repl in replacements.items():
        new_text = re.sub(pattern, repl, new_text)
        
    # Extra generic cleanup for Adjective ending with 'ý', 'é', 'á' at start
    # We only do this if there's a comma right after.
    # Actually, regex is safer so we don't destroy words like "Káva" or "Čaj"
    return new_text

count = 0
for item in data:
    if "name" in item:
        orig = item["name"]
        new_name = clean_text(orig)
        if new_name != orig:
            item["name"] = new_name
            count += 1
            
    if "_category_name" in item:
        orig = item["_category_name"]
        if orig == "Občerstvení, bary & Soubory cookie" or orig == "Občerstvení, bary & sušenky":
            item["_category_name"] = "Svačinky, tyčinky a sušenky"
            count += 1
            
    if "serves" in item:
        for serve in item["serves"]:
            if "title" in serve:
                orig_title = serve["title"]
                new_title = clean_text(orig_title)
                if new_title != orig_title:
                    serve["title"] = new_title
                    count += 1

with open(input_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Fixed {count} extra instances.")
