#!/usr/bin/env python3
import argparse
from ruamel.yaml import YAML

def update_data(target, source):
    """
    Recursively updates the target dictionary with values from the source
    for keys that already exist in target.
    """
    for key, source_value in source.items():
        if key in target:
            target_value = target[key]
            if isinstance(target_value, dict) and isinstance(source_value, dict):
                update_data(target_value, source_value)
            else:
                target[key] = source_value

def main():
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
