import os
import glob
import json
import shutil

try:
    from src.fase1_scanner import scan_image
    from src.fase2_blurring import blur_img
except ModuleNotFoundError:
    print("ERROR: kan .py bestanden niet importeren.")
    exit(0)

# Setup functie om benodigde directories aan te maken
def setup(base_path="data"):
    input_dir = os.path.join(base_path, "satellietbeelden")
    downlink_dir = os.path.join(base_path, "downlink_payload")
    images_dir = os.path.join(downlink_dir, "images")
    metadata_dir = os.path.join(downlink_dir, "metadata")

    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(metadata_dir, exist_ok=True)

    return input_dir, images_dir, metadata_dir

# Functie om metadata te exporteren naar JSON
def export_metadata(filename, military_targets, metadata_dir):
    base_name = os.path.splitext(filename)[0]
    json_filename = f"{base_name}_metadata.json"
    json_path = os.path.join(metadata_dir, json_filename)

    # Structuur van de metadata payload
    payload = {
        "metadata": {
            "source_image": filename,
            "military_target_count": len(military_targets),
            "edge_processed": True
        },
        "military_targets": military_targets
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=4)

    print(f"Metadata geëxporteerd naar: {json_path}")

def batch_processing():
    input_dir, images_dir, metadata_dir = setup()

    # Haal alle DOTA satellietbeelden op
    image_paths = glob.glob(os.path.join(input_dir, "*.png"))

    if not image_paths:
        print(f"Geen data gevonden in {input_dir}.")
        return
    
    print(f"\n Batch-processing voor {len(image_paths)} beelden gestart.")
    print("-" * 50)

    for path in image_paths:
        filename = os.path.basename(path)
        base_name = os.path.splitext(filename)[0]
        safe_img_filename = f"{base_name}_safe.png"
        print(f"Verwerken van: {filename}")

        # Fase 1: Scannen op militaire doelen
        military_targets, civilian_targets = scan_image(path)

        # Fase 2: Anonimiseren van civiele doelen als die gevonden zijn
        if civilian_targets:
            print (f"{len(civilian_targets)} civiele doelen anonimiseren.")
            
            final_out = blur_img(path, civilian_targets, output_dir=images_dir)

            print(f"Beeld geblurd en opgeslagen op: {final_out}")
        else:
            print("Geen civiele doelen gevonden, geen blurring nodig.")
            final_out = os.path.join(images_dir, safe_img_filename)
            shutil.copy2(path, final_out)
            print(f"Beeld gekopieerd naar: {final_out}")

        # Fase 3: Exporteren van metadata
        export_metadata(filename, military_targets,  metadata_dir)

        print("-" * 50)

    print("\nBatch-processing voltooid.")

if __name__ == "__main__":
    batch_processing()