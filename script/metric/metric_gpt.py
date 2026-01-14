import json
import os
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix

metric_output_path = '../results/gpt4.1mini/metrics'

language = 'python'
prompt_type = 'sarp' # 'zeroshot', 'fewshot', 'gold', 'sarp'

result_path = f'../results/gpt4.1mini/{prompt_type}'

rTypes = ['Extract Method', 'Inline Method', 'Rename Variable', 'Extract Variable', 'Inline Variable']

def metric_gpt(rType, results, metric_output_path):
    metric_file = os.path.join(metric_output_path, f'{prompt_type}_{language}_{rType.replace(" ", "_").lower()}_metric.txt')

    y_true = []
    y_pred = []

    wrong_type_counts = {}

    for result in results:
        ground_truth = result.get("ground_truth", "").strip().lower()
        prediction_parsed = result.get("prediction_parsed", {})
        predicted_refactor = prediction_parsed.get("Refactor", False)

        is_target_type = (ground_truth == rType.lower())
        y_true.append(1 if is_target_type else 0)
        y_pred.append(1 if predicted_refactor else 0)

        if ground_truth != rType.lower() and predicted_refactor:
            wrong_type = ground_truth.title()
            if wrong_type in wrong_type_counts:
                wrong_type_counts[wrong_type] += 1
            else:
                wrong_type_counts[wrong_type] = 1

    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average='binary', zero_division=0
    )

    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0,1]).ravel()

    with open(metric_file, 'w') as f:
        f.write(f'Refactoring Type: {rType}\n')
        f.write(f'Precision: {precision:.4f}\n')
        f.write(f'Recall:    {recall:.4f}\n')
        f.write(f'F1 Score:  {f1:.4f}\n')
        f.write(f'Total Samples: {len(results)}\n')
        f.write(f'True Positives:  {tp}\n')
        f.write(f'False Positives: {fp}\n')
        f.write(f'False Negatives: {fn}\n')

        if wrong_type_counts:
            f.write("\nMisclassified Other Types as This Type:\n")
            for wrong_type, count in wrong_type_counts.items():
                f.write(f"- {wrong_type}: {count}\n")

    print(f'[Metric Saved] {metric_file}')

if __name__ == '__main__':
    os.makedirs(metric_output_path, exist_ok=True)
    for rType in rTypes:
        output_results_path = os.path.join(result_path, f'{prompt_type}_{language}_{rType.replace(" ", "_").lower()}.json')
        with open(output_results_path, 'r') as f:
            results = json.load(f)
        metric_gpt(rType, results, metric_output_path)