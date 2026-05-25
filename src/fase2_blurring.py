import cv2
import numpy as np
import os

# Functie die image omzet in een geblurde image binnen de bounding box
def blur_img(image_array, filename, civilian_targets, output_dir="data/veilige_beelden"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Maak een kopie van de originele afbeelding om te bewerken
    safe_img = image_array.copy()

    for target in civilian_targets:
        coords = target.get('coords', [])

        pts = np.array(coords, dtype=np.int32)
        if pts.size == 8:
            pts = pts.reshape((-1, 1, 2))

            x, y, w, h = cv2.boundingRect(pts)

            # Zorg ervoor dat de coördinaten binnen de grenzen van de afbeelding blijven
            x_min, y_min = max(0, x), max(0, y)
            x_max, y_max = min(image_array.shape[1], x + w), min(image_array.shape[0], y + h)

            # Extract het gebied van interesse (ROI) en pas de blur toe
            roi = safe_img[y_min:y_max, x_min:x_max]

            if roi.size == 0:
                continue

            blurred_roi = cv2.GaussianBlur(roi, (91, 91), 0)
            
            # Maak een masker voor het gebied van interesse
            local_mask = np.zeros(roi.shape[:2], dtype=np.uint8)
            
            # Shift de coördinaten van het burger object naar de lokale coördinaten van de ROI
            shifted_pts = pts - [x_min, y_min]
            cv2.fillPoly(local_mask, [shifted_pts], 255)
            
            # Gebruik het masker om alleen het burger object te blurren
            mask_3d = local_mask[:, :, np.newaxis]
            safe_img[y_min:y_max, x_min:x_max] = np.where(mask_3d == 255, blurred_roi, roi)
    
    # Sla de veilige afbeelding op
    base_name = os.path.splitext(filename)[0]
    output_path = os.path.join(output_dir, f"{base_name}_safe.png")
    cv2.imwrite(output_path, safe_img)

    return output_path

def visualize_results(image_array, filename, military_targets, civilian_targets, output_dir="data/inspectie_beelden"):
    # Zorg ervoor dat de output directory bestaat
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Laad de afbeelding als kopie om te bewerken
    img = image_array.copy()

    # Visualiseer militaire doelen in rood
    for target in military_targets:
        pts = np.array(target["coords"], np.int32)
        cv2.polylines(img, [pts], isClosed=True, color=(0, 0, 255), thickness=2)
        cv2.putText(img, f"MIL {target['id']}", tuple(pts[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
    # Visualiseer burger doelen in blauw
    for target in civilian_targets:
        pts = np.array(target["coords"], np.int32)
        cv2.polylines(img, [pts], isClosed=True, color=(255, 0, 0), thickness=2)
        cv2.putText(img, f"CIV {target['id']}", tuple(pts[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Sla de inspectie afbeelding op
    base_name = os.path.splitext(filename)[0]
    output_path = os.path.join(output_dir, f"inspectie_{base_name}.png")
    cv2.imwrite(output_path, img)
    print(f"Inspectie afbeelding opgeslagen in: {output_path}")

    # Toon de afbeelding (Uitgeschakeld voor Docker)
    # window_name = "GuardianEye - Privacy vs. Bruikbaarheid Validatie"
    # cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    # print("Beeld wordt weergegeven. Druk op een toets om door te gaan...")
    # cv2.imshow(window_name, img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        from fase1_scanner import scan_image
    except ImportError:
        print("ERROR: kan fase1_scanner.py niet importeren. Zorg ervoor dat het bestand in dezelfde directory staat.")
        exit()
    
    TEST_IMAGE = os.path.join("data", "satellietbeelden", "P0139.png")

    if os.path.exists(TEST_IMAGE):
        print(f"\nStarten met GuardianEye test op {TEST_IMAGE}")

        img_array = cv2.imread(TEST_IMAGE)
        filename = os.path.basename(TEST_IMAGE)

        # Stap 1: Scan de afbeelding om militaire en burger doelen te identificeren
        military, civilians = scan_image(img_array, image_name=filename)

        # Stap 2: Anonimiseren
        print(f"\nToepassen van Privacy Filter op {len(civilians)} burger doelen...")
        veilige_image_path = blur_img(img_array, filename, civilians)
        print(f"Veilige afbeelding opgeslagen in: {veilige_image_path}")

        # Stap 3: Visuele inspectie van de resultaten
        visualize_results(img_array, filename, military, civilians)
    
    else:
        print(f"ERROR: Testafbeelding niet gevonden op {TEST_IMAGE}. Zorg ervoor dat het bestand bestaat.")