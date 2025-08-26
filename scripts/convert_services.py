import json
import os
import sys
import pandas as pd

SRC_XLSX = "Services.xlsx"
OUT_JSON = os.path.join("data", "services.json")

# Helpers
def yn_to_bool(v):
    return str(v).strip().lower() in ("y", "yes", "true", "1")

def money_or_none(v):
    if pd.isna(v) or str(v).strip() == "":
        return None
    try:
        return float(v)
    except Exception:
        s = str(v).replace("$", "").replace(",", "").strip()
        try:
            return float(s)
        except Exception:
            return None

def main():
    if not os.path.exists(SRC_XLSX):
        print(f"ERROR: {SRC_XLSX} not found in repo root.", file=sys.stderr)
        sys.exit(1)

    df = pd.read_excel(SRC_XLSX)

    # normalize headers -> original name
    cols = {c.strip().lower(): c for c in df.columns}

    # Required (minimal) columns
    required = ["slug", "name", "price", "image", "description"]
    for r in required:
        if r not in cols:
            raise SystemExit(f"Missing column in Excel: '{r}'")

    # Tolerate either "sales price" or "sale price"
    sale_col_key = "sales price" if "sales price" in cols else ("sale price" if "sale price" in cols else None)

    out = []
    for _, row in df.iterrows():
        slug = str(row[cols["slug"]]).strip()
        name = str(row[cols["name"]]).strip()

        price = money_or_none(row[cols["price"]])
        sale = money_or_none(row[cols[sale_col_key]]) if sale_col_key else None

        image = "" if pd.isna(row[cols["image"]]) else str(row[cols["image"]]).strip()
        desc  = "" if pd.isna(row[cols["description"]]) else str(row[cols["description"]]).strip()

        # Bullet points are optional; semicolon-separated if present
        bullets = []
        if "bullet points" in cols:
            bullets_raw = "" if pd.isna(row[cols["bullet points"]]) else str(row[cols["bullet points"]])
            bullets = [b.strip() for b in bullets_raw.split(";") if b.strip()]

        # NEW: actions via actionType (+ optional links)
        action_type   = ""
        contact_link  = ""
        checkout_link = ""
        if "actiontype" in cols:
            action_type = str(row[cols["actiontype"]]).strip().lower()
        elif "action type" in cols:
            action_type = str(row[cols["action type"]]).strip().lower()

        if "contactlink" in cols:
            contact_link = "" if pd.isna(row[cols["contactlink"]]) else str(row[cols["contactlink"]]).strip()
        elif "contact link" in cols:
            contact_link = "" if pd.isna(row[cols["contact link"]]) else str(row[cols["contact link"]]).strip()

        if "checkoutlink" in cols:
            checkout_link = "" if pd.isna(row[cols["checkoutlink"]]) else str(row[cols["checkoutlink"]]).strip()
        elif "checkout link" in cols:
            checkout_link = "" if pd.isna(row[cols["checkout link"]]) else str(row[cols["checkout link"]]).strip()

        out.append({
            "slug": slug,
            "name": name,
            "price": price,            # number or null
            "salePrice": sale,         # number or null
            "image": image,            # path/URL to image OR video OR YouTube/Vimeo
            "description": desc,
            "bullets": bullets,        # array (optional)
            "actionType": action_type, # '', 'contact', 'checkout', 'both'
            "contactLink": contact_link,
            "checkoutLink": checkout_link,
        })

    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"Wrote {OUT_JSON} with {len(out)} services")

if __name__ == "__main__":
    main()
