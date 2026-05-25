import os
import sys
import json
import glob
import cv2

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
if root_dir not in sys.path:
    sys.path.append(root_dir)

try:
    from src.fase1_scanner import scan_image
except ModuleNotFoundError:
    print("ERROR: kan fase1_scanner niet importeren.")
    exit(0)

def calculate_metrics(tp, fp, fn):
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    return precision, recall, f1_score

def evaluate_model(test_dir="data/satellietbeelden_test", ground_truth_filename="ground_truth.json"):
    gt_path = os.path.join(test_dir, ground_truth_filename)

    if not os.path.exists(gt_path):
        print(f"ERROR: Ground truth bestand niet gevonden op {gt_path}")
        return

    with open(gt_path, "r", encoding="utf-8") as f:
        ground_truth = json.load(f)

    image_paths = glob.glob(os.path.join(test_dir, "*.png"))
    if not image_paths:
        print(f"ERROR: Geen testbeelden gevonden in {test_dir}.")
        return
    
    print(f"Evaluatie gestart voor {len(image_paths)} testbeelden.")

    # Threshold voor geclutterede beelden om te stress-testen
    DENSE_THRESHOLD = 300

    # Initializeer metrics
    metrics = {
        "baseline": {
            "military_targets": {"tp": 0, "fp": 0, "fn": 0},
            "civilian_targets": {"tp": 0, "fp": 0, "fn": 0},
            "count": 0
        },
        "dense": {
            "military_targets": {"tp": 0, "fp": 0, "fn": 0},
            "civilian_targets": {"tp": 0, "fp": 0, "fn": 0},
            "count": 0
        }
    }

    # Export metrics voor visualisatie
    export_data = {
        "actual_mil": [],
        "pred_mil": [],
        "actual_civ": [],
        "pred_civ": []
    }

    for path in image_paths:
        filename = os.path.basename(path)

        # Check of de afbeelding in de ground truth staat
        if filename not in ground_truth:
            print(f"Waarschuwing: {filename} niet gevonden in ground truth, wordt overgeslagen.")
            continue
        
        gt_military = ground_truth[filename].get("military_count", 0)
        gt_civilian = ground_truth[filename].get("civilian_count", 0)

        total_gt = gt_military + gt_civilian
        subset = "dense" if total_gt >= DENSE_THRESHOLD else "baseline"
        metrics[subset]["count"] += 1

        img_array = cv2.imread(path)
        pred_military, pred_civilian = scan_image(img_array, image_name=filename)

        yolo_military = len(pred_military)
        yolo_civilian = len(pred_civilian)

        # Voeg toe aan export data
        export_data["actual_mil"].append(gt_military)
        export_data["pred_mil"].append(yolo_military)
        export_data["actual_civ"].append(gt_civilian)
        export_data["pred_civ"].append(yolo_civilian)

        # Update militaire target metrics
        metrics[subset]["military_targets"]["tp"] += min(gt_military, yolo_military)
        metrics[subset]["military_targets"]["fp"] += max(0, yolo_military - gt_military)
        metrics[subset]["military_targets"]["fn"] += max(0, gt_military - yolo_military)

        # Update burger target metrics
        metrics[subset]["civilian_targets"]["tp"] += min(gt_civilian, yolo_civilian)
        metrics[subset]["civilian_targets"]["fp"] += max(0, yolo_civilian - gt_civilian)
        metrics[subset]["civilian_targets"]["fn"] += max(0, gt_civilian - yolo_civilian)

    # Bereken eind metrics voor baseline subset
    baseline_military_precision, baseline_military_recall, baseline_military_f1 = calculate_metrics(metrics["baseline"]["military_targets"]["tp"], metrics["baseline"]["military_targets"]["fp"], metrics["baseline"]["military_targets"]["fn"])

    baseline_civilian_precision, baseline_civilian_recall, baseline_civilian_f1 = calculate_metrics(metrics["baseline"]["civilian_targets"]["tp"], metrics["baseline"]["civilian_targets"]["fp"], metrics["baseline"]["civilian_targets"]["fn"])

    print(f"\nEvaluatieresultaten Baseline ({metrics['baseline']['count']} beelden, < {DENSE_THRESHOLD})")
    print(f"Precision -> Militair: {baseline_military_precision:.2f} | Burger: {baseline_civilian_precision:.2f}")
    print(f"Recall    -> Militair: {baseline_military_recall:.2f} | Burger: {baseline_civilian_recall:.2f}")
    print(f"F1-Score  -> Militair: {baseline_military_f1:.2f} | Burger: {baseline_civilian_f1:.2f}")

    # Bereken eind metrics voor dense subset
    dense_military_precision, dense_military_recall, dense_military_f1 = calculate_metrics(metrics["dense"]["military_targets"]["tp"], metrics["dense"]["military_targets"]["fp"], metrics["dense"]["military_targets"]["fn"])

    dense_civilian_precision, dense_civilian_recall, dense_civilian_f1 = calculate_metrics(metrics["dense"]["civilian_targets"]["tp"], metrics["dense"]["civilian_targets"]["fp"], metrics["dense"]["civilian_targets"]["fn"])

    print(f"\nEvaluatieresultaten Extreme Density Test ({metrics['dense']['count']} beelden, >= {DENSE_THRESHOLD})")
    print(f"Precision -> Militair: {dense_military_precision:.2f} | Burger: {dense_civilian_precision:.2f}")
    print(f"Recall    -> Militair: {dense_military_recall:.2f} | Burger: {dense_civilian_recall:.2f}")
    print(f"F1-Score  -> Militair: {dense_military_f1:.2f} | Burger: {dense_civilian_f1:.2f}")

    # Bereken de MAE en exporteer de data voor visualisatie
    n_images = len(export_data["actual_mil"])

    mae_military = sum(abs(a - p) for a, p in zip(export_data["actual_mil"], export_data["pred_mil"])) / n_images
    mae_civilian = sum(abs(a - p) for a, p in zip(export_data["actual_civ"], export_data["pred_civ"])) / n_images

    print(f"\nMean Absolute Error (Militair): {mae_military:.2f}")
    print(f"Mean Absolute Error (Burger): {mae_civilian:.2f}")

    export_path = os.path.join(test_dir, "evaluation_results.json")
    with open(export_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=4)
    
if __name__ == "__main__":
    evaluate_model()