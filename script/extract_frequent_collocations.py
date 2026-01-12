import csv

INPUT_FILE = "list-of-collocations.csv"
OUTPUT_FILE = "frequent_collocations.csv"


def extract_collocations():
    results = []
    current_right = None

    with open(INPUT_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            right = (row.get("right") or "").strip().lower()
            left_raw = (row.get("left") or "").strip()

            # Update current right word if present
            if right:
                current_right = right

            if not current_right or not left_raw:
                continue

            # Split left cell by newline (important fix)
            left_items = []
            for item in left_raw.splitlines():
                if item.strip():
                    if "N" in item.strip():
                        left_items.append(item.strip())
                    else:
                        left_items.append(item.strip().lower())          

            for left in left_items:
                results.append({
                    "left": left,
                    "right": current_right
                })

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["left", "right"])
        # writer.writeheader()
        writer.writerows(results)

    print(f"Extracted {len(results)} collocations to {OUTPUT_FILE}")


if __name__ == "__main__":
    extract_collocations()

