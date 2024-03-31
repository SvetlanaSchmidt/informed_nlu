import json
import pandas as pd
from sklearn.metrics import cohen_kappa_score
    

def read_data(path_to_excel):
    """prepares data for annotaion
    returns: dict: for every target language returns lists with siurce-target sentence pairs"""
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
    """crates list of source and target sentences"""
    src_tar = []
    for src, trg in zip(source, target):
        src_tar.append((src, trg))
    return src_tar

def read_data_excel(path):
    tq_data = pd.read_excel(path, header=0, usecols=[9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21])
    return tq_data

def read_data_json(path):
    """
    reads the generated annotations in and returns them in a list
    """
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
    """
    Extends the pandas dataframe with the GPT generated annotations and their reasonings
    """
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

def clean_annot(annotations):
    """ Prepares labels for Cohen's kappa computation    
    """
    clean_annot=[]
    for i,annot in enumerate(annotations):
        if type(annot) == str:
            if "1" in annot:
                new_annot = "1"
            elif "2" in annot:
                new_annot = "2"
            elif "3" in annot:
                new_annot = "3"
            elif "4" in annot:
                new_annot = "4"
            elif "5" in annot:
                new_annot = "5"
            clean_annot.append(new_annot)
    return clean_annot
            
    

def compute_cohens_kappa(gpt1_df, gpt2_df):
    """
    Computes teh Cohen's kappa 
    Params:
     - gpt1_df: df with modified gpt annotation (gpt has access to the labels description)
     - gpt2_df: df with human annotations and first GPT-annotation attemp
    """
    #annotations gained with modified annot process when gpt has access to label description
    eng_deu_mod = clean_annot(gpt1_df['GPT_DE_XSTS-score'].values.tolist())
    eng_ben_mod = clean_annot(gpt1_df['GPT_BEN_XSTS-score'].values.tolist())
    eng_rus_mod = clean_annot(gpt1_df['GPT_RU_XSTS-score'].values.tolist())
    eng_spa_mod = clean_annot(gpt1_df['GPT_SP_XSTS-score'].values.tolist())

    eng_deu = clean_annot(gpt2_df['GPT_DE_XSTS-score'].values.tolist())
    eng_ben = clean_annot(gpt2_df['GPT_BEN_XSTS-score'].values.tolist())
    eng_rus = clean_annot(gpt2_df['GPT_RU_XSTS-score'].values.tolist())
    eng_spa = clean_annot(gpt2_df['GPT_SP_XSTS-score'].values.tolist())
    
    #human annotations 1 and 2     
    eng_rus_h1 = clean_annot(gpt2_df['annotation1_RUS_XSTS-score'].values.tolist())
    eng_rus_h2 = clean_annot(gpt2_df['annotation2_RUS_XSTS-score'].values.tolist())
    eng_deu_h1 = clean_annot(gpt2_df['annotator1_DE_XSTS-score'].values.tolist())
    eng_deu_h2 = clean_annot(gpt2_df['annotator2_DE_XSTS-score'].values.tolist())
    eng_ben_h1 = clean_annot(gpt2_df['annotator1_BEN_XSTS-score'].values.tolist())
    eng_ben_h2 = clean_annot(gpt2_df['annotator2_BEN_XSTS-score'].values.tolist())
    eng_spa_h1 = clean_annot(gpt2_df['annotation1_SP_XSTS-score'].values.tolist())
    eng_spa_h2 = clean_annot(gpt2_df['annotation2_SP_XSTS-score'].values.tolist())

    
    kappa_eng_deu = cohen_kappa_score(eng_deu_mod, eng_deu)
    kappa_eng_ben = cohen_kappa_score(eng_ben_mod, eng_ben)
    kappa_eng_rus = cohen_kappa_score(eng_rus_mod, eng_rus)
    kappa_eng_spa = cohen_kappa_score(eng_spa_mod, eng_spa)
    
    #Kappa between A1 and A2
    kappa_h_eng_rus = cohen_kappa_score(eng_rus_h1, eng_rus_h2)
    kappa_h_eng_ben = cohen_kappa_score(eng_ben_h1, eng_ben_h2)
    kappa_h_eng_deu = cohen_kappa_score(eng_deu_h1, eng_deu_h2)
    kappa_h_eng_spa = cohen_kappa_score(eng_spa_h1, eng_spa_h2[:49])
    
    #Kappa between GPT and annotators:
    #RUS A1
    kappa_gpt1_A1_rus = cohen_kappa_score(eng_rus_mod, eng_rus_h1)
    kappa_gpt0_A1_rus = cohen_kappa_score(eng_rus, eng_rus_h1)
    #RUS A2
    kappa_gpt1_A2_rus = cohen_kappa_score(eng_rus_mod, eng_rus_h2)
    kappa_gpt0_A2_rus = cohen_kappa_score(eng_rus, eng_rus_h2)
    #DEU A1
    kappa_gpt1_A1_deu = cohen_kappa_score(eng_deu_mod, eng_deu_h1)
    kappa_gpt0_A1_deu = cohen_kappa_score(eng_deu, eng_deu_h1)
    #DEU A2
    kappa_gpt1_A2_deu = cohen_kappa_score(eng_deu_mod, eng_deu_h2)
    kappa_gpt0_A2_deu = cohen_kappa_score(eng_deu, eng_deu_h2)
    #SP A1
    kappa_gpt1_A1_spa = cohen_kappa_score(eng_spa_mod[:49], eng_spa_h1)
    kappa_gpt0_A1_spa = cohen_kappa_score(eng_spa[:49], eng_spa_h1)
    #SP A2
    kappa_gpt1_A2_spa = cohen_kappa_score(eng_spa_mod, eng_spa_h2)
    kappa_gpt0_A2_spa = cohen_kappa_score(eng_spa, eng_spa_h2)    
    #BEN A1
    kappa_gpt1_A1_ben = cohen_kappa_score(eng_ben_mod, eng_ben_h1)
    kappa_gpt0_A1_ben = cohen_kappa_score(eng_ben, eng_ben_h1)
    #BEN A2
    kappa_gpt1_A2_ben = cohen_kappa_score(eng_ben_mod, eng_ben_h2)
    kappa_gpt0_A2_ben = cohen_kappa_score(eng_ben, eng_ben_h2)
    
    
    # Output the computed kappas for the current type_folder
    print(f"Cohen's kappa between GPT1 and GPT0 for eng-deu: {kappa_eng_deu}")
    print(f"Cohen's kappa between GPT1 and GPT0 for eng-ben: {kappa_eng_ben}")
    print(f"Cohen's kappa between GPT1 and GPT0 for eng-rus: {kappa_eng_rus}")
    print(f"Cohen's kappa between GPT1 and GPT0 for eng-spa: {kappa_eng_spa}")
    print()
    print(f"Cohen's kappa between for Russian A1 and A2: {kappa_h_eng_rus}")
    print(f"Cohen's kappa between for Russian GPT1 (mod) and A1: {kappa_gpt1_A1_rus}")
    print(f"Cohen's kappa between for Russian GPT0 and A1: {kappa_gpt0_A1_rus}")
    print(f"Cohen's kappa between for Russian GPT1 (mod) and A2: {kappa_gpt1_A2_rus}")
    print(f"Cohen's kappa between for Russian GPT0 and A2: {kappa_gpt0_A2_rus}")
    print()
    print(f"Cohen's kappa between for Bengali A1 and A2: {kappa_h_eng_ben}")
    print(f"Cohen's kappa between for Bengali GPT1 (mod) and A1: {kappa_gpt1_A1_ben}")
    print(f"Cohen's kappa between for Bengali GPT0 and A1: {kappa_gpt0_A1_ben}")
    print(f"Cohen's kappa between for Bengali GPT1 (mod) and A2: {kappa_gpt1_A2_ben}")
    print(f"Cohen's kappa between for Bengali GPT0 and A2: {kappa_gpt0_A2_ben}")
    print()
    print(f"Cohen's kappa between for German A1 and A2: {kappa_h_eng_deu}")
    print(f"Cohen's kappa between for German GPT1 (mod) and A1: {kappa_gpt1_A1_deu}")
    print(f"Cohen's kappa between for German GPT0 and A1: {kappa_gpt0_A1_deu}")
    print(f"Cohen's kappa between for German GPT1 (mod) and A2: {kappa_gpt1_A2_deu}")
    print(f"Cohen's kappa between for German GPT0 and A2: {kappa_gpt0_A2_deu}")
    print()
    print(f"Cohen's kappa between for Spanish A1 and A2: {kappa_h_eng_spa}")
    print(f"Cohen's kappa between for Spanish GPT1 (mod) and A1: {kappa_gpt1_A1_spa}")
    print(f"Cohen's kappa between for Spanish GPT0 and A1: {kappa_gpt0_A1_spa}")
    print(f"Cohen's kappa between for Spanish GPT1 (mod) and A2: {kappa_gpt1_A2_spa}")
    print(f"Cohen's kappa between for Spanish GPT0 and A2: {kappa_gpt0_A2_spa}")