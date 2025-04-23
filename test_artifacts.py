import yaml
import os
import re


testpath = 'test'
if not os.path.exists(testpath):
    os.makedirs(testpath)


# dump 2 examples of each vql type 
counts = {
    "file_creation": 2,
    "process_execution": 2,
    "persistence": 2,
}

dirpath = 'data/artifacts'
for filename in os.listdir(dirpath):
    values = sum(counts.values())
    if(values <= 0):
        break

    filepath = os.path.join(dirpath, filename)

    with open(filepath, 'r') as f:
        artifact = yaml.load(f, Loader=yaml.FullLoader)

    description = artifact.get('description', "")
    match = re.match(r'^(\w+)', description)

    if match and counts[match.group(1)] > 0:
        vql_type = match.group(1)
        
        test_filepath = os.path.join(testpath, filename)
        with open(test_filepath, 'w') as f:
            yaml.dump(artifact, f, default_flow_style=False, sort_keys=False)

        counts[vql_type] = counts[vql_type] - 1
        

