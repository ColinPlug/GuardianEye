import json
import os

# Leest ground_truth.json, sorteert de entries op bestandsnaam en schrijft het gesorteerde resultaat terug naar het bestand.
def sort_ground_truth():
    json_path = os.path.join("data", "satellietbeelden_test", "ground_truth.json")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    sorted_data = dict(sorted(data.items()))

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(sorted_data, f, indent=4)
    
    print("Ground truth JSON is gesorteerd op bestandsnaam.")

if __name__ == "__main__":
    sort_ground_truth()