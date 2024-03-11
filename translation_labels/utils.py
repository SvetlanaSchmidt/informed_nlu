import json
import pandas as pd


def read_data(path):
    tq_data = pd.read_excel(path, header=0, usecols= [9,10,11,12,13,14,15,16,17,18,19,20,21])
    source_sentences = []
    target_sentences = []

    source_eng = tq_data['eng [eng_Latn.devtest]']
    target_deu = tq_data['eng-deu [flores200-eng_Latn-deu_Latn-devtest]']
    target_spa = tq_data['eng-spa [flores200-eng_Latn-spa_Latn-devtest]']
    target_ben = tq_data['eng-ben [flores200-eng_Latn-ben_Beng-devtest]']
    target_rus = tq_data['eng-rus [flores200-eng_Latn-rus_Cyrl-devtest]']


    # define a list for prompts
    eng_deu=[]
    # loop through zipped source and target segments
    for src,trg in zip(source_eng,target_deu):
            eng_deu.append((src,trg))
    # assign list as new column in DataFrame
    tq_data['eng-deu-pairs'] = eng_deu
        # for line in open(path, mode='r', encoding='utf-8'):
        #     reader = json.loads(line)
        #     #line_lst = []
        #     for k in reader.keys():
        #         if k == 'sentence1':
        #             source_sentences.append(reader[k])
        #             target_sentences.append(reader[k])                 

    return source_sentences

