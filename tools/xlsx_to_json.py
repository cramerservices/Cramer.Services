import pandas as pd, json, sys

src = sys.argv[1] if len(sys.argv) > 1 else 'Services.xlsx'
out = sys.argv[2] if len(sys.argv) > 2 else 'data/services.json'

df = pd.read_excel(src)
# expected column names (case-insensitive): slug, name, price, sales price, image, description, bullet points, contact us, payment
df.columns = [str(c).strip().lower() for c in df.columns]

def split_bullets(val):
    if pd.isna(val): return []
    return [x.strip() for x in str(val).split(';') if x.strip()]

rows = []
for _,r in df.iterrows():
    rows.append({
        "slug": r.get("slug",""),
        "name": r.get("name",""),
        "price": r.get("price",""),
        "sales_price": r.get("sales price",""),
        "image": r.get("image",""),
        "description": r.get("description",""),
        "bullets": split_bullets(r.get("bullet points","")),
        "contact_us": r.get("contact us",""),
        "payment": r.get("payment","")
    })

with open(out, 'w', encoding='utf-8') as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)

print(f"Wrote {len(rows)} services to {out}")
