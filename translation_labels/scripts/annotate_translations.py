import openai
import json
import pandas as pd
from translation_labels.trans_labels_types1 import *
#from informed_nlu.utils.api_key import api_key # you need to provide your personal API key in this file
from utils import read_data, read_and_extend_data, compute_cohens_kappa

# path to adjust to your system, where the repository is located
base_path = "add base path"

# OpenAI config
openai.api_key="add api key"
model='gpt-4'
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

#load the data for annotation
data = read_data('/scratch/informed_nlu/translation_labels/content/TQA_PromptGPT_Input.xlsx')

annotation_labels = [label_1, label_2, label_3, label_4, label_5]
annotation_labels_descriptions = [label_1.description, label_2.description, label_3.description, label_4.description, label_5.description]

lang_d = {'eng_deu_pairs' : 'german', 'eng_spa_pairs' : 'spanish', 'eng_ben_pairs' : 'bengali', 'eng_rus_pairs' : 'russian'}

#iterate over each source-target sentece pair and generate annotation
for d in data:
    responses=[]
    language = lang_d[d]
    for source, target in data[d]:
        response=[]
        res = openai.ChatCompletion.create(
        model=model,
        max_tokens=max_tokens,
        messages=[
                {"role": "system", "content": f"Score the quality of the translations from english to {language} from {source} to {target}\
                You have to validate the translation from english to {language} with respect to human reference using one of the {annotation_labels} and their {annotation_labels_descriptions}."},
                {"role": "user", "content": f"Please annotate the translation of the {source} to the {target}, based on the description of the chosen annotation label from {annotation_labels} and explain your choice.\
                Format your response in the following way: annotation_label S: [SOURCE], T: [TARGET] R: [reasoning]."}
            ]
        )

        print(res["choices"][0]["message"]["content"])
        response.append(res["choices"][0]["message"]["content"])
        if response not in responses:
            responses.append(response)
    #save annotations for each target lanbguage as json
    samples=[]
    with open(f'gpt_translation_annotation_{d}.json', 'w') as fp:
        for r in responses:
            sample={}
            for pair in r:
                sents = pair.split("T:")
                print(sents)
                source = sents[0]
                target = sents[1]
                sample["label"] = source.split("S: ")[0].strip("\n")#.strip(", ")
                sample["source"] = source.split("S: ")[1].strip("\n")#.strip(", ")
                sample["target"] = target.split("R: ")[0].strip("\n").strip()
                sample["reason"] = target.split("R: ")[1].strip("\n")
                fp.write(json.dumps(sample) + "\n")     
                
     

gpt_annot = read_and_extend_data("/scratch/informed_nlu/translation_labels/content/TQA_PromptGPT_Input.xlsx", "TQA_PromptGPT_Input_all_2.0_1.xlsx")


gpt1_data = pd.read_excel("/scratch/informed_nlu/translation_labels/scripts/TQA_PromptGPT_Input_all_2.0_1.xlsx", header=0)
gpt2_data = pd.read_excel("/scratch/informed_nlu/translation_labels/content/TQA_GPT_XSTSscores_sec(1) - Kopie.xlsx", header=0)

#kappa computation
compute_cohens_kappa(gpt1_data, gpt2_data)

