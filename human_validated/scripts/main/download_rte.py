import requests
import xml.etree.ElementTree as ET
import json


def download_rte_dataset(url: str):
    """
    1: download the XML file from the URL
    2: parse the XML content
    3: extract the elements of each par
    4: save labels, premises and hypothesis pairwise to JSON file
    """
    
    response = requests.get(url)
    root = ET.fromstring(response.content)

    with open('contradiction_pairs.json', 'w') as json_file:
        for pair in root.findall('.//pair'):
            if pair.attrib['contradiction'] == 'YES':
                gold_label = 'contradiction'
            contradiction = {
                'gold_label': gold_label,
                'sentence1': pair.find('t').text,
                'sentence2': pair.find('h').text
            }
            json_file.write(json.dumps(contradiction) + '\n')

def main():   
    url = 'https://nlp.stanford.edu/projects/contradiction/real_contradiction.xml'
    download_rte_dataset(url)

if __name__=="__main__":
    main()


