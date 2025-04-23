import json
import argparse

MITRE_NAVIGATOR = {
    "name": "layer",
    "versions": {
      "attack": "16",
      "navigator": "5.1.0",
      "layer": "4.5"
    },
    "domain": "enterprise-attack",
    "description": "",
    "filters": {
      "platforms": [
        "Windows",
        "Linux",
        "macOS",
        "Network",
        "PRE",
        "Containers",
        "IaaS",
        "SaaS",
        "Office Suite",
        "Identity Provider"
      ]
    },
    "sorting": 0,
    "layout": {
      "layout": "side",
      "aggregateFunction": "average",
      "showID": False,
      "showName": True,
      "showAggregateScores": False,
      "countUnscored": False,
      "expandedSubtechniques": "none"
    },
    "hideDisabled": False,
    "gradient": {
      "colors": [
        "#ff6666ff",
        "#ffe766ff",
        "#8ec843ff"
      ],
      "minValue": 0,
      "maxValue": 100
    },
    "legendItems": [],
    "metadata": [],
    "links": [],
    "showTacticRowBackground": False,
    "tacticRowBackground": "#dddddd",
    "selectTechniquesAcrossTactics": True,
    "selectSubtechniquesWithParent": False,
    "selectVisibleTechniques": False,
    "techniques": []
}

# navigator score used to classify different tatic
TATIC_SCORE = {
    "process_execution": 1,
    "file_creation": 2,
    "persistence": 3,
}

def load_events(filepath):
    events = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                events.append(json.loads(line))

    return events

def convert_events_to_navigator_layer(events):
    navigator = MITRE_NAVIGATOR.copy()

    for event in events:
        technique = {
            "techniqueID": event['TechniqueID'],
            "tactic": event['Tactic'],
            "comment": event['TechniqueName'],
            "enabled": True,
            "metadata": [],
            "score": TATIC_SCORE.get(event['Tactic'], 0),
            "showSubtechniques": False

        }

        navigator['techniques'].append(technique)

    return navigator

def main():
    # args
    parser = argparse.ArgumentParser(description='Generate MITRE ATT&CK Navigator from hunt report in Velociraptor')
    parser.add_argument('--input', required=True, help='Path to hunt report')
    parser.add_argument('--output', required=False, help='Path to hunt report, default is data/Navigator.json')

    args = parser.parse_args()


    filepath = args.input
    print(f"Start loading hunt report from {filepath}")
    events = load_events(filepath)


    print(f"Start converting hunt events to navigator layer")
    navigator = convert_events_to_navigator_layer(events)

    filepath = args.output
    if not filepath:
        filepath = 'data/Navigator.json'
    print(f"Start dumping navigator layer to {filepath}")
    with open(filepath, 'w') as f:
        json.dump(navigator, f, indent=4)


    print("Finished")


if __name__ == '__main__':
    main()
