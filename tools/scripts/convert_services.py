#!/usr/bin/env python3
import json, math, pathlib
import pandas as pd

XLSX_PATH = pathlib.Path("Services.xlsx")
JSON_PATH = pathlib.Path("services.json")

df = pd.read_excel(XLSX_PATH, dtype=str).fillna("")

def as_bool(val: str) -> bool:
    return str(val).strip().lower() in {"y","yes","true","1"}

def as_money(val: str):
    s = str(val).strip().replace("$","").replace(",","")
    if s == "" or s.lower() == "na":
        return None
    try:
        n = float(s)
        return int(n) if abs(n - round(n)) < 1e-9 else round(n, 2)
    except:
        return None

items = []
for _, r in df.iterrows():
    slug = r.get("slug","").strip()
    if not slug or slug.lower() == "slug":
        continue

    bullets = [b.strip() for b in str(r.get("bullet points","")).split(";") if b.strip()]
    needs_contact = as_bool(r.get("contact us",""))
    needs_payment = as_bool(r.get("payment",""))

    if needs_contact and needs_payment:
        action = "contact_then_checkout"
    elif needs_payment:
        action = "checkout"
    elif needs_contact:
        action = "contact"
    else:
        action = "none"

    items.append({
        "slug": slug,
        "name": r.get("name","").strip(),
        "price": as_money(r.get("price","")),
        "salePrice": as_money(r.get("sale price","")),
        "image": r.get("image","").strip(),
        "description": r.get("description","").strip(),
        "bullets": bullets,
        "needsContact": needs_contact,
        "needsPayment": needs_payment,
        "action": action
    })

JSON_PATH.write_text(json.dumps(items, indent=2), encoding="utf-8")
print(f"Wrote {JSON_PATH} with {len(items)} services.")
