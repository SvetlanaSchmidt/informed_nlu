import json
import requests
import tqdm
import random
import time
from copy import deepcopy

random.seed(31)

samples = []
with open("/shared_with_lisa/contradiction_detection/data/raw/TED/TED2020.json", "r") as fp:
    for line in fp:
        samples.append(json.loads(line))

data_updated = []
random.shuffle(samples)
for sample in tqdm.tqdm(samples[:100000]):
    try:
        r_de = eval(requests.get(f"http://api.syntagnet.org/disambiguate?lang=DE&text={sample['de']}", timeout=5).content)
        time.sleep(0.5)
        r_en = eval(requests.get(f"http://api.syntagnet.org/disambiguate?lang=EN&text={sample['en']}", timeout=5).content)
        time.sleep(0.5)

        """for token_de in r_de["tokens"]:
            print(token_de["senseID"])
            print(sample["de"][token_de["position"]["charOffsetBegin"]:token_de["position"]["charOffsetEnd"]])
            print()
        
        print("-------------------------------------------")

        for token_en in r_en["tokens"]:
            print(token_en["senseID"])
            print(sample["en"][token_en["position"]["charOffsetBegin"]:token_en["position"]["charOffsetEnd"]])
            print()"""
        
        syn_de = {}
        syn_en = {}

        sample_updated = deepcopy(sample)
        for token_de in r_de["tokens"]:
            syn_de.update({f'{token_de["position"]["charOffsetBegin"]}-{token_de["position"]["charOffsetEnd"]}': token_de["senseID"]})
        for token_en in r_en["tokens"]:
            syn_en.update({f'{token_en["position"]["charOffsetBegin"]}-{token_en["position"]["charOffsetEnd"]}': token_en["senseID"]})

        sample_updated.update({"syn_de": syn_de, "syn_en": syn_en})
        #print(sample_updated)
        data_updated.append(sample_updated)
        json.dump(data_updated, open("/shared_with_lisa/contradiction_detection/data/raw/TED/TED2020_with_syn.json", "w"))
    except Exception as e:
        print(e)



