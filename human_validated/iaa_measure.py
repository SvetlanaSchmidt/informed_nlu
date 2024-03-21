import os
import json
import csv
import pandas as pd
import numpy as np
from sklearn.metrics import cohen_kappa_score
from krippendorff import alpha
from statsmodels.stats.inter_rater import fleiss_kappa, aggregate_raters
from sklearn.preprocessing import LabelEncoder
from utils import coincidence_matrix_from_reliability, observed_agreement_matrix, expected_agreement_matrix, observed_disagreement_matrix, expected_disagreement_matrix, coincidence_matrix, reliability_matrix


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

def label_encode(annotations_df):
    labels_dict  = {"no contradiction":0, "factive contradiction":1, "other contradiction":2,"difficult to answer":3, "lexical contradiction":4, "structural contradiction":5, "world knowledge contradiction":6}
    annotations_numeric = []
    for pair_annotations in annotations_df:
        numeric_pair = []
        for annotation in pair_annotations:
            pair_annotations_numeric = labels_dict[annotation]
            numeric_pair.append(pair_annotations_numeric)
        annotations_numeric.append(numeric_pair)
    return annotations_numeric

def label_encode_bin(annotations_df):
    labels_dict  = {"no contradiction":0, "contradiction":1}
    annotations_numeric = []
    for pair_annotations in annotations_df:
        numeric_pair = []
        for annotation in pair_annotations:
            pair_annotations_numeric = labels_dict[annotation]
            numeric_pair.append(pair_annotations_numeric)
        annotations_numeric.append(numeric_pair)
    return annotations_numeric

def calculate_kappa_alpha(combined_dfs):
    for type_folder, combined_df in combined_dfs.items():
        #comment out, extend for all types
        # Preprocess annotations for the current dataframe
        combined_df = preprocess_annotations(combined_df)
        #print(combined_df[['annotator_1', 'annotator_2', 'annotator_3']])
        # Calculate Fleiss' kappa
        annotations = combined_df[['annotator_1', 'annotator_2', 'annotator_3']].values.tolist()
        numeric_annotations = label_encode(annotations)
        #print(annotations_numeric)
        # Convert list of lists to numpy array
        annotations_numeric_array = aggregate_raters(numeric_annotations, n_cat = None)
            
        #print(annotations)    
        #print(numeric_annotations)
        #print(annotations_numeric_array[0].shape)
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
        #c_m = coincidence_matrix(annotations)
        #r_m = reliability_matrix(annotations)
        #c_m = coincidence_matrix_from_reliability(r_m)
        
                    
        pi = scotts_pi(P_o)
        s = bennets_s(P_o)
        print(f"For type_folder '{type_folder}':")
        print(f"Scott's pi: {pi}")
        print(f"For type_folder '{type_folder}':")
        print(f"Bennette s S: {s}")


def iaa_measure_bin(combined_dfs):
    combined_2lab_df = pd.DataFrame()
    for type_folder, combined_df in combined_dfs.items():
        combined_2lab_df = pd.concat([combined_2lab_df, combined_df], axis=0)
    combined_2lab_dfs = preprocess_annotations(combined_2lab_df)
    #print(combined_df[['annotator_1', 'annotator_2', 'annotator_3']])
    # Calculate Fleiss' kappa
    annotations = combined_2lab_dfs[['annotator_1', 'annotator_2', 'annotator_3']].values.tolist()
    numeric_annotations = label_encode_bin(annotations)
    #print(annotations_numeric)
    # Convert list of lists to numpy array
    annotations_numeric_array = aggregate_raters(numeric_annotations, n_cat = None)
        
    #print(annotations)    
    #print(numeric_annotations)
    #print(annotations_numeric_array[0].shape)
    fleiss_k = fleiss_kappa(annotations_numeric_array[0], method = 'fleiss')
    #fleiss_k = fleiss_kappa(combined_df[['annotator_1', 'annotator_2', 'annotator_3']])
    
    # Calculate Krippendorff's alpha
    kripp_alpha = alpha(annotations_numeric_array[0])

    
    # Output the computed kappa and alpha for the current type_folder
    print(f"Fleiss' kappa: {fleiss_k}")
    print(f"Krippendorff's alpha: {kripp_alpha}")
    print()

                
    P_o = observed_agreement_matrix(annotations)
    P_e = expected_agreement_matrix(annotations)
    D_o = observed_disagreement_matrix(annotations)
    D_e = expected_disagreement_matrix(annotations) 
    
    
                
    pi = scotts_pi(P_o)
    s = bennets_s(P_o)
    print(f"Scott's pi: {pi}")
    print(f"Bennette s S: {s}")
    print(f"Krippendorffs alpha 2.0: {k_a}")
        
        

def compute_cohens_kappa(combined_dfs):
    for type_folder, combined_df in combined_dfs.items():
        # Preprocess annotations for the current dataframe
        combined_df = preprocess_annotations(combined_df)
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