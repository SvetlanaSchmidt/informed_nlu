import requests
import xml.etree.ElementTree as ET
import json

# Step 1: Download the XML file from the URL
url = 'https://nlp.stanford.edu/projects/contradiction/real_contradiction.xml'
response = requests.get(url)

# Step 2: Parse the XML content
root = ET.fromstring(response.content)

# Step 3: Extract the contradiction pairs
contradictions = []

for pair in root.findall('.//pair'):
    contradiction = {
        'id': pair.attrib['id'],
        'contradiction': pair.attrib['contradiction'],
        'type': pair.attrib['type'],
        'text': pair.find('t').text,
        'hypothesis': pair.find('h').text
    }
    contradictions.append(contradiction)

# Step 4: Save the extracted pairs as JSON
with open('contradiction_pairs.json', 'w') as json_file:
    json.dump(contradictions, json_file, indent=4)

print("Contradiction pairs saved as 'contradiction_pairs.json'.")