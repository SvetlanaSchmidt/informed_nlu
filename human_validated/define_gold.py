import os
import json
import csv
import pandas as pd


def data_prep(group_data_path):
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

    data_d = {"sentence1": sentence1_list, "sentence2": sentence2_list, "annotator_labels": label_list}
    data_df = pd.DataFrame(data=data_d)
    return data_df

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
            
    data_d = {"sentence1": sentence1, "sentence2": sentence2, "annotator_labels": annotator_labels,"gold_label": gold_labels}
    data_df = pd.DataFrame(data=data_d)
    return data_df

def iaa_ind_votes():
    """Defines the gold label, based on three annotator labels
    Args:
     - path_to_file: path to file for a group of contradictions
     - 
    Return:
     - saves the data to a SNLI format with all annotator labels and gold
    """
    pass

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
    for type_folder in os.listdir(path_to_data):
        type_path = os.path.join(path_to_data, type_folder)
        combined_df = pd.DataFrame()
        type_out_path = os.path.join(path_to_data, type_folder)
        for group_folder in os.listdir(type_path):
            group_path = os.path.join(type_path, group_folder)
            group_out_path = os.path.join(type_out_path, group_folder)
            for filename in os.listdir(group_path):
                if 'gold' not in filename:
                    file_path = os.path.join(group_path, filename)
                    group_data_df = data_prep(file_path)
                    gold_data_df = iaa_major_votes(group_data_df)
                    
                    combined_df = pd.concat([combined_df, gold_data_df], axis=0)
            #output_file = os.path.join(group_out_path, f"gold_type_{type_folder}_group_{group_folder}.json")
            #gold_data_df.to_json(output_file, orient="records", lines=True)
            
            output_file = os.path.join("/scratch/informed_nlu/human_validated/combined_dfs", f"combined_df_{type_folder}.json")
            combined_df.to_json(output_file, orient="records", lines=True)    

        combined_dfs[type_folder] = combined_df

    return combined_dfs
            
            
if __name__ == "__main__":
    group_data_df = data_prep("/scratch/informed_nlu/human_validated/types_output/factive/1/type_factive_group_1.json")
    group_data_gold = iaa_major_votes(group_data_df)
    combined_dfs=combine_df("/scratch/informed_nlu/human_validated/types_output")
    #TODO: connect all groups for one type together
    #TODO: count all NA
    # Example usage:
    # Assuming combined_dfs is the dictionary returned by the main function
    process_analysis(combined_dfs)
    #TODO: find a way to handle them , add more annotations
    #TODO: find a way to  visualize