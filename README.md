# Replication Package

This is the replication package of "Evaluating Cross-Language Transfer for Refactoring Detection with Large Language Models".

Refactoring types considered:
- **Extract Method**
- **Inline Method**
- **Rename Variable**
- **Extract Variable**
- **Inline Variable**

## Environment Setup
Required Python: **3.10+**.

1. Clone / download the repository.
2. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
1. Install dependencies:
```bash
pip install -r script/requirements.txt
```
1. Set your OpenAI API key (required for all evaluation scripts):
```bash
export OPENAI_API_KEY=YOUR_KEY_HERE
```

## Running Evaluations
Change into the script directory first:
```bash
cd script
```
Each evaluation script iterates over all refactoring types and writes one JSON file per type.

Zero-shot:
```bash
python eval_gpt_p.py
```
Cross-language Few-shot (Java examples):
```bash
python eval_gpt_p_fewshot.py
```
Native Few-shot (Python examples, "gold"):
```bash
python eval_gpt_p_gold.py
```
Cross-language Few-shot with descriptions ("sarp"):
```bash
python eval_gpt_p_sarp.py
```

## Output Files
Location root: `results/gpt4.1mini/`

For each prompt strategy and refactoring type a file is generated:
```text
<strategy>/<strategy>_python_<refactoring_type>.json
```
Example:
```text
results/gpt4.1mini/zeroshot/zeroshot_python_extract_method.json
```
Each JSON entry includes:
- `id`: sample id
- `system_prompt` / `user_prompt`: assembled prompts
- `ground_truth`: expected refactoring type or `None Refactoring`
- `prediction_parsed`: structured model output `{ Refactor, Explanation }`

## Computing Metrics
After running one strategy:
```bash
python metric/metric_gpt.py
```
Configuration variables at top of `metric/metric_gpt.py`:
- `prompt_type`: set to one of `zeroshot` | `fewshot` | `gold` | `sarp` before running
- `language`: `python`

Outputs written to:
```text
results/gpt4.1mini/metrics/<prompt_type>_python_<refactoring_type>_metric.txt
```
Containing precision, recall, F1, confusion matrix components, misclassification counts.

## Dataset
Test dataset: `data/python_test.json`. Each sample encodes before/after code fragments plus refactoring label fields consumed by `assemble_input()`.

## Appendix

### 1. [F1-Scores for refactoring detection by prompt strategy using GPT-4.1-mini.Bold values indicate the highest F1 score for each refactoring type. Values in brackets are Precision and Recall, respectively.](appendix/table1.pdf)

### 2. Descriptions for each refactoring type
| Refactoring Type | Description |
|------------------|-------------|
| Extract Method | This refactoring occurs when a segment of code is moved from an existing method (the `original_method`) and placed into a new, separate method (the `new_method`). The `original_method` is then modified to include a function call to this `new_method` in place of the removed code block. |
| Inline Method | This refactoring is the reverse of 'Extract Method.' It occurs when a method's call (the `caller`) is replaced by the *entire body* of the method being called (the `callee`). This is done to eliminate the indirection of the method call. Often, the `callee` method definition is then removed if it's no longer used. |
| Rename Variable | This refactoring involves changing the name of an identifier (such as a local variable, a function parameter, or a class field) to a new name. The change must be applied consistently across its entire scope of use. The surrounding code logic and structure remain identical. |
| Extract Variable | This refactoring involves taking a complex expression that is part of a larger statement and assigning it to a new, temporary local variable. This new variable, which usually has a descriptive name, is then used in the original statement, making the code easier to read and debug. |
| Inline Variable | This refactoring is the reverse of 'Extract Variable'. It occurs when a variable, often a temporary one, is replaced by the full expression it holds. The original variable definition is then removed if it is no longer needed. |
