import json

path_cz = 'c:/Users/Fany/Desktop/FODMAP/monash_full_export_cz.json'
with open(path_cz, 'r', encoding='utf-8') as f:
    data = json.load(f)

corrections = {
    "Hovězí vývar (s česnekem a cibulí)": "Bujón / vývar (hovězí, s česnekem a cibulí)",
    "Hovězí vývar (bez česneku a cibule)": "Bujón / vývar (hovězí, bez česneku a cibule)",
    "Kuřecí vývar (s česnekem a cibulí)": "Bujón / vývar (kuřecí, s česnekem a cibulí)",
    "Kuřecí vývar (bez česneku a cibule)": "Bujón / vývar (kuřecí, bez česneku a cibule)",
    "Zeleninový vývar (s česnekem a cibulí)": "Bujón / vývar (zeleninový, s česnekem a cibulí)",
    "Zeleninový vývar (bez česneku a cibule)": "Bujón / vývar (zeleninový, bez česneku a cibule)"
}

for item in data:
    for bad, good in corrections.items():
        if item["name"] == bad:
            item["name"] = good

with open(path_cz, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
