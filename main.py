import json
import os
import urllib.request
import urllib.error
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

def load_db():
    if not os.path.exists(DB_CESTA):
        return []
    with open(DB_CESTA, "r", encoding="utf-8") as f:
        return json.load(f)

def build_food_context(food_name):
    data = load_db()
    query_norm = strip_accents(food_name.lower().strip())
    results = []
    for item in data:
        name_norm = strip_accents(str(item.get("name", "")).lower())
        if query_norm in name_norm or name_norm in query_norm:
            serves = item.get("serves") or []
            serves_info = []
            for s in serves:
                f_arr = s.get("fodmap", [1,1,1,1,1,1,1,1])
                serves_info.append({
                    "porce": s.get("title", ""),
                    "vaha": s.get("measurement_value", ""),
                    "fodmap": {
                        "fruktóza": f_arr[0] if len(f_arr)>0 else 1,
                        "laktóza": f_arr[1] if len(f_arr)>1 else 1,
                        "sorbitol": f_arr[2] if len(f_arr)>2 else 1,
                        "mannitol": f_arr[3] if len(f_arr)>3 else 1,
                        "fruktany": f_arr[4] if len(f_arr)>4 else 1,
                        "GOS": f_arr[5] if len(f_arr)>5 else 1,
                    },
                    "komentar": s.get("comment", "")
                })
            results.append({
                "nazev": item.get("name"),
                "kategorie": str(item.get("_category_name", "")).replace("&amp;", "&"),
                "celkove": item.get("overall", 1),
                "porce": serves_info
            })
            if len(results) >= 5:
                break
    return results

def build_plate_context(plate_items):
    data = load_db()
    context = []
    for item in plate_items:
        food_name = item.get("n", "")
        serving_title = item.get("t", "")
        serving_weight = item.get("v", "")
        query_norm = strip_accents(food_name.lower().strip())
        for db_item in data:
            name_norm = strip_accents(str(db_item.get("name", "")).lower())
            if query_norm == name_norm or query_norm in name_norm:
                serves = db_item.get("serves") or []
                matched_serve = None
                for s in serves:
                    if s.get("title", "") == serving_title or str(s.get("measurement_value", "")) == str(serving_weight):
                        matched_serve = s
                        break
                if not matched_serve and serves:
                    matched_serve = serves[0]
                if matched_serve:
                    f_arr = matched_serve.get("fodmap", [1,1,1,1,1,1,1,1])
                    level_map = {1: "Nízký (bezpečný)", 2: "Střední (pozor na množství)", 3: "Vysoký (nevhodný)"}
                    context.append({
                        "potravina": food_name,
                        "porce": f"{matched_serve.get('measurement_value', '')}g - {matched_serve.get('title', '')}",
                        "fodmap": {
                            "fruktóza": level_map.get(f_arr[0] if len(f_arr)>0 else 1, ""),
                            "laktóza": level_map.get(f_arr[1] if len(f_arr)>1 else 1, ""),
                            "sorbitol": level_map.get(f_arr[2] if len(f_arr)>2 else 1, ""),
                            "mannitol": level_map.get(f_arr[3] if len(f_arr)>3 else 1, ""),
                            "fruktany": level_map.get(f_arr[4] if len(f_arr)>4 else 1, ""),
                            "GOS": level_map.get(f_arr[5] if len(f_arr)>5 else 1, ""),
                        },
                        "komentar": matched_serve.get("comment", "")
                    })
                break
    return context

SYSTEM_PROMPT = """Jsi FODMAP asistent pro české uživatele. Odpovídej VÝHRADNĚ na základě poskytnutých dat z databáze Monash University FODMAP. Nikdy nevymýšlej informace, které nejsou v datech.

Pravidla:
1. Všechny odpovědi musí být založeny na poskytnutých databázových datech
2. Pokud potravina není v databázi, řekni to explicitně
3. Používej tyto úrovně: 1 = Nízký FODMAP (bezpečný), 2 = Střední FODMAP (pozor na množství), 3 = Vysoký FODMAP (nevhodný)
4. Odpovídej česky
5. Buď stručný a výstižný
6. Pokud analyzuješ talíř, zhroť každou potravinu zvlášť a pak celkový dojem
7. Nikdy nepředkládej pouze své dojmy - vždy se opírej o data"""

def call_gemini(api_key, messages, system_prompt=None):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    sys_prompt = system_prompt or SYSTEM_PROMPT
    contents = []
    for msg in messages:
        role = "model" if msg["role"] == "assistant" else "user"
        contents.append({"role": role, "parts": [{"text": msg["content"]}]})
    payload = {
        "contents": contents,
        "system_instruction": {"parts": [{"text": sys_prompt}]}
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url + f"?key={api_key}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            text = result["candidates"][0]["content"]["parts"][0]["text"]
            return {"ok": True, "text": text}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        error_msg = f"HTTP {e.code}: {body}"
        if e.code == 429:
            if "free_tier" in body.lower() or "quota exceeded" in body.lower():
                error_msg = "QUOTA_EXCEEDED: Vyčerpaná denní kvóta free tier. Zkontrolujte billing na https://aistudio.google.com nebo zkuste znovu zítra."
            else:
                error_msg = "QUOTA_EXCEEDED: Příliš mnoho požadavků. Počkejte chvíli a zkuste znovu."
        elif e.code == 401:
            error_msg = "AUTH_ERROR: Neplatný API klíč. Zkontrolujte jej v nastavení."
        elif e.code == 403:
            error_msg = "ACCESS_DENIED: API klíč nemá oprávnění. Zkontrolujte nastavení v Google AI Studio."
        return {"ok": False, "error": error_msg}
    except Exception as e:
        return {"ok": False, "error": str(e)}

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

    @app.route("/fodmap/api/gemini/check", method="POST")
    def gemini_check_plate():
        body = request.json or {}
        api_key = body.get("apiKey", "")
        plate = body.get("plate", [])
        if not api_key:
            return {"ok": False, "error": "Chybí API klíč"}
        if not plate:
            return {"ok": False, "error": "Talíř je prázdný"}
        plate_context = build_plate_context(plate)
        if not plate_context:
            return {"ok": False, "error": "Nepodařilo se načíst data o potravinách z databáze"}
        context_str = json.dumps(plate_context, ensure_ascii=False, indent=2)
        user_msg = f"Zkontroluj tento talíř z hlediska FODMAP. Seznam potravin a jejich dat z databáze:\n\n{context_str}\n\nZhroť každou potravinu a poté dej celkové doporučení."
        result = call_gemini(api_key, [{"role": "user", "content": user_msg}])
        return result

    @app.route("/fodmap/api/gemini/chat", method="POST")
    def gemini_chat():
        body = request.json or {}
        api_key = body.get("apiKey", "")
        messages = body.get("messages", [])
        user_question = body.get("question", "")
        if not api_key:
            return {"ok": False, "error": "Chybí API klíč"}
        if not user_question:
            return {"ok": False, "error": "Chybí otázka"}
        food_context = []
        import re
        words = re.findall(r'\b[a-zA-Zá-žÁ-Ž]{3,}\b', user_question)
        for word in words:
            found = build_food_context(word)
            for f in found:
                if f not in food_context:
                    food_context.append(f)
        context_str = json.dumps(food_context, ensure_ascii=False, indent=2) if food_context else "Žádné konkrétní potraviny nebyly nalezeny v databázi."
        system_with_context = SYSTEM_PROMPT + f"\n\nAktuální relevantní data z databáze pro tuto otázku:\n{context_str}"
        chat_messages = messages + [{"role": "user", "content": user_question}]
        result = call_gemini(api_key, chat_messages, system_with_context)
        return result

    @app.route("/fodmap/api/gemini/validate", method="POST")
    def gemini_validate_key():
        body = request.json or {}
        api_key = body.get("apiKey", "")
        if not api_key:
            return {"ok": False, "error": "Chybí API klíč"}
        result = call_gemini(api_key, [{"role": "user", "content": "Odpověz jedním slovem: ano"}])
        return result

if __name__ == "__main__":
    import bottle
    app = bottle.Bottle()
    register(app)
    print("Spouštím lokální testovací server na http://localhost:8080/fodmap")
    app.run(host="localhost", port=8080, debug=True)
