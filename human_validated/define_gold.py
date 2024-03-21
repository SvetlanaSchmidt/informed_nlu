import os
import json
import pandas as pd
import numpy as np
from iaa_measure import compute_cohens_kappa, calculate_kappa_alpha, iaa_measure_bin


def data_prep(group_data_path):
    """
    prepare data for gold labels definition and analysis 
    Params:
     - path to the file containing the annotated data of one type and one group
    Return:
     - returns pandas dataframe with columns: sentence1, sentence2, annotator_labels
    """
    with open(group_data_path, "r") as json_file:
        data = json.load(json_file)
        
    sentence1_list = []
    sentence2_list = []
    label_list = []
    annotator1=[]
    annotator2=[]
    annotator3=[]

    for i, (key, value) in enumerate(data.items()):
        if i == 0:
            for entry in value:
                sentence1_list.append(entry["sentence1"])
                sentence2_list.append(entry["sentence2"])
                annotator1.append(entry["label"])
        elif i == 1:
            for entry in value:
                annotator2.append(entry["label"])
        else:
            for entry in value:
                annotator3.append(entry["label"])
        
    for a1, a2, a3 in zip(annotator1, annotator2,annotator3):
        label_list.append([a1,a2,a3])
        
    label_list = clean_labels(label_list)
    sentence1, sentence2, label_bin_list = clean_bin_labels(sentence1_list, sentence2_list, label_list)
    data_d = {"sentence1": sentence1_list, "sentence2": sentence2_list, "annotator_labels": label_list}
    data_df = pd.DataFrame(data=data_d)
    
    data_d_bin = {"sentence1": sentence1, "sentence2": sentence2, "annotator_labels": label_bin_list}
    data_df_bin = pd.DataFrame(data=data_d_bin)
    
    return data_df, data_df_bin

def clean_labels(annotations_list):
    cleaned_annotations = []
    for pair in annotations_list:
        clean_pair = []
        for annotation in pair:
            if "other contradiction" in annotation:
                annotation = "other contradiction"
            elif "factive contradiction" in annotation:
                annotation = "factive contradiction"
            elif "no contradiction" in annotation:
                annotation = "no contradiction"
            elif "difficult to answer" in annotation:
                annotation = "difficult to answer"
            elif "lexical contradiction" in annotation:
                annotation = "lexical contradiction"
            elif "structural contradiction" in annotation:
                annotation = "structural contradiction"
            elif "world knowledge contradiction" in annotation:
                annotation = "world knowledge contradiction"
            clean_pair.append(annotation)
        cleaned_annotations.append(clean_pair)
                
    return cleaned_annotations

def clean_bin_labels(sent1, sent2, annotations_list):
    clean_annotations = []
    clean_sent1 = []
    clean_sent2 = []
    for s1, s2, pair in zip(sent1, sent2, annotations_list):
        clean_pair = []
        for annotation in pair:
            if "no contradiction" in annotation:
                annotation = "no contradiction"
            else: 
                annotation = "contradiction"
                
            clean_pair.append(annotation)

        if len(clean_pair) == 3: 
            clean_annotations.append(clean_pair)
            clean_sent1.append(s1)
            clean_sent2.append(s2)
                
    return clean_sent1, clean_sent2, clean_annotations
            

def calculate_gold_label_frequency(combined_dfs, gold_label):
    for type_folder, combined_df in combined_dfs.items():
        # Filter the dataframe to include only rows with the specific gold label within the current type_folder
        filtered_df = combined_df[combined_df['gold_label'] == gold_label]
        
        # Calculate the frequency of the specific gold label
        frequency = len(filtered_df)
        
        # Output the frequency for the current type_folder
        print(f"For type_folder '{type_folder}', frequency of '{gold_label}': {frequency}")


def iaa_major_votes(group_data_df):
    """Defines the gold label, based on three annotator labels
    Three case:
        1 Absolute agreement: all three same label
        2 Partial agreement: two have the same label
        3 Asolute disagreement: all three have different labels
    Args:
     - path_to_file: path to file for a group of contradictions
     - 
    Return:
     - saves the data to a SNLI format with all annotator labels and gold
    """
    #define and save gold labels for each sentence pair to list
    sentence1 = group_data_df.loc[:,'sentence1']
    sentence2 = group_data_df.loc[:,'sentence2']
    annotator_labels = group_data_df.loc[:,'annotator_labels']
    
    gold_labels = []
    for entry in annotator_labels:
        if entry[0] == entry[1]:
            gold_labels.append(entry[0])
        elif entry[1] == entry[2]: 
            gold_labels.append(entry[1])
        elif entry[0] == entry[2]:
            gold_labels.append(entry[0])
        else:
            gold_labels.append('NA')
            
    data_d = {"sentence1": sentence1, "sentence2": sentence2, "annotator_labels": annotator_labels, "gold_label": gold_labels}
    data_df = pd.DataFrame(data=data_d)
    return data_df

def iaa_2lab_votes(group_data_df):
    """Defines the gold label, based on three annotator labels
    Args:
     - path_to_file: path to file for a group of contradictions
     - 
    Return:
     - saves the data to a SNLI format with all annotator labels and gold
     - saves only two labels: contradiction and not contradiction
    """
    #define and save gold labels for each sentence pair to list
    sentence1 = group_data_df.loc[:,'sentence1']
    sentence2 = group_data_df.loc[:,'sentence2']
    annotator_labels = group_data_df.loc[:,'annotator_labels']
    n_sentence1 = []
    n_sentence2 = []
    n_annotator_labels = []
    gold_labels = []
    for sent1, sent2, entry in zip(sentence1, sentence2, annotator_labels):
        if entry[0] == entry[1]:
            if "no contradiction" in entry[0]:
                gold_labels.append("no contradiction")
            else: 
                gold_labels.append("contradiction")
            n_sentence1.append(sent1)
            n_sentence2.append(sent2)
        elif entry[1] == entry[2]:
            if "no contradiction" in entry[1]:
                gold_labels.append("no contradiction")
            else: 
                gold_labels.append("contradiction")
            n_sentence1.append(sent1)
            n_sentence2.append(sent2)
        elif entry[0] == entry[2]:
            if "no contradiction" in entry[0]:
                gold_labels.append("no contradiction")
            else: 
                gold_labels.append("contradiction")
            n_sentence1.append(sent1)
            n_sentence2.append(sent2)

            
    data_d = {"sentence1": n_sentence1, "sentence2": n_sentence2, "annotator_labels": annotator_labels, "gold_label": gold_labels}
    data_df = pd.DataFrame(data=data_d)
    return data_df

def process_analysis(combined_dfs):
    for type_folder, combined_df in combined_dfs.items():
        # Count occurrences of 'NA' in the 'gold_label' column for each type_folder
        na_count = combined_df['gold_label'].value_counts().get('NA', 0)
        na_rows = combined_df[combined_df['gold_label'] == 'NA']
        
        # Save the filtered rows to a JSON file for the current type_folder
        output_file = f"na_rows_{type_folder}.json"
        na_rows.to_json(output_file, orient="records", lines=True)
        
        # Output the count for the current type_folder
        print(f"For type_folder '{type_folder}', 'NA' count: {na_count}")



def combine_df(path_to_data):
    combined_dfs = {}
    combined_2lab_dfs = {}
    for type_folder in os.listdir(path_to_data):
        type_path = os.path.join(path_to_data, type_folder)
        combined_df = pd.DataFrame()
        combined_2lab_df = pd.DataFrame()
        type_out_path = os.path.join(path_to_data, type_folder)
        for group_folder in os.listdir(type_path):
            group_path = os.path.join(type_path, group_folder)
            group_out_path = os.path.join(type_out_path, group_folder)
            for filename in os.listdir(group_path):
                if 'gold' not in filename:
                    file_path = os.path.join(group_path, filename)
                    group_data_df, group_data_bin = data_prep(file_path)
                    gold_data_df = iaa_major_votes(group_data_df)
                    gold_2lab_df = iaa_major_votes(group_data_bin)
                    
                    combined_df = pd.concat([combined_df, gold_data_df], axis=0)
                    combined_2lab_df = pd.concat([combined_2lab_df, gold_2lab_df], axis=0)
                    
            #output_file = os.path.join(group_out_path, f"gold_type_{type_folder}_group_{group_folder}.json")
            #gold_data_df.to_json(output_file, orient="records", lines=True)
            
            output_file = os.path.join("/scratch/informed_nlu/human_validated/combined_dfs", f"combined_df_{type_folder}.json")
            combined_df.to_json(output_file, orient="records", lines=True)
            
            output_2lab = os.path.join("/scratch/informed_nlu/human_validated/combined_dfs", f"comb_2lab_df_{type_folder}.json")
            combined_2lab_df.to_json(output_2lab, orient="records", lines=True)  
                

        combined_dfs[type_folder] = combined_df
        combined_2lab_dfs[type_folder] = combined_2lab_df

    return combined_dfs, combined_2lab_dfs

def read_combined_dfs(path_to_combined_dfs):
    combined_dfs = {}
    for file_name in os.listdir(path_to_combined_dfs):
        if file_name.endswith('.json'):
            type_folder = file_name.split('_')[2].split('.')[0]  # Extract type_folder from file name
            file_path = os.path.join(path_to_combined_dfs, file_name)
            combined_df = pd.read_json(file_path, orient="records", lines=True)
            combined_dfs[type_folder] = combined_df
    return combined_dfs
            
            
if __name__ == "__main__":
    group_data_df, group_data_bin = data_prep("/scratch/informed_nlu/human_validated/types_output/factive/1/type_factive_group_1.json")
    #group_data_gold = iaa_major_votes(group_data_df)
    combined_dfs, combined_2lab = combine_df("/scratch/informed_nlu/human_validated/types_output")
    #combined_dfs = read_combined_dfs("/scratch/informed_nlu/human_validated/combined_dfs")
    # Example usage:
    # Assuming combined_dfs is the dictionary returned by the main function
    #process_analysis(combined_dfs)
    print("Calculated IAA for factive, wk, structure and lexical types")
    compute_cohens_kappa(combined_dfs)
    calculate_kappa_alpha(combined_dfs)
    print("Calculated IAA for all contradictioons (two labels)")
    iaa_measure_bin(combined_2lab)
    
    #TODO: find a way to handle them , add more annotations
    #TODO: find a way to  visualize
    #calculate_gold_label_frequency(combined_dfs, 'factive contradiction')
    #calculate_gold_label_frequency(combined_dfs, 'other contradiction')
    
    # calculate_gold_label_frequency(combined_dfs, 'lexical contradiction')
    # print("___________________________________")
    # calculate_gold_label_frequency(combined_dfs, 'no contradiction')
    # print("___________________________________")
    # calculate_gold_label_frequency(combined_dfs, 'difficult to answer')
    # print("___________________________________")
    # calculate_gold_label_frequency(combined_dfs, 'structural contradiction')
    # print("___________________________________")
    # calculate_gold_label_frequency(combined_dfs, 'world knowledge contradiction')
