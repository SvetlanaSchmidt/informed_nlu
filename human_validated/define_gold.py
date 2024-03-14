import os
import json
import csv
import pandas as pd
import numpy as np
from sklearn.metrics import cohen_kappa_score
from krippendorff import alpha
from statsmodels.stats.inter_rater import fleiss_kappa, aggregate_raters
from sklearn.preprocessing import LabelEncoder
from utils import observed_agreement_matrix, expected_agreement_matrix, observed_disagreement_matrix, expected_disagreement_matrix, coincidence_matrix

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
        
    label_list = clean_labels(label_list)
    data_d = {"sentence1": sentence1_list, "sentence2": sentence2_list, "annotator_labels": label_list}
    data_df = pd.DataFrame(data=data_d)
    return data_df

def clean_labels(annotaions_list):
    cleaned_annotaions = []
    for pair in annotaions_list:
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
        cleaned_annotaions.append(clean_pair)
                
    return cleaned_annotaions

def transform_annotator_labels(row):
    annotator_labels = row['annotator_labels']
    annotator_1 = annotator_labels[0] if len(annotator_labels) >= 1 else None
    annotator_2 = annotator_labels[1] if len(annotator_labels) >= 2 else None
    annotator_3 = annotator_labels[2] if len(annotator_labels) >= 3 else None
    return pd.Series({'annotator_1': annotator_1, 'annotator_2': annotator_2, 'annotator_3': annotator_3})

def preprocess_annotations(combined_df):
    # Apply the transformation function to each row to create new annotator columns
    new_annotator_cols = combined_df.apply(transform_annotator_labels, axis=1)
    
    # Concatenate the new annotator columns with the original dataframe
    combined_df = pd.concat([combined_df, new_annotator_cols], axis=1)
    
    return combined_df

def compute_cohens_kappa(combined_dfs):
    for type_folder, combined_df in combined_dfs.items():
        # Preprocess annotations for the current dataframe
        combined_df = preprocess_annotations(combined_df)
        print(combined_df)
        # Compute Cohen's kappa between annotators
        kappa_1_2 = cohen_kappa_score(combined_df['annotator_1'], combined_df['annotator_2'])
        kappa_1_3 = cohen_kappa_score(combined_df['annotator_1'], combined_df['annotator_3'])
        kappa_2_3 = cohen_kappa_score(combined_df['annotator_2'], combined_df['annotator_3'])
        
        # Output the computed kappas for the current type_folder
        print(f"For type_folder '{type_folder}':")
        print(f"Cohen's kappa between annotators 1 and 2: {kappa_1_2}")
        print(f"Cohen's kappa between annotators 1 and 3: {kappa_1_3}")
        print(f"Cohen's kappa between annotators 2 and 3: {kappa_2_3}")
        print()
        
def label_encode(annotations_df, type_folder):
    if type_folder == 'factive':
        labels_dict  = {"no contradiction":0, "factive contradiction":1, "other contradiction":2,"difficult to answer":3}
    annotations_numeric = []
    for pair_annotations in annotations_df:
        numeric_pair = []
        for annotaion in pair_annotations:
            pair_annotations_numeric = labels_dict[annotaion]
            numeric_pair.append(pair_annotations_numeric)
        annotations_numeric.append(numeric_pair)
    return annotations_numeric

def scotts_pi(observed_agreement_matrix):
    # Total number of ratings
    n_ratings = np.sum(observed_agreement_matrix)
    
    # Observed proportion of agreement
    P_o = np.trace(observed_agreement_matrix) / n_ratings
    
    # Expected proportion of agreement by chance
    marginal_probs = np.sum(observed_agreement_matrix, axis=0) / n_ratings
    P_e = np.sum(marginal_probs ** 2)
    
    # Scott's Pi
    pi = (P_o - P_e) / (1 - P_e)
    return pi

def bennets_s(observed_agreement_matrix, cat_num = 4):
    # Total number of ratings
    n_ratings = np.sum(observed_agreement_matrix)
    
    # Observed proportion of agreement
    P_o = np.trace(observed_agreement_matrix) / n_ratings

    # Scott's Pi
    s = (P_o - 1/cat_num) / (1 - 1/cat_num)
    return s

def calculate_kappa_alpha(combined_dfs):
    for type_folder, combined_df in combined_dfs.items():
        #comment out, extend for all types
        if type_folder == 'factive':
            # Preprocess annotations for the current dataframe
            combined_df = preprocess_annotations(combined_df)
            #print(combined_df[['annotator_1', 'annotator_2', 'annotator_3']])
            # Calculate Fleiss' kappa
            annotations = combined_df[['annotator_1', 'annotator_2', 'annotator_3']].values.tolist()
            numeric_annotations = label_encode(annotations, type_folder)
            #print(annotations_numeric)
            # Convert list of lists to numpy array
            annotations_numeric_array = aggregate_raters(numeric_annotations, n_cat = None)
                
            #print(annotations)    
            print(numeric_annotations)
            print(annotations_numeric_array[0].shape)
            fleiss_k = fleiss_kappa(annotations_numeric_array[0], method = 'fleiss')
            #fleiss_k = fleiss_kappa(combined_df[['annotator_1', 'annotator_2', 'annotator_3']])
            
            # Calculate Krippendorff's alpha
            #kripp_alpha = alpha(combined_df[['annotator_1', 'annotator_2', 'annotator_3']])
            kripp_alpha = alpha(annotations_numeric_array[0])

            
            # Output the computed kappa and alpha for the current type_folder
            print(f"For type_folder '{type_folder}':")
            print(f"Fleiss' kappa: {fleiss_k}")
            print(f"Krippendorff's alpha: {kripp_alpha}")
            print()

                        
            P_o = observed_agreement_matrix(annotations)
            P_e = expected_agreement_matrix(annotations)
            D_o = observed_disagreement_matrix(annotations)
            D_e = expected_disagreement_matrix(annotations) 
            c_m = coincidence_matrix(annotations)
            
            
            k_a = 1.0 - (np.sum(D_o) / np.sum(D_e))
                      
            pi = scotts_pi(P_o)
            s = bennets_s(P_o)
            print(f"For type_folder '{type_folder}':")
            print(f"Scott's pi: {pi}")
            print(f"For type_folder '{type_folder}':")
            print(f"Bennette s S: {s}")
            print(f"Krippendorffs alpha 2.0: {k_a}")
            return c_m
            

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
    group_data_df = data_prep("/scratch/informed_nlu/human_validated/types_output/factive/1/type_factive_group_1.json")
    group_data_gold = iaa_major_votes(group_data_df)
    combined_dfs=combine_df("/scratch/informed_nlu/human_validated/types_output")

    #combined_dfs = read_combined_dfs("/scratch/informed_nlu/human_validated/combined_dfs")
    # Example usage:
    # Assuming combined_dfs is the dictionary returned by the main function
    process_analysis(combined_dfs)
    compute_cohens_kappa(combined_dfs)
    c_m = calculate_kappa_alpha(combined_dfs)
    #TODO: find a way to handle them , add more annotations
    #TODO: find a way to  visualize
    #calculate_gold_label_frequency(combined_dfs, 'factive contradiction')
    #calculate_gold_label_frequency(combined_dfs, 'other contradiction')
    calculate_gold_label_frequency(combined_dfs, 'lexical contradiction')
    print("___________________________________")
    calculate_gold_label_frequency(combined_dfs, 'no contradiction')
    print("___________________________________")
    calculate_gold_label_frequency(combined_dfs, 'difficult to answer')
    print("___________________________________")
    calculate_gold_label_frequency(combined_dfs, 'structural contradiction')
    print("___________________________________")
    calculate_gold_label_frequency(combined_dfs, 'world knowledge contradiction')
