#bin/sh

# check if parameter 1 exist -> used for datastore dir 
if [ -z "$1" ]; then
	echo "Missing Gui Datastore Path"
	echo "Example Command: generate_artifacts.sh /tmp/gui_datastore"
	exit
fi

# mkdir data dir if not exist
dir="data"
if [ ! -d "$dir" ]; then
	mkdir -p "$dir"
fi


# TODO: might be able to skip this process because it ran slow
python3 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt


# TODO: check finished string captured
echo "----------------Run stix_to_techniques.py--------------------"
python stix_to_techniques.py


# TODO: check finished string captured
echo "----------------Run techniques_to_vqls.py--------------------"
python techniques_to_vqls.py


# TODO: check finished string captured
echo "----------------Run vqls_to_artifacts.py--------------------"
python vqls_to_artifacts.py


# TODO: upload all artifacts (include main artifact) to specified datastore (cmd arg)
echo "----------------Upload artifacts to Velociraptor Server--------------------"
path="$1/artifact_definitions/"
echo "copy data/artifacts to $path"
cp data/artifacts/* "$path"

echo "copy data/Custom_MITRE_MAIN_AllDetections.yaml to $path"
cp data/Custom_MITRE_MAIN_AllDetections.yaml "$path"


echo "Finished Uploading Artifacts"

echo """
Let's Run Hunt on Velociraptor:
1. Run command: velociraptor gui --datastore {$1}
2. Open Velociraptor Server and Navigate to artifacts
3. press Custom.MITRE.MAIN.AllDetections on the artifacts section, press Hunt Artifact, and press Launch
4. Remember to Run Hunt
5. Wait for the Hunt to be completed
6. After completed, press the flowID to get the result
7. dump the result as json
8. copy json file to data directory
"""

read -p "Prepare your hunt report to continue the following"

read -p "Enter report file path: " reportPath
echo "report path is {$reportPath}"

echo "Run Converting to MITRE ATT&CK Navigator Layer format"
python hunt_report_to_mitre_navigator.py --input $reportPath


echo "Finished Converting to MITRE ATT&CK Navigator format"

