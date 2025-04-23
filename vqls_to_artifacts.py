import json
import yaml
import os

def load_vqls(filepath):
    with open(filepath, 'r') as f:
        vqls = json.load(f)

    return vqls

def generate_artifacts(techniques, dirpath):
    artifacts = []
    for tech in techniques:
        artifact = generate_single_artifact(tech)

        # dump 
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        filepath = os.path.join(dirpath, f"{tech['name']}.yaml")
        with open(filepath, 'w') as f:
            yaml.dump(artifact, f, default_flow_style=False, sort_keys=False)

        artifacts.append(artifact)

    return artifacts


def generate_single_artifact(technique):
    artifact = {
        'name': f"Custom.MITRE.{technique['name']}",
        'type': "CLIENT",
        'description': technique['description'],
        'sources': [
            {
                'query': technique['vql']
            }
        ]
    }

    return artifact

def generate_main_artifact(artifacts):
    artifact_names = [artifact['name'] for artifact in artifacts]

    # Build the VQL query that calls all artifacts
    vql_query = "LET all_results = SELECT * FROM chain(\n"
    
    for i, name in enumerate(artifact_names):
        vql_query += f"    a{i} = {{ SELECT *, '{name}' AS SourceArtifact FROM Artifact.{name}() }},\n"
    
    # Remove the last comma and close the chain
    vql_query = vql_query.rstrip(",\n") + "\n)\n\n"
    
    # Add the final SELECT statement
    vql_query += """
        SELECT
            * 
        FROM all_results
        """
    
    # Create the main artifact
    main_artifact = {
        'name': 'Custom.MITRE.MAIN.AllDetections',
        'type': 'CLIENT',
        'description': 'Run all MITRE ATT&CK detection rules for macOS',
        'sources': [
            {
                'query': vql_query
            }
        ],
    }

    return main_artifact


def main():
    filepath = 'data/techniques_with_vqls.json'
    print(f"Start loading Techniques with vqls in {filepath}")
    techniques = load_vqls(filepath)

    
    dirpath = 'data/artifacts'
    print("Start generating artifacts in {dirpath} directory")
    artifacts = generate_artifacts(techniques, dirpath)

    print("Start generating main artifact")
    main_artifact = generate_main_artifact(artifacts)

    filepath = 'data/Custom_MITRE_MAIN_AllDetections.yaml'
    print(f"Start dumping main artifact to {filepath}")
    with open(filepath, 'w') as f:
        yaml.dump(main_artifact, f, default_flow_style=False, sort_keys=False)

    print("Finished")


if __name__ == "__main__":
    main()
