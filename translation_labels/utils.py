import json
import pandas as pd


def create_column(source, target):
    # define a list for prompts
    src_tar=[]
    # loop through zipped source and target segments
    for src,trg in zip(source,target):
            src_tar.append((src,trg))
    return src_tar
    

def read_data(path_to_excel):
    tq_data = pd.read_excel(path_to_excel, header=0, usecols= [9,10,11,12,13,14,15,16,17,18,19,20,21])
    source_sentences = []
    target_sentences = []

    source_eng = tq_data['eng [eng_Latn.devtest]']
    target_deu = tq_data['eng-deu [flores200-eng_Latn-deu_Latn-devtest]']
    target_spa = tq_data['eng-spa [flores200-eng_Latn-spa_Latn-devtest]']
    target_ben = tq_data['eng-ben [flores200-eng_Latn-ben_Beng-devtest]']
    target_rus = tq_data['eng-rus [flores200-eng_Latn-rus_Cyrl-devtest]']



    tq_data['eng-deu-pairs'] = create_column(source_eng, target_deu)
    tq_data['eng-spa-pairs'] = create_column(source_eng, target_deu)
    tq_data['eng-ben-pairs'] = create_column(source_eng, target_deu)
    tq_data['eng-rus-pairs'] = create_column(source_eng, target_deu)
    
    eng_deu_pairs = create_column(source_eng, target_deu)
    eng_spa_pairs = create_column(source_eng, target_spa)
    eng_ben_pairs = create_column(source_eng, target_ben)
    eng_rus_pairs = create_column(source_eng, target_rus)
  
            
    return {
    'eng_deu_pairs': eng_deu_pairs,
    'eng_spa_pairs': eng_spa_pairs,
    'eng_ben_pairs': eng_ben_pairs,
    'eng_rus_pairs': eng_rus_pairs
    }
    
def create_column(source, target):
    src_tar = []
    for src, trg in zip(source, target):
        src_tar.append((src, trg))
    return src_tar

def read_data_excel(path):
    tq_data = pd.read_excel(path, header=0, usecols=[9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21])
    return tq_data

def read_data_json(path, tq_data):
    annotations = []
    source = []
    target = []
    for line in open(path, mode='r', encoding='utf-8'):
        reader = json.loads(line)
        #line_lst = []
        for k in reader.keys():
            if k == 'sentence1':
                premises.append(reader[k])                

    return premises

def read_and_extend_data(excel_path, json_path, output_excel_path):
    tq_data = read_data_excel(excel_path)
    tq_data_extended = read_data_json(json_path, tq_data)
    
    tq_data_extended.to_excel(output_excel_path, index=False)  # Save to Excel without index column
    print("DataFrame saved to:", output_excel_path)
    
    return tq_data_extended
