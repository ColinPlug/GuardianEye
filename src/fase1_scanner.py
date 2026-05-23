import os
from ultralytics import YOLO

# Laad het YOLO-model
print("Laden van het AI-model... (Kan de eerste keer even duren)")
model = YOLO("yolo26n-obb.pt") 

# Definieer de klassen die als militair of civiel worden beschouwd
MILITARY_IDS = [0, 1, 2, 7, 8, 11]
CIVILIAN_IDS = [3, 4, 5, 6, 9, 10, 12, 13, 14]


def scan_image(image_path):

    print(f"\nFoto analyseren: {image_path}")

    results = model(image_path, verbose=False)

    military_targets = []
    civilian_targets = []

    if results[0].obb is not None:
        for box in results[0].obb:
            class_id = int(box.cls.item())

            coords = box.xyxyxyxy.tolist()[0]
            if class_id in MILITARY_IDS:
                military_targets.append({"id": class_id, "coords": coords})
            elif class_id in CIVILIAN_IDS:
                civilian_targets.append({"id": class_id, "coords": coords})

    print("\n---GuardianEye Resultaten---")
    print(f"Aantal militaire objecten (Behouden): {len(military_targets)}")
    print(f"Aantal civiele objecten (Klaar voor blurren): {len(civilian_targets)}")

    return military_targets, civilian_targets

if __name__ == "__main__":
    # Test de scanner met een voorbeeldafbeelding
    TEST_IMAGE = os.path.join("data", "satellietbeelden", "P0000.png")
    military, civilians = scan_image(TEST_IMAGE)

    if civilians:
        print(f"Voorbeeld van een te blurren civiel object (ID {civilians[0]['id']})")
        print(f"Coördinaten: {civilians[0]['coords']}")