import json

path_cz = 'c:/Users/Fany/Desktop/FODMAP/monash_full_export_cz.json'
with open(path_cz, 'r', encoding='utf-8') as f:
    data = json.load(f)

final_corrections = {
    # Cukry a sladidla
    "Cukr, hnědá": "Hnědý cukr",
    "Cukr, hnědý": "Hnědý cukr",
    "Cukr, kokos": "Kokosový cukr",
    "Cukr, demerara": "Třtinový cukr Demerara",
    "Cukr, poleva / prášek / cukrovinky": "Moučkový cukr",
    "Cukr, bílý": "Bílý cukr",
    "Sirup, agáve, tmavý": "Agávový sirup (tmavý)",
    "Sirup, agáve, světlo": "Agávový sirup (světlý)",
    "Sirup, extrakt z ječného sladu": "Sirup z ječného sladu",
    "Sirup, zlatý": "Zlatý sirup",
    "Sirup, javor, čistý": "Javorový sirup",
    "Sirup, melasa": "Melasa",
    "Sirup, rýžový slad": "Rýžový sirup",
    "Sirup, čirok": "Čirokový sirup",
    
    # Džemy a pomazánky
    "Pomazánka, džem, smíšené bobule": "Džem, lesní směs",
    "Pomazánka, marmeláda, malina": "Malinový džem",
    "Pomazánka, džem, jahoda": "Jahodový džem",
    "Pomazánka, marmeláda, citrusy": "Citrusová marmeláda",
    "Pomazánka, mandlové máslo": "Mandlové máslo",
    "Pomazánka, kešu máslo": "Kešu máslo",
    "Pomazánka, arašídové máslo": "Arašídové máslo",
    "Pomazánka, kaštanový krém": "Kaštanové pyré (slazené)",
    "Pomazánka, hořčice, Dijon": "Dijonská hořčice",
    "Pomazánka, hořčice": "Hořčice",
    
    # Koření a omáčky
    "Koření, pět koření": "Koření pěti vůní (Five spice)",
    "Omáčka, jablečný protlak": "Jablečné pyré (omáčka)",
    "Omáčka, grilování / BBQ": "BBQ omáčka",
    "Omáčka, černé fazole": "Omáčka z černých fazolí",
    "Omáčka, černý pepř, asijský styl": "Omáčka z černého pepře (asijská)",
    "Omáčka, sladkokyselá": "Sladkokyselá omáčka",
    "Omáčka, ryba": "Rybí omáčka",
    "Omáčka, ústřice": "Ústřicová omáčka",
    "Omáčka, sója": "Sójová omáčka",
    
    # Nápoje a další chyby
    "Káva, instantní, běžná, granule / prášek": "Instantní káva",
    "Káva, instantní, bezkofeinová, granule / prášek": "Instantní káva (bez kofeinu)",
    "Pijte, aloe, neochucené": "Aloe vera nápoj (neochucený)",
    "Nápoj, brusinka, 27% šťáva": "Brusinkový nápoj (27 % šťávy)",
    "Cola, dieta / nula / bez cukru": "Cola (light/zero)",
    "Limonáda, dietní / nula / bez cukru": "Limonáda (light/zero)",
    "Šťáva, směs bobulového ovoce (z džusu)": "Šťáva z lesních plodů",
    
    # Špatné želé
    "Instantní želé, limetka, dietní, připravené": "Limetkové želé (připravené z prášku, light)",
    "Instantní želé, malina, připravené": "Malinové želé (připravené z prášku)",
    "Instantní želé, jahody, připravené": "Jahodové želé (připravené z prášku)",
    "Ibišek": "Marshmallow",
    "Haw flakes / Hawthorn cukroví": "Haw flakes (Cukroví z hlohu)",
    
    # Nesmysly v bílkovinách
    "Alternativa masa, vegetariánská, mykoproteinová (bez česneku a cibule), mletá, vařené": "Mykoproteinové mleté maso (vegetariánské, vařené)",
    "Vejce, kuře, celé": "Slepičí vejce (celé)",
    "Kuře, všechny kusy, obyčejné, vařené": "Kuřecí maso (vařené, neochucené)",
    "Hovězí maso, všechny kusy, obyčejné, vařené": "Hovězí maso (vařené, neochucené)",
    "Vepřové maso, všechny kusy, obyčejné, vařené": "Vepřové maso (vařené, neochucené)",
    "Jehněčí maso, všechny kusy, obyčejné, vařené": "Jehněčí maso (vařené, neochucené)",
    "Ryby, všechny druhy, obyčejné": "Ryby (neochucené)",
    
    # Mouky a obilí
    "Tyčinka, svačina, na bázi pšenice": "Cereální tyčinka (pšeničná)",
    "Tyčinka, energie, ovoce a ořech": "Energetická tyčinka (ovoce a ořechy)",
    "Tyčinka, müsli, sušené ovoce": "Müsli tyčinka (se sušeným ovocem)",
    "Otruby, pšenice, nezpracované, nevařené": "Pšeničné otruby (syrové)",
    "Otruby, oves, nezpracované, nevařené": "Ovesné otruby (syrové)",
    "Kukuřičný koláč, obyčejný": "Kukuřičný chlebíček (neochucený)",
    "Rýžový koláč, obyčejný": "Rýžový chlebíček (neochucený)"
}

count = 0
for item in data:
    name = item.get("name", "")
    for bad, good in final_corrections.items():
        if bad in name:
            name = name.replace(bad, good)
    
    if item.get("name") != name:
        item["name"] = name
        count += 1

with open(path_cz, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print("Fix applied to", count, "items.")
