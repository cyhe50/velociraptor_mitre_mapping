# Velociraptor MITRE ATT&CK Mapping tools
## description
This is a tool to detect potential risks using MITRE ATT&CK framework and MITRE ATT&CK Navigator

## How to use
1. download MITRE STIX data


    choose one of the json file you want
    https://github.com/mitre-attack/attack-stix-data/tree/master

2. install velociraptor 
3. download this github
4. run run_all.sh


    NOTE: one parameters is required for specifing velociraptor datastore path
    `./generate_artifacts.sh ~/{path}/gui_datastore`
5. open velociraptor server
    `velociraptor gui --datastore ~/{path}/gui_datastore`
6. run hunt for the main artifact
7. get the report and download it to data directory
8. tell the script the places you store the report
9. get the converted MITRE navigator layer
10. visit MITRE navigator and upload the file
