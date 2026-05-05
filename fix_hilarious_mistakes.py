import json

input_file = "c:/Users/Fany/Desktop/FODMAP/monash_full_export_cz.json"

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Hardcoded dictionary for all the funny/bad literal translations
replacements = {
    "řízek": "Schnitzer", # Fix brand name
    "kapesní sklad": "The Pocket Storehouse",
    "Dietní vláknina": "Vláknina",
    "Doplněk stravy": "Doplněk stravy",
    "Enzymový doplněk": "Enzymatický doplněk",
    "Mandlové jídlo": "Mandlová mouka",
    "Prášek do pečiva": "Kypřící prášek",
    "Chléb, anglické / snídaňové muffiny": "Anglické / snídaňové muffiny",
    "Mouka, šípek": "Mouka, maranta třtinová (arrowroot)",
    "Mouka, besan / cizrna / gram": "Mouka, cizrnová (besan)",
    "Mouka, lepkavá rýže": "Mouka z lepkavé rýže",
    "Mouka, jednozrnka": "Mouka, jednozrnka (einkorn)",
    "Obilí, ječmen, perly, vařené": "Ječné krupky, vařené",
    "Obilí, ječmen, perly, celé, naklíčené": "Ječné krupky, celé, naklíčené",
    "Obilí, bulgur / burghul / burgaul / krakovaná pšenice, vař": "Bulgur, vařený",
    "Hominy, konzervy, scezené": "Hominy (loupaná kukuřice), konzervované, scezené",
    "Nudle, chaluhy, vařené": "Kelp nudle (z mořských řas), vařené",
    "Nudle, nudle (mungo fazole), vařené": "Skleněné nudle (mungo), vařené",
    "Nudle, nudle (sladké brambory), vařené": "Skleněné nudle (batátové), vařené",
    "Nudle, nudle, rýže, vařené": "Rýžové nudle (vermicelli), vařené",
    "Nudle, nudle, pšenice (Amoy), vařené": "Pšeničné nudle (vermicelli), vařené",
    "Těstoviny, tvrdá pšenice, vařené, okapané": "Těstoviny z tvrdé pšenice, vařené, okapané",
    "Těstoviny, noky (pšenice), vařené": "Noky (pšeničné), vařené",
    "Těstoviny, noky, bezlepkové": "Noky, bezlepkové",
    "Pečivo, listové, vařené": "Listové těsto, pečené/vařené",
    "Quinoa, černá, vařená": "Quinoa, černá, vařená",
    "Krupicová kaše, jemná, nevařená": "Krupice, jemná, nevařená",
    "Taco shell, kukuřice, obyčejný, tvrdý": "Taco skořápky, kukuřičné, neochucené, tvrdé",
    "Wontonův obal, nevařený": "Wonton těsto (plátky), nevařené",
    "Artyčok, zeměkoule, syrové": "Artyčok (Globe), syrový",
    "Artyčok, Jeruzalém, syrové": "Topinambur (Jeruzalémský artyčok), syrový",
    "Lilek / Brinjal / Lilek, neloupaný, syrové": "Lilek, neloupaný, syrový",
    "Fazole, chřest / yardlong / hadí boby, syrové": "Dlouhatec (hadí fazole), syrové",
    "Zelí, čínské / wombok, syrové": "Pekingské zelí (Wombok), syrové",
    "Celer (pouze stopkový), syrové": "Řapíkatý celer, syrový",
    "Cho Cho / Chayote / Choko, syrové": "Čajot, syrový",
    "Kukuřice, dítě, konzerva, okapaná": "Mini kukuřice, konzervovaná, okapaná",
    "Kukuřice, smetana, konzerva": "Kukuřice krémová (creamed corn), konzervovaná",
    "Houba, bílá hřbet černá, sušená": "Jidášovo ucho (černá houba), sušená",
    "Srdce z palem, konzervované ve slaném nálevu, scezené": "Palmová srdce, konzervovaná, scezená",
    "Salát, máslo, syrové": "Hlávkový salát (máslový), syrový",
    "Salát, cos / římský, syrové": "Římský salát, syrový",
    "Hlávkový salát, čekanky, syrové": "Radicchio (čekanka), syrové",
    "Salát, červený korál, syrové": "Salát Lollo Rosso (červený korál), syrový",
    "Salát, rukola / rukola, syrové": "Rukola, syrová",
    "Houba, černá liška, sušená": "Stroček trubkovitý, sušený",
    "Houba, knoflík, syrová": "Žampiony, syrové",
    "Houby, žampiony / bílý knoflík, konzerva ve slaném nálevu, okapaná": "Žampiony, konzervované, okapané",
    "Houby, hříbky / porchino / penny houska, sušené": "Hříbky (Porcini), sušené",
    "Houba, portobella / portobello / obří cremini, syr": "Portobello houby, syrové",
    "Houba, červená borovice / šafránová čepice, syrová": "Ryzec pravý, syrový",
    "Houba, kluzký jack / lepkavá buchta, syrová": "Klouzek, syrový",
    "Hrášek, sníh / mangetout, syrové": "Cukrový hrášek (ploché lusky), syrový",
    "Hrášek, cukr, syrové": "Cukrový hrášek (kulaté lusky), syrový",
    "Brambory, sladké / kumara, fialové, neloupané, syrové": "Batáty, fialové, neloupané, syrové",
    "Brambory, sladké / kumara, bílé, neloupané, syrové": "Batáty, bílé, neloupané, syrové",
    "Dýně / tykev, žalud, loupaná, syrová": "Žaludová dýně, loupaná, syrová",
    "Dýně / tykev, žalud, neloupaná, syrová": "Žaludová dýně, neloupaná, syrová",
    "Dýně / tykev, máslová, neloupaná, syrová": "Máslová dýně, neloupaná, syrová",
    "Dýně / tykev, Delicata, loupaná, syrová": "Dýně Delicata, loupaná, syrová",
    "Dýně / tykev, japonská / Kabocha / Kent, neloupaná, syrová": "Dýně Kabocha / japonská, neloupaná, syrová",
    "Dýně / tykev, cukr, loupaná, syrová": "Dýně cukrová, loupaná, syrová",
    "Rutabaga / Švédská / Švédská tuřín, neloupaná, syrová": "Tuřín (kolník), neloupaný, syrový",
    "Švýcarský mangold / Stříbrná řepa, syrové": "Mangold, syrový",
    "Squash, knoflík / placička / hřebenatka, syrové": "Patizon, syrový",
    "Squash, rovný krk, žlutý, syrové": "Cuketa žlutá (straightneck), syrová",
    "Rajčatová, třešňová, syrová": "Cherry rajčata, syrová",
    "Rajčatová, romská / švestková, konzerva, se šťávou": "Rajčata San Marzano / oválná, konzervovaná",
    "Witlof / Witloof / Belgická endivie, syrová": "Čekanka puky (Witlof), syrová",
    "Pudinkové jablko, oloupané, zbavené pecek, syrové": "Čerimoja (Custard apple), syrová",
    "Meloun, meloun / meloun, loupaný, zbavený semínek, syrové": "Meloun Cantaloupe, loupaný, syrový",
    "Meloun, medová rosa, bílá slupka, oloupaná, zbavená semínek, syrová": "Žlutý meloun (Honeydew), loupaný, syrový",
    "Smíšená kůra, citrusové plody": "Kandovaná kůra, citrusy",
    "Sušené švestky / Sušené švestky": "Sušené švestky",
    "Kůra / kůra, citron": "Citronová kůra",
    "Kůra / kůra, pomeranč": "Pomerančová kůra",
    "Sýr, americké, pomerančové, předem zabalené singly": "Sýr, americký, oranžový, plátkový (balený)",
    "Sýr, americké, bílé, předem zabalené singly": "Sýr, americký, bílý, plátkový (balený)",
    "Sýr, modrý": "Sýr, Niva / modrý sýr",
    "Sýr, chaloupka": "Sýr, Cottage",
    "Sýr, smetana, česnek a bylinky, běžný tuk": "Smetanový sýr, česnek a bylinky, plnotučný",
    "Sýr, smetana, obyčejný tuk": "Smetanový sýr, obyčejný, plnotučný",
    "Smetana, čistý, běžný tuk": "Smetana, plnotučná",
    "Smetana, kyselý, běžný tuk": "Zakysaná smetana, plnotučná",
    "Smetana, zahuštěný, pravidelný tuk": "Smetana ke šlehání, plnotučná",
    "Smetana, šlehané, čerstvé": "Šlehačka, čerstvá",
    "Pudinka, vanilka, obyčejný tuk": "Vanilkový pudink, plnotučný",
    "Mléko, kravské, odpařené, normální tuk": "Kondenzované mléko neslazené, plnotučné",
    "Mléko, kráva, odstředěné": "Mléko, kravské, odtučněné",
    "Fazole, černé (frijoles), konzervy, okapané": "Fazole, černé (frijoles), konzervované, okapané",
    "Fazole, fazole / navy, sušené, vařené, okapané": "Fazole, bílé (navy), sušené, vařené, okapané",
    "Hrášek rozpůlený, sušený, uvařený, scezený": "Hrách půlený, sušený, uvařený, scezený",
    "Fazole, mungo / zelené gramy, sušené, loupané, štípané, vařené, okapané": "Mungo fazole, půlené, loupané, vařené",
    "Alternativa masa, vegetariánská, texturovaný rostlinný protein (TVP) (na bázi sójového proteinu)": "Sójové maso (TVP)",
    "Alternativa masa, vegetariánská, falešné kuře (na bázi sojových bobů)": "Falešné kuře (veganské sójové maso)",
    "Semínková, chia, černá, sušená": "Chia semínka, černá, sušená",
    "Semínková, maková, černá": "Mák, černý",
    "Čokoládový prášek, 23% kakaa": "Prášek na horkou čokoládu, 23% kakaa",
    "Šťáva, jablko, 99% rekonstituovaný": "Jablečný džus, 99% z koncentrátu",
    "Šťáva, pomeranč, 99% rekonstituovaná a čerstvá směs": "Pomerančový džus, 99% z koncentrátu",
    "Limonáda, dietní / nula / bez cukru": "Limonáda, light / zero / bez cukru",
    "Čaj, černé, silné, sójové mléko (sójové boby)": "Čaj, černý, silný, sójové mléko",
    "Víno, lepkavé / dezert / obohacené": "Víno, dezertní / portské",
    "Krevety / Krevety, všechny druhy, hladké, vařené": "Krevety, všechny druhy, neochucené, vařené",
    "Klobása, Saucisson (francouzská uzená klobása)": "Klobása, Saucisson (francouzská sušená)",
    "Pomazánka z mléčné směsi, másla a jedlého oleje": "Směsný tuk (máslo a rostlinný olej)",
    "Čínské / Shaoxing víno na vaření": "Shaoxing (čínské rýžové víno na vaření)",
    "Nutriční droždí, vločky": "Lahůdkové droždí, vločky",
    "Protlak, rajčatový protlak / koncentrát": "Rajčatový protlak / koncentrát",
    "Zázvorové pivo (obsahuje zázvor)": "Zázvorové pivo (Ginger beer)",
    "Ovesné krupice, tepelně neupravené": "Oves, kroupy, nevařené",
    "Ovesné, rychlé, nevařené": "Ovesné vločky, jemné (rychlé), nevařené",
    "Sýr, parmazán": "Parmezán",
    "Klokan, všechny kusy, obyčejný, vařený": "Klokaní maso, neochucené, vařené"
}

count = 0
for item in data:
    if "name" in item:
        name = item["name"]
        for bad, good in replacements.items():
            if bad in name:
                name = name.replace(bad, good)
        if name != item["name"]:
            item["name"] = name
            count += 1
            
    if "serves" in item:
        for serve in item["serves"]:
            if "title" in serve:
                title = serve["title"]
                for bad, good in replacements.items():
                    if bad in title:
                        title = title.replace(bad, good)
                if title != serve["title"]:
                    serve["title"] = title
                    count += 1

with open(input_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Fixed {count} instances.")
