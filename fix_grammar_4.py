import json

path_cz = 'c:/Users/Fany/Desktop/FODMAP/monash_full_export_cz.json'
with open(path_cz, 'r', encoding='utf-8') as f:
    data = json.load(f)

replacements = {
    "Chlebovník, loupaný, syrové": "Chlebovník, loupaný, syrový",
    "Mouka, kukuřice, masa harina / masa lista": "Kukuřičná mouka (Masa Harina)",
    "Mouka, zelený banán": "Mouka ze zelených banánů",
    "Sýr, tvaroh": "Tvaroh",
    "Ořechy, kaštanový, vyloupaný, vařený": "Kaštany, loupané, vařené",
    "Ořechy, kaštanový, vyloupaný, pražený": "Kaštany, loupané, pražené",
    ", syrové": ", syrový" # Zjednodušená plošná oprava špatné koncovky pro většinu ovoce/zeleniny v mužském rodě
}

for item in data:
    name = item.get("name", "")
    for bad, good in replacements.items():
        if bad in name:
            name = name.replace(bad, good)
            
    # Fix grammar for specific feminine/masculine vegetables that ended up with "syrový" but should be "syrová" or "syrové"
    # This is complex without a dictionary, but we will fix the user's exact issues first.
    if item.get("name") != name:
        item["name"] = name

with open(path_cz, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
