import json
import os
import re

# VQL template for different types of data
VQL_TEMPLATES = {
    "process_execution": """
LET process_events = SELECT * FROM pslist()
WHERE Name =~ '{process_name}'
LIMIT 50

SELECT 
    '{technique_id}' as TechniqueID,
    '{technique_name}' as TechniqueName,
    'process_execution' as Tactic,
    *
FROM process_events
""",
    
    "file_creation": """
LET file_events = SELECT * FROM glob(globs='{file_path}')
LIMIT 50

SELECT 
    '{technique_id}' as TechniqueID,
    '{technique_name}' as TechniqueName,
    'file_creation' as Tactic,
    *
FROM file_events
""",

    "persistence": """
LET persistence_locations = SELECT * FROM Artifact.MacOS.Detection.Autoruns()
LIMIT 50

SELECT 
    '{technique_id}' as TechniqueID,
    '{technique_name}' as TechniqueName,
    'persistence' as Tactic,
    *
FROM persistence_locations
"""
}

def load_techniques(filepath):
    with open(filepath, 'r') as f:
        techniques = json.load(f)
    return techniques

def generate_vqls(techniques):
    vqls = []

    for tech in techniques:
        tmp_vqls = convert_single_technique_to_vqls(tech)
        vqls.extend(tmp_vqls)

    return vqls

def convert_single_technique_to_vqls(technique):
    id = technique['id']
    name = technique['name']
    description = technique['description']
    platforms = technique['platforms']

    vqls = []
    # process_execution 
    if any(keyword in description for keyword in ["process", "launch", "execute", "run"]):
        process_names = re.findall(r'`([^`]+)`', description)

        # if nothing found, use default suspicious processes
        if not process_names:
            process_names = ["bash", "sh", "python", "perl", "ruby"]

        for process_name in process_names: 
            query = VQL_TEMPLATES["process_execution"].format(
                process_name=process_name,
                technique_id=id,
                technique_name=name
            )

            vql = {
                "id": id,
                "name": f"{id}_{process_name}",
                "description": f"process_execution type of {name} with ID {id}",
                "vql": query
            }

            vqls.append(vql)

    # file_creation
    if any(keyword in description for keyword in ["file", "create", "write", "modify"]):
        suspicious_paths = [
            "/tmp/*", 
            "/Users/*/Library/LaunchAgents/*",
            "/Library/LaunchAgents/*",
            "/Library/LaunchDaemons/*"
        ]
        for path in suspicious_paths:
            query = VQL_TEMPLATES["file_creation"].format(
                file_path=path,
                technique_id=id,
                technique_name=name
            )

            vql = {
                "id": id,
                "name": f"{id}_{path.replace('/', '_').replace('*', 'X')}",
                "description": f"file_creation type of {name} with ID {id}",
                "vql": query
            }

            vqls.append(vql)

    # persistence
    if any(keyword in description for keyword in ["persist", "boot", "startup", "launch agent", "launch daemon"]):
        query = VQL_TEMPLATES["persistence"].format(
            technique_id=id,
            technique_name=name
        )
        
        vql = {
            "id": id,
            "name": f"{id}_persistence",
            "description": f"persistence type of {name} with ID {id}",
            "vql": query
        }

        vqls.append(vql)


    return vqls


def main():
    filepath = 'data/stix_techniques.json'

    print(f"Start loading techniques from {filepath}")
    techniques = load_techniques(filepath)

    print(f"Start generating vqls")
    vqls = generate_vqls(techniques)

    with open('data/techniques_with_vqls.json', 'w') as f:
        json.dump(vqls, f, indent=4)

    print("Finished")


if __name__ == "__main__":
    main()
