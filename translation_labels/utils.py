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

def read_data_json(path):
    annotations = []
    source = []
    target = []
    for line in open(path, mode='r', encoding='utf-8'):
        reader = json.loads(line)
        line_lst = {}
        for k in reader.keys():
            #TODO: possibly add source and target if there are mismatch in languages
            if k == 'label' or k == 'reason':
                line_lst[k]= reader[k]
        annotations.append(line_lst)

                        
    return annotations

def read_and_extend_data(excel_path, output_excel_path):
    tq_data = read_data_excel(excel_path)
    eng_deu = read_data_json("/scratch/informed_nlu/translation_labels/scripts/gpt_translation_annotation_eng_deu_pairs.json")
    eng_ben = read_data_json("/scratch/informed_nlu/translation_labels/scripts/gpt_translation_annotation_eng_ben_pairs.json")
    eng_rus = read_data_json("/scratch/informed_nlu/translation_labels/scripts/gpt_translation_annotation_eng_rus_pairs.json")
    eng_spa = read_data_json("/scratch/informed_nlu/translation_labels/scripts/gpt_translation_annotation_eng_spa_pairs.json")
    
    result_df = tq_data.copy()
    result_df['GPT_RU_XSTS-score'] = [r['label'].strip("annotation_label ") for r in (eng_rus or [])]
    result_df['GPT_RU_Reasoning'] = [r['reason'] for r in (eng_rus or [])]
    
    result_df_1 = result_df.copy()
    result_df_1['GPT_SP_XSTS-score'] = [r['label'].strip("annotation_label ") for r in (eng_spa or [])]
    result_df_1['GPT_SP_Reasoning'] = [r['reason'] for r in (eng_spa or [])]
    
    result_df_2 = result_df_1.copy()
    result_df_2['GPT_DE_XSTS-score'] = [r['label'].strip("annotation_label ") for r in (eng_deu or [])]
    result_df_2['GPT_DE_Reasoning'] = [r['reason'] for r in (eng_deu or [])]
    
    result_df_3 = result_df_2.copy()
    result_df_3['GPT_BEN_XSTS-score'] = [r['label'].strip("annotation_label ") for r in (eng_ben or [])]
    result_df_3['GPT_BEN_Reasoning'] = [r['reason'] for r in (eng_ben or [])]
    
    result_df_3.to_excel(output_excel_path, index=False)  # Save to Excel without index column
    print("DataFrame saved to:", output_excel_path)
    
    return result_df_3
