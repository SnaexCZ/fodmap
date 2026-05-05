import json
import os
from bottle import response, static_file, request

# Detekce prostředí pro lokální testování na Windows vs. běh na Androidu
if os.path.exists("monash_full_export_cz.json"):
    SLOZKA = "."
    DB_CESTA = "monash_full_export_cz.json"
else:
    SLOZKA = "/storage/emulated/0/PyServe/fodmap_plugin"
    DB_CESTA = "/storage/emulated/0/PyServe/monash_cz_cista.json"

import unicodedata

def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', str(s)) if unicodedata.category(c) != 'Mn')

def register(app):
    @app.route("/fodmap")
    @app.route("/fodmap/")
    def index():
        return static_file("index.html", root=SLOZKA)

    @app.route("/fodmap/api/kategorie")
    def get_categories():
        if not os.path.exists(DB_CESTA): return {"kategorie": []}
        with open(DB_CESTA, "r", encoding="utf-8") as f: data = json.load(f)
        kat = set(str(i.get("_category_name", "")).replace("&amp;", "&") for i in data if i.get("_category_name"))
        return {"kategorie": sorted(list(kat))}

    @app.route("/fodmap/api/hledej/<query>")
    def api_search(query):
        is_category_search = False
        if query.startswith("cat:"):
            is_category_search = True
            query_norm = strip_accents(query[4:].strip().lower())
            query_words = []
        else:
            query_norm = strip_accents(query.lower().strip())
            query_words = query_norm.split()
        
        # Načtení limitů z URL (pokud chybí, bere 3 = povolí vše)
        l_fru = int(request.query.fru or 3)
        l_lak = int(request.query.lak or 3)
        l_man = int(request.query.man or 3)
        l_sor = int(request.query.sor or 3)
        l_gos = int(request.query.gos or 3)
        l_frun = int(request.query.frun or 3)

        vysledky = []
        if not os.path.exists(DB_CESTA): return {"vysledky": []}
        with open(DB_CESTA, "r", encoding="utf-8") as f: data = json.load(f)

        for item in data:
            raw_name = str(item.get("name", ""))
            name_norm = strip_accents(raw_name.lower())
            
            raw_cat = str(item.get("_category_name", "")).replace("&amp;", "&")
            cat_norm = strip_accents(raw_cat.lower())
            
            # Pokud se jedná o kliknutí na kategorii, hledáme přesnou shodu jen v kategorii
            if is_category_search:
                match = (query_norm == cat_norm)
            else:
                # Pokud se hledá textem, slova musí být v názvu, NEBO uživatel napsal název kategorie
                match = (query_norm == cat_norm) or all(word in name_norm for word in query_words)
            
            if match:
                porce_seznam = []
                serves = item.get("serves") or []
                try: serves = sorted(serves, key=lambda x: int(x.get("display_order", 99)))
                except: pass

                # FILTRACE PROBÍHÁ PRO KAŽDOU PORCI ZVLÁŠŤ
                for s in serves:
                    f_arr = s.get("fodmap", [1,1,1,1,1,1,1,1])
                    # DEFINITIVNÍ MAPOVÁNÍ (Ověřeno proti česneku, jablku i fazolím):
                    # Index 0: Fruktóza
                    # Index 1: Laktóza
                    # Index 2: Sorbitol
                    # Index 3: Mannitol
                    # Index 4: Fruktany (Fru-n)
                    # Index 5: GOS
                    # Index 6: Pomocný index (pro tečky ignorujeme)
                    f_fru  = f_arr[0] if len(f_arr)>0 else 1
                    f_lak  = f_arr[1] if len(f_arr)>1 else 1
                    f_sor  = f_arr[2] if len(f_arr)>2 else 1
                    f_man  = f_arr[3] if len(f_arr)>3 else 1
                    f_frun = f_arr[4] if len(f_arr)>4 else 1
                    f_gos  = f_arr[5] if len(f_arr)>5 else 1
                    
                    # Zkontrolujeme, jestli CUKRY V TÉTO PORCI nevyletěly nad náš bezpečný limit
                    if f_frun <= l_frun and f_gos <= l_gos and f_lak <= l_lak and f_fru <= l_fru and f_sor <= l_sor and f_man <= l_man:
                        titulek = str(s.get("title", "")).strip() or "Standardní porce"
                        vaha = str(s.get("measurement_value", "")).strip()
                        barva_porce = max(f_arr[0:6]) if len(f_arr) >= 6 else 1

                        porce_seznam.append({
                            "titulek": titulek, "vaha": vaha, "barva": barva_porce, "info": s.get("comment", ""),
                            "cukry": [
                                {"n": "Fru", "v": f_fru}, {"n": "Lak", "v": f_lak},
                                {"n": "Man", "v": f_man}, {"n": "Sor", "v": f_sor},
                                {"n": "GOS", "v": f_gos}, {"n": "Fru-n","v": f_frun}
                            ]
                        })
                
                # Pokud po smazání špatných porcí zbyla aspoň jedna bezpečná, jídlo ukážeme
                if len(porce_seznam) > 0:
                    cisty_nazev_kat = str(item.get("_category_name", "")).replace("&amp;", "&")
                    vysledky.append({"n": item.get("name"), "k": cisty_nazev_kat, "o": item.get("overall", 1), "p": porce_seznam})
                    
        return {"vysledky": vysledky[:50]}

if __name__ == "__main__":
    import bottle
    app = bottle.Bottle()
    register(app)
    print("Spouštím lokální testovací server na http://localhost:8080/fodmap")
    app.run(host="localhost", port=8080, debug=True)
