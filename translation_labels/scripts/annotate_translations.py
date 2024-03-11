import openai
import random
import re
import json
import time
from informed_nlu.translation_labels.translation_labels.trans_labels_types import *
from informed_nlu.utils.api_key import api_key # you need to provide your personal API key in this file
from informed_nlu.translation_labels.utils import read_prem

# path to adjust to your system, where the repository is located
base_path = "/scratch/"

# OpenAI config
openai.api_key=api_key
model_new_types='gpt-4'
model_new_samples = "gpt-4"
max_tokens=512
temperature=1

# total iterations
iterations = 1
# number of contradiction type examples to provide in each prompt
prompt_examples = 3
# number of new contradictions to generate for each type
num_contradictions = 5

total_cost = 0
total_num_contradictions = 0
total_num_types = 0

#TODO loop anpassen
# sentence pairs einlesen
# prompt anpassen
for premise in train_premises[:50]:
    #premise=train_premises[i]
    response=[]
    for contradiction_type in contradiction_types:
        res = openai.ChatCompletion.create(
        model=model,
        max_tokens=max_tokens,
        messages=[
                {"role": "system", "content": "You are an expert on semantics and linguistics, with a profound knowledge\
                in Natural Language Processing. You are especially aware of the work by Marneffe et al., classifying\
                different types of contradictions, such as factive, structural, lexical, and world knowledge contradictions. The Premise is provided,\
                you have to create a Hypothesis of one of the contradiction types for this premise."},
                {"role": "user", "content": f"Please generate one contradictory Hypothesis for a {premise}, based on {contradiction_type.description}.\
                Format your response in the following way: {contradiction_type.name} P: [PREMISE], H: [HYPOTHESIS]."},
                {"role": "assistant", "content": contradiction_type.description},
            ]
        )

        print(res["choices"][0]["message"]["content"])
        response.append(res["choices"][0]["message"]["content"])
    if response not in responses:
        responses.append(response)

samples=[]
with open('gpt_complex_contradictions.json', 'w') as fp:
    for r in responses:
        sample={}
        for pair in r:
            sents = pair.split("H:")
            premise=sents[0]
            sample["label"] = "contradiction" + " " + premise.split("P: ")[0].strip("\n")#.strip(", ")
            sample["sentence1"] = premise.split("P: ")[1].strip("\n")#.strip(", ")
            sample["sentence2"] = sents[1]
            fp.write(json.dumps(sample) + "\n")           
