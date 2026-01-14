import json

fewshot_example_path = "../prompts"

# only python
def assemble_input(json_data):
    input = ""
    match json_data['refactoring_type']:
        case 'Extract Method':
            input = 'Original Code:\n' + \
                    f"{json_data['original_method_before_refactoring']['source_code']}\n" + \
                    '\n' + \
                    'Modified Code:\n' + \
                    f"{json_data['original_method_after_refactoring']['source_code']}\n" + \
                    f"{json_data['newly_extracted_method']['source_code']}\n"
        case 'Inline Method':
            input = 'Original Code:\n' + \
                    f"{json_data['caller_before']['source_code']}\n" + \
                    f"{json_data['inlined_method']['source_code']}\n" + \
                    '\n' + \
                    'Modified Code:\n' + \
                    f"{json_data['caller']['source_code']}\n"
        case 'Rename Variable' | 'Extract Variable' | 'Inline Variable':
            input = 'Original Code:\n' + \
                    f"{json_data['original_code']['source_code']}\n" + \
                    '\n' + \
                    'Modified Code:\n' + \
                    f"{json_data['refactored_code']['source_code']}\n"
        case 'Rename Method':
            input = 'Original Code:\n' + \
                    f"{json_data['original_method']['source_code']}\n" + \
                    '\n' + \
                    'Modified Code:\n' + \
                    f"{json_data['renamed_method']['source_code']}\n"

    res = 'Language: Python\n\n' + input
    return res

def load_fewshot_examples(language, refactor_type, k=2):
    with open(fewshot_example_path + f"/{language.lower()}/{refactor_type.replace(' ', '_').lower()}.json", 'r') as f:
        data = json.load(f)
        
    return data[:k]

if __name__ == "__main__":
    print(load_fewshot_examples("python", "Extract Method", 2))