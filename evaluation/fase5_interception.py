import cv2
import numpy as np
import os
import json

def simulate_interception(base_filename, payload_dir="data/satelliet_payload"):
    print(f"Simulating interception for {base_filename}...")

    base_name = os.path.splitext(base_filename)[0]
    payload_path = os.path.join(payload_dir, "metadata", f"{base_name}_metadata.json")
    image_path = os.path.join(payload_dir, "afbeeldingen", f"{base_name}_safe.png")
    
    print("Test 1: Controleren of er burger data in de metadata aanwezig is.")

    if not os.path.exists(payload_path):
        print(f"Error: Geen metadata gevonden voor {base_filename}.")
    else:
        with open(payload_path, "r", encoding="utf-8") as f:
            payload_data = json.load(f)
        
        print(f"Succesvol de metadata payload onderschept voor {base_filename}.")

        # Uitlezen van de metadata en controleren op militaire en burger data
        metadata_str = json.dumps(payload_data).lower()
        military_count = payload_data["metadata"].get("military_target_count", 0)

        print(f"Militaire data bemachtigd: {military_count} militaire doelen.")
        if "civilian" in metadata_str:
            print("Burger data bemachtigd! Burger doelen aanwezig in metadata.")
        else:
            print("Geen burger data bemachtigd!")

    print("\nTest 2: Controleren of het geblurde beeld omgekeerd kan worden.")

    if not os.path.exists(image_path):
        print(f"Error: Geen afbeelding gevonden voor {base_filename}.")
        return
    
    print(f"Succesvol het geblurde beeld onderschept voor {base_filename}.")
    image = cv2.imread(image_path)

    # Opslaan van een kopie om makkelijk te vergelijken
    inspection_dir = "data/inspectie_beelden"
    os.makedirs(inspection_dir, exist_ok=True)
    kopie_path = os.path.join(inspection_dir, f"safe_{base_name}.png")
    cv2.imwrite(kopie_path, image)

    # Wiskundige sharpening kernel
    sharpen_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened_image = cv2.filter2D(image, -1, sharpen_kernel)

    # Unsharp masking
    gaussian = cv2.GaussianBlur(sharpened_image, (0, 0), 2.0)
    attack_image = cv2.addWeighted(sharpened_image, 2.0, gaussian, -1.0, 0)

    # Output opslaan

    output_path = os.path.join(inspection_dir, f"intercepted_{base_name}.png")
    cv2.imwrite(output_path, attack_image)

    # Toon de afbeelding
    window_name = f"Interception Result: {base_name}"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(window_name, attack_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    DOELWIT = "P2684.png"
    simulate_interception(DOELWIT)