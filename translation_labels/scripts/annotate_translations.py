import openai
import random
import re
import json
import time
from translation_labels.trans_labels_types import *
#from informed_nlu.utils.api_key import api_key # you need to provide your personal API key in this file
from utils import read_data, read_and_extend_data

# path to adjust to your system, where the repository is located
base_path = "/scratch/"

# OpenAI config
openai.api_key=""
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

data = read_data('/scratch/informed_nlu/translation_labels/content/TQA_PromptGPT_Input.xlsx')

annotation_labels = [label_1, label_2, label_3, label_4, label_5]
#print("English-German pairs:")
#print(data['eng_deu_pairs'])

#eng_deu = data['eng_deu_pairs']


lang_d = {'eng_deu_pairs' : 'german', 'eng_spa_pairs' : 'spanish', 'eng_ben_pairs' : 'bengali', 'eng_rus_pairs' : 'russian'}

#comment out for GPT annotation
# for d in data:
#     responses=[]
#     language = lang_d[d]
#     for source, target in data[d]:
#         #premise=train_premises[i]
#         response=[]
#         res = openai.ChatCompletion.create(
#         model=model,
#         max_tokens=max_tokens,
#         messages=[
#                 {"role": "system", "content": f"You are an expert in translation from english to other languages, especially to german, russian, spanish and bengali.\
#                 You are provided with pairs of sentences, where the first sentence is in english - the source sentence, and the second, target, sentence is in {language}.\
#                 You have to validate the translation from english to other language with one of the {annotation_labels} for translation validation."},
#                 {"role": "user", "content": f"Please annotate the translation of the {source} to the {target}, based on the description of the chosen annotation label from {annotation_labels} and explain your choice.\
#                 Format your response in the following way: annotation_label S: [SOURCE], T: [TARGET] R: [reasoning]."}
#             ]
#         )

#         print(res["choices"][0]["message"]["content"])
#         response.append(res["choices"][0]["message"]["content"])
#         if response not in responses:
#             responses.append(response)

#     samples=[]
#     with open(f'gpt_translation_annotation_{d}.json', 'w') as fp:
#         for r in responses:
#             sample={}
#             for pair in r:
#                 sents = pair.split("T:")
#                 print(sents)
#                 source = sents[0]
#                 target = sents[1]
#                 sample["label"] = source.split("S: ")[0].strip("\n")#.strip(", ")
#                 sample["source"] = source.split("S: ")[1].strip("\n")#.strip(", ")
#                 sample["target"] = target.split("R: ")[0].strip("\n").strip()
#                 sample["reason"] = target.split("R: ")[1].strip("\n")
#                 fp.write(json.dumps(sample) + "\n")     
                
    #TODO: save data to the original dataframe for the further analysis    

ext_ben = read_and_extend_data("/scratch/informed_nlu/translation_labels/content/TQA_PromptGPT_Input.xlsx", "/scratch/informed_nlu/translation_labels/scripts/gpt_translation_annotation_eng_ben_pairs.json", "TQA_PromptGPT_Input_ben.xlsx")
ext_deu = read_and_extend_data("TQA_PromptGPT_Input_ben.xlsx", "/scratch/informed_nlu/translation_labels/scripts/gpt_translation_annotation_eng_deu_pairs.json", "TQA_PromptGPT_Input_ben_deu.xlsx")
ext_rus = read_and_extend_data("TQA_PromptGPT_Input_ben_deu.xlsx", "/scratch/informed_nlu/translation_labels/scripts/gpt_translation_annotation_eng_rus_pairs.json", "TQA_PromptGPT_Input_ben_deu_rus.xlsx")
ext_spa = read_and_extend_data("TQA_PromptGPT_Input_all.xlsx", "/scratch/informed_nlu/translation_labels/scripts/gpt_translation_annotation_eng_spa_pairs.json", "TQA_PromptGPT_Input_ben_deu_rus_spa.xlsx")
