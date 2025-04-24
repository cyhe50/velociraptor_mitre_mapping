#!/usr/bin/env python3
import json
import os

def load_stix_from_json(filepath):
    with open(filepath, 'r') as f:
        stix_data = json.load(f)
    return stix_data

def convert_to_array_format(stix_data):
    techniques = []

    objects = stix_data.get('objects', [])
    for obj in objects:
        # extract only type of attack-pattern
        if obj.get('type') == 'attack-pattern':
            # extract only relevant for macos
            platforms = obj.get('x_mitre_platforms', [])
            if 'macOS' in platforms:

                # the external_id represents the technique id of the attack, e.g. T1059
                # it usually stores in the first element of external_references
                # TODO: get the external_id by finding the element with source_name equals to mitre-attack, instead of using index 0
                references = obj.get('external_references', [{}])
                tech_id = references[0].get('external_id', '')

                technique = {
                    'id': tech_id.replace('.', '_'),
                    'name': obj.get('name', ''),
                    'description': obj.get('description', ''),
                    'platforms': platforms,
                }

                techniques.append(technique)
    return techniques

def main():
    filepath = 'data/enterprise-attack.json'

    print(f"Start loading {filepath}")
    try:
        stix_data = load_stix_from_json(filepath)
    except Exception as e:
        print(f"failed to load {filepath}: {e}")
        os.exit(1)
        


    print(f"Start converting techniques to array format")
    try:
        techniques = convert_to_array_format(stix_data)
    except Exception as e:
        print(f"failed to convert stix_data: {e}")
        os.exit(1)


    outpath = 'data/stix_techniques.json'
    print(f"Start Dumping techniques to {outpath}")
    with open(outpath, 'w') as f:
        json.dump(techniques, f, indent=4)

    print("Finished")


if __name__ == "__main__":
    main()
