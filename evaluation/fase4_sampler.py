import os
import random
import shutil
import glob
import json

def create_testset(sample_size=10, seed=42):
    pool_dir = os.path.join("data", "satellietbeelden_test_pool")
    test_dir = os.path.join("data", "satellietbeelden_test")

    # Controleer of de pool directory bestaat anders aanmaken en gebruiker informeren
    if not os.path.exists(pool_dir):
        os.makedirs(pool_dir, exist_ok=True)
        print(f"Pool directory {pool_dir} is aangemaakt. Voeg hier satellietbeelden toe voordat je dit script runt.")
        return

    os.makedirs(test_dir, exist_ok=True)

    # Controleer of het gevraagde aantal afbeeldingen al bestaat in de test directory
    existing_images = glob.glob(os.path.join(test_dir, "*.png"))
    if len(existing_images) >= sample_size:
        print(f"Er zijn al {len(existing_images)} afbeeldingen in {test_dir}.")
        return
    
    # Sorteer de afbeeldingen op naam om consistentie te garanderen
    all_images = sorted(glob.glob(os.path.join(pool_dir, "*.png")))

    if len(all_images) < sample_size:
        print(f"Niet genoeg afbeeldingen gevonden in {pool_dir} voor sample size {sample_size}.")
        return
    
    # Sample de afbeeldingen op basis van de seed
    random.seed(seed)
    sampled_images = random.sample(all_images, sample_size)
    sampled_images.sort()  # Sorteer de geselecteerde afbeeldingen op naam voor makkelijkere handmatige classificatie

    print(f"Selecteren van {sample_size} afbeeldingen vanuit {len(all_images)} beschikbare afbeeldingen (Seed: {seed}).")

    json_path = os.path.join(test_dir, "ground_truth.json")
    ground_truth_dic = {}

    # Controleer of er al een bestaand ground_truth.json bestand is en laad het indien aanwezig
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            try:
                ground_truth_dic = json.load(f)
                print(f"Bestaand ground_truth.jsongevonden met {len(ground_truth_dic)} bestanden. Nieuwe bestanden zullen worden toegevoegd.")
            except json.JSONDecodeError:
                print(f"WAARSCHUWING: ground_truth.json was corrupt of leeg. Een nieuw bestand zal worden gemaakt.")

    # Voeg de nieuwe afbeeldingen toe aan de testset en update ground_truth_dic
    new_images_added = 0

    for path in sampled_images:
        filename = os.path.basename(path)
        dest_path = os.path.join(test_dir, filename)

        if not os.path.exists(dest_path):
            shutil.copy2(path, dest_path)
        
        if filename not in ground_truth_dic:
            ground_truth_dic[filename] = {
                "military_count": 0,
                "civilian_count": 0
            }
            new_images_added += 1

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(ground_truth_dic, f, indent=4)

    print(f"{new_images_added} nieuwe afbeeldingen toegevoegd.")
    print(f"Totaal aantaal afbeeldingen in testset: {sample_size}.")

if __name__ == "__main__":
    create_testset(50)