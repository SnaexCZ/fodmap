import json
data=json.load(open('monash_full_export_cz.json', encoding='utf-8'))
for item in data:
    s = item['serves'][0]
    f = s.get('fodmap', [])
    if len(f) > 0 and max(f[0:8]) == 3:
        try:
            print(item['name'].encode('ascii', 'ignore').decode(), f)
        except:
            pass
