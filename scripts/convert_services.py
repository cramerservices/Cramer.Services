import json
import os
import sys
import pandas as pd

SRC_XLSX = "Services.xlsx"
OUT_JSON = os.path.join("data", "services.json")

# Expected columns in Excel (first row is headers):
# slug | name | price | sales price | image | description | bullet points | contact us | payment
# - "bullet points" separated by ';'
# - "contact us" and "payment" are yes/no (case-insensitive)

def yn_to_bool(v):
    return str(v).strip().lower() in ("y", "yes", "true", "1")

def money_or_none(v):
    if pd.isna(v) or str(v).strip() == "":
        return None
    try:
        return float(v)
    except:
        # If they already include $ etc., try to clean it
        s = str(v).replace("$","").replace(",","").strip()
        try:
            return float(s)
        except:
            return None

def main():
    if not os.path.exists(SRC_XLSX):
        print(f"ERROR: {SRC_XLSX} not found in repo root.", file=sys.stderr)
        sys.exit(1)

    df = pd.read_excel(SRC_XLSX)

    # Normalize column names
    cols = {c.strip().lower(): c for c in df.columns}
    required = ["slug","name","price","sales price","image","description","bullet points","contact us","payment"]
    for r in required:
        if r not in cols:
            raise SystemExit(f"Missing column in Excel: '{r}'")

    out = []
    for _, row in df.iterrows():
        slug   = str(row[cols["slug"]]).strip()
        name   = str(row[cols["name"]]).strip()
        price  = money_or_none(row[cols["price"]])
        sale   = money_or_none(row[cols["sales price"]])
        image  = str(row[cols["image"]]).strip() if not pd.isna(row[cols["image"]]) else ""
        desc   = str(row[cols["description"]]).strip() if not pd.isna(row[cols["description"]]) else ""
        bullets_raw = "" if pd.isna(row[cols["bullet points"]]) else str(row[cols["bullet points"]])
        bullets = [b.strip() for b in bullets_raw.split(";") if b.strip()]
        contact = yn_to_bool(row[cols["contact us"]])
        payment = yn_to_bool(row[cols["payment"]])

        out.append({
            "slug": slug,
            "name": name,
            "price": price,            # number or null
            "salePrice": sale,         # number or null
            "image": image,            # path/URL to image OR video
            "description": desc,       # used for hover + first paragraph
            "bullets": bullets,        # array of bullet strings
            "contact": contact,        # boolean
            "payment": payment         # boolean
        })

    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"Wrote {OUT_JSON} with {len(out)} services")

if __name__ == "__main__":
    main()
