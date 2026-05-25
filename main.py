import os
import glob
import json
import shutil
import time
import cv2

try:
    from src.fase1_scanner import scan_image
    from src.fase2_blurring import blur_img
except ModuleNotFoundError:
    print("ERROR: kan .py bestanden niet importeren.")
    exit(0)

# Setup functie om benodigde directories aan te maken
def setup(base_path="data"):
    input_dir = os.path.join(base_path, "satellietbeelden")
    payload_dir = os.path.join(base_path, "satelliet_payload")
    images_dir = os.path.join(payload_dir, "afbeeldingen")
    metadata_dir = os.path.join(payload_dir, "metadata")

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
    
    print(f"Batch-processing voor {len(image_paths)} beelden gestart.")

    # Benchmarking variabelen
    total_latency_inference = 0
    total_latency_blurring = 0
    total_latency_io_write = 0
    total_images = len(image_paths)

    # Start timer
    start_pipeline = time.perf_counter()

    for path in image_paths:
        filename = os.path.basename(path)
        base_name = os.path.splitext(filename)[0]
        safe_img_filename = f"{base_name}_safe.png"
        print(f"Verwerken van beeld: {filename}")
        
        # Laad de afbeelding in als numpy array
        img_array = cv2.imread(path)

        # Fase 1: Scannen op militaire doelen
        t_start_inference = time.perf_counter()
        military_targets, civilian_targets = scan_image(img_array, filename)
        t_end_inference = time.perf_counter()
        total_latency_inference += (t_end_inference - t_start_inference)

        # Fase 2: Anonimiseren van civiele doelen als die gevonden zijn
        t_start_blurring = time.perf_counter()
        if civilian_targets:
            final_out = blur_img(img_array, filename, civilian_targets, output_dir=images_dir)
        else:
            final_out = os.path.join(images_dir, safe_img_filename)
            shutil.copy2(path, final_out)
        t_end_blurring = time.perf_counter()
        total_latency_blurring += (t_end_blurring - t_start_blurring)

        # Fase 3: Exporteren van metadata
        t_start_io_write = time.perf_counter()
        export_metadata(filename, military_targets,  metadata_dir)
        t_end_io_write = time.perf_counter()
        total_latency_io_write += (t_end_io_write - t_start_io_write)

    # Eind timer
    t_end_pipeline = time.perf_counter()
    total_pipeline_time = t_end_pipeline - start_pipeline
    fps = total_images / total_pipeline_time if total_pipeline_time > 0 else 0

    # Benchmarking resultaten
    print("\n--- Benchmarking Resultaten ---")
    print(f"Totale beelden verwerkt: {total_images}")
    print(f"Totale pipeline tijd: {total_pipeline_time:.4f} seconden")
    print(f"Gemiddelde fps: {fps:.2f} beelden/sec")
    print("-" * 60)
    print(f"Fase 1 (Inference) gemiddelde latency per beeld: {total_latency_inference / total_images:.4f} sec")
    print(f"Fase 2 (Blurring) gemiddelde latency per beeld: {total_latency_blurring / total_images:.4f} sec")
    print(f"Fase 3 (I/O Write) gemiddelde latency per beeld: {total_latency_io_write / total_images:.4f} sec")
    print("-" * 60)

    # Exporteren van latency resultaten naar JSON
    latency_data = {
        "total_images": total_images,
        "total_pipeline_time": total_pipeline_time,
        "average_latency_inference": total_latency_inference / total_images,
        "average_latency_blurring": total_latency_blurring / total_images,
        "average_latency_io_write": total_latency_io_write / total_images
    }

    latency_export_path = os.path.join("data", "latency_results.json")
    with open(latency_export_path, "w", encoding="utf-8") as f:
        json.dump(latency_data, f, indent=4)

if __name__ == "__main__":
    batch_processing()