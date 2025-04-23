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



echo "Finished Uploading. Now you can go Velociraptor server to check themk"

