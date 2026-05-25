import os
import json
import matplotlib.pyplot as plt

def gen_visualization_scatter(test_dir="data/satellietbeelden_test", data_file="evaluation_results.json"):
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

def gen_visualization_latency(data_file="data/latency_results.json"):
    if not os.path.exists(data_file):
        print("ERROR: Bestand met de latency resulaten kan niet worden gevonden.")
        return
    
    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Data voorbereiden
    labels = ["Fase 1: AI Inference", "Fase 2: Blurring", "Fase 3: I/0 Write"]
    sizes = [data["average_latency_inference"], data["average_latency_blurring"], data["average_latency_io_write"]]
    explode = (0.1, 0, 0)

    print("Visualisatie latency creëren.")

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.pie(sizes, explode=explode, labels=labels, autopct="%1.1f%%", startangle=140)

    ax.axis("equal")

    plt.title("Gemiddelde Latency Verdeling per Fase", fontsize=14, pad=20, fontweight="bold")

    info_text = (f"Latency Benchmarks:\n"
                 f"Inference: {data['average_latency_inference']:.4f} sec\n"
                 f"Blurring: {data['average_latency_blurring']:.4f} sec\n"
                 f"I/O Write: {data['average_latency_io_write']:.4f} sec"
    )

    plt.text(1.2, 0.5, info_text, fontsize=10, bbox=dict(facecolor="white", edgecolor="black", alpha=0.9, boxstyle="round,pad=0.6"), verticalalignment="center")

    # Opslaan visuals
    output_dir = "visuals"
    os.makedirs(output_dir, exist_ok=True)

    plt.tight_layout()
    output_img = os.path.join(output_dir, "pie_latency_distribution.png")
    plt.savefig(output_img, dpi=300)

    plt.show()

if __name__ == "__main__":
    gen_visualization_scatter()
    gen_visualization_latency()