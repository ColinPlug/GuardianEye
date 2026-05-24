import os
import json
import matplotlib.pyplot as plt

def gen_visualization(test_dir="data/satellietbeelden_test", data_file="evaluation_results.json"):
    data_path = os.path.join(test_dir, data_file)

    if not os.path.exists(data_path):
        print(f"ERROR: Evaluatie data kan niet worden gevonden op {data_path}.")

    # Laad de data
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    actual_mil = data["actual_mil"]
    pred_mil = data["pred_mil"]
    actual_civ = data["actual_civ"]
    pred_civ = data["pred_civ"]

    print("Visualisatie creëren.")

    plt.figure(figsize=(12,6))

    # Subplot militair
    plt.subplot(1, 2, 1)
    plt.scatter(actual_mil, pred_mil, color="red", alpha=0.6, edgecolors="black", label="Afbeelding met militaire doelen")

    max_val_mil = max(max(actual_mil, default=0), max(pred_mil, default=0))
    if max_val_mil == 0: max_val_mil = 10

    plt.plot([0, max_val_mil], [0, max_val_mil], "k--", label="Ideale prestatie")
    plt.title("Militaire doelen: Ground Truth vs. YOLO", fontsize=12)
    plt.xlabel("Daadwerkelijk aantal doelen")
    plt.ylabel("Door YOLO gedetecteerd aantal doelen")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)

    # Subplot burger
    plt.subplot(1, 2, 2)
    plt.scatter(actual_civ, pred_civ, color="blue", alpha=0.6, edgecolors="black", label="Afbeelding met burger doelen")

    max_val_civ = max(max(actual_civ, default=0), max(pred_civ, default=0))
    if max_val_civ == 0: max_val_civ = 10

    plt.plot([0, max_val_civ], [0, max_val_civ], "k--", label="Ideale prestatie")
    plt.title("Burger doelen: Ground Truth vs. YOLO", fontsize=12)
    plt.xlabel("Daadwerkelijk aantal doelen")
    plt.ylabel("Door YOLO gedetecteerd aantal doelen")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)

    # Directory voor output aanmaken
    output_dir = "visuals"
    os.makedirs(output_dir, exist_ok=True)

    # Plot opslaan en tonen
    plt.tight_layout()
    output_img = os.path.join(output_dir, "scatter_actual_vs_pred.png")
    plt.savefig(output_img, dpi=300)

    plt.show()

if __name__ == "__main__":
    gen_visualization()