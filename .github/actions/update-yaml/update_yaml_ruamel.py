#!/usr/bin/env python3
from ruamel.yaml import YAML

def normalize_key(key: str) -> str:
    """
    Normalize a key by replacing dashes with underscores and lowercasing it.
    """
    return key.replace("-", "_").lower()

def update_data(target: dict, source: dict):
    """
    Recursively updates the target dictionary with values from the source
    for keys that already exist in the target.
    
    - Keys are compared using normalized forms.
    - A custom mapping is applied for known synonyms:
         "nonprod" in source maps to "nprd" in target,
         "prod" maps to "prd".
    """
    # Custom mapping for known synonyms
    custom_mapping = {
        "nonprod": "nprd",
        "prod": "prd"
    }
    
    # Create a mapping from normalized target keys to their original keys.
    norm_target_map = {normalize_key(k): k for k in target.keys()}
    
    for source_key, source_value in source.items():
        norm_source_key = normalize_key(source_key)
        
        # First try a direct match.
        if norm_source_key in norm_target_map:
            target_key = norm_target_map[norm_source_key]
        # Otherwise, check if the normalized key has a custom mapping.
        elif norm_source_key in custom_mapping:
            mapped_key = custom_mapping[norm_source_key]
            if mapped_key in norm_target_map:
                target_key = norm_target_map[mapped_key]
            else:
                continue
        else:
            continue

        target_value = target[target_key]
        if isinstance(target_value, dict) and isinstance(source_value, dict):
            update_data(target_value, source_value)
        else:
            target[target_key] = source_value

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--file1', required=True, help='Path to file1 YAML file')
    parser.add_argument('--file2', required=True, help='Path to file2 YAML file')
    parser.add_argument('--output', required=False, help='Path for the output file (defaults to file2)', default=None)
    args = parser.parse_args()

    file1_path = args.file1
    file2_path = args.file2
    output_path = args.output if args.output else file2_path

    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)

    with open(file1_path, 'r') as f1:
        data1 = yaml.load(f1)
    with open(file2_path, 'r') as f2:
        data2 = yaml.load(f2)

    update_data(data2, data1)

    with open(output_path, 'w') as out:
        yaml.dump(data2, out)
    
    print("YAML update completed successfully!")

if __name__ == "__main__":
    main()
