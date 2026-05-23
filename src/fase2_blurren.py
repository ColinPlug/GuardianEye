import cv2
import numpy as np
import os

def apply_blur(image_path, civiele_doelen, output_dir="data/veilige_beelden"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    img = cv2.imread(image_path)

    if img is None:
        raise FileNotFoundError(f"Afbeelding niet gevonden: {image_path}")
    
    # Maak een kopie van de originele afbeelding om te bewerken
    safe_img = img.copy()

    for doel in civiele_doelen:
        coords = doel.get('coords', [])

        if len(coords) == 8:
            pts = np.array(coords, dtype=np.int32).reshape((-1, 1, 2))

            x, y, w, h = cv2.boundingRect(pts)

            # Zorg ervoor dat de coördinaten binnen de grenzen van de afbeelding blijven
            x_min, y_min = max(0, x), max(0, y)
            x_max, y_max = min(img.shape[1], x + w), min(img.shape[0], y + h)

            # Extract het gebied van interesse (ROI) en pas de blur toe
            roi = safe_img[y_min:y_max, x_min:x_max]

            if roi.size == 0:
                continue

            blurred_roi = cv2.GaussianBlur(roi, (51, 51), 0)
            
            # Maak een masker voor het gebied van interesse
            local_mask = np.zeros(roi.shape[:2], dtype=np.uint8)

            shifted_pts = pts - [x_min, y_min]
            cv2.fillPoly(local_mask, [shifted_pts], 255)
            
            # Gebruik het masker om alleen het civiele object te blurren
            mask_3d = local_mask[:, :, np.newaxis]
            safe_img[y_min:y_max, x_min:x_max] = np.where(mask_3d == 255, blurred_roi, roi)
    
    filename = os.path.basename(image_path)
    output_path = os.path.join(output_dir, f"safe_{filename}")
    cv2.imwrite(output_path, safe_img)

    return output_path

def visualize_results(image_path, miliaire_doelen, civiele_doelen):
    # Laad de afbeelding
    img = cv2.imread(image_path)

    return None