import os
import openai
import json
from tqdm import tqdm
from pydantic import BaseModel, Field
from typing import Literal, Optional

from assemble.input import assemble_input 

GPT_MODEL_NAME = 'gpt-4.1-mini-2025-04-14'
refactoring_type = 'Extract Method'

test_dataset_path = "../data/python_test.json"  # Define test dataset path here

print(f"Loading test dataset from {test_dataset_path}...")
test_dataset = json.load(open(test_dataset_path, 'r'))
print(f"Found {len(test_dataset)} samples in the test set.")

rTypes = ['Extract Method', 'Inline Method', 'Rename Variable', 'Extract Variable', 'Inline Variable']

try:
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
except TypeError:
    print("Error: OPENAI_API_KEY environment variable not set.")
    exit()

def run_evaluation(refactoring_type: str):
    output_results_path = f"../results/gpt4.1mini/zeroshot/zeroshot_python_{refactoring_type.replace(' ', '_').lower()}.json" # Define output path here

    results = []

    class RefactoringResponse(BaseModel):
        """Defines the structured output schema for code refactoring analysis."""
        Refactor: bool = Field(..., description=f"Whether the code change is a refactoring of {refactoring_type}."),
        Explanation: str = Field(..., description="A brief explanation of the reasoning behind the decision.")

    print(f"\nStarting evaluation with model: {GPT_MODEL_NAME} ...")
    for sample in tqdm(test_dataset):
        
        # --- Build Prompts ---
        role_definition = "You are an expert code analyst specializing in identifying and classifying code refactorings."
        main_instruction = (
        f"Analyze the user's code change and determine whether it constitutes a refactoring of {refactoring_type}. "
        "Your response MUST strictly conform to the provided structure:\n\n"
        "{\n"
        '  "Refactor": true or false,\n'
        '  "Explanation": "A brief, factual description of why the change is or isn\'t a refactoring, no additional interpretations or comments."\n'
        "}"
        )

        system_prompt = f'{role_definition}\n' + \
                        f'{main_instruction}'

        user_prompt = f"Determine whether the following code change is a {refactoring_type} refactoring.\n\n" + \
                        f"{assemble_input(sample)}"

        ground_truth = sample['refactoring_type'] if sample['label'] == 'positive' else 'None Refactoring'

        # --- Call modern OpenAI API with Pydantic parsing ---
        try:
            response = client.responses.parse(
                model=GPT_MODEL_NAME,
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                text_format=RefactoringResponse,

                temperature=0.0,
                top_p=1.0,
                max_output_tokens=512
            )
            
            prediction_obj = response.output_parsed
            prediction = prediction_obj.model_dump()

        except Exception as e:
            print(f"An API or validation error occurred: {e}")
            prediction = {}
        
        results.append({
            "id": sample['id'],
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "ground_truth": ground_truth,
            "prediction_parsed": prediction,
        })


    os.makedirs(os.path.dirname(output_results_path), exist_ok=True)
    with open(output_results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nDetailed results saved to {output_results_path}")

if __name__ == "__main__":
    for item in rTypes:
        run_evaluation(item)
