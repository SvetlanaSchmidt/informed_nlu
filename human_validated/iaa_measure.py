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
    """prepare the annotations for IAA computation
    """
    # transform each row to create new annotator columns
    new_annotator_cols = combined_df.apply(transform_annotator_labels, axis=1)
    
    # concatenate the new annotator columns with the original dataframe
    combined_df = pd.concat([combined_df, new_annotator_cols], axis=1)  
    return combined_df


def calculate_kappa_alpha(combined_dfs):
    """Compute Fleiss kappa and Krippendorff's alpha among three annotations in each contradiction type
    Params:
     - combined dataframe with 4 contradiction types dataframes
    return:
     - outputs the Kappa and alpha computed within a contradiction type
    """

    for type_folder, combined_df in combined_dfs.items():
        # prepare annotations for the current dataframe
        combined_df = preprocess_annotations(combined_df)
        annotations = combined_df[['annotator_1', 'annotator_2', 'annotator_3']].values.tolist()
        
        #adjust the shape of input array for krippendorff alpha
        annotations_T = np.array(annotations).transpose()
        #prepare input for fleiss kappa
        annotations_array = aggregate_raters(annotations, n_cat = None)
            
        #Fleiss Kappa
        fleiss_k = fleiss_kappa(annotations_array[0], method = 'fleiss')
        
        #Krippendorff's alpha
        kripp_alpha = alpha(annotations_T, level_of_measurement="nominal")
                                
        print(f"For type_folder '{type_folder}':")
        print(f"Fleiss' kappa: {fleiss_k}")
        print(f"Krippendorff's alpha: {kripp_alpha}")
        
    # fleiss_kappas, n_total = compute_fleiss_kappa(combined_dfs, n_categories)
    # print("Fleiss' Kappas for each category:", fleiss_kappas)
        

def iaa_measure_bin(combined_dfs):
    """calculate IAA for annotated data with labels converted to: contradiction - no contradiction
    params:
     - dataframe with annotated and gold labels combined of 4 types
    output:
     - Fleiss Kappa
     - Kripp alpha 
     - Cohens kappa between annotations pairs
    """
    combined_2lab_df = pd.DataFrame()
    for type_folder, combined_df in combined_dfs.items():
        combined_2lab_df = pd.concat([combined_2lab_df, combined_df], axis=0)
    combined_2lab_dfs = preprocess_annotations(combined_2lab_df)

    
    annotations = combined_2lab_dfs[['annotator_1', 'annotator_2', 'annotator_3']].values.tolist()
    annotations_T = np.array(annotations).transpose()
    annotations_numeric_array = aggregate_raters(annotations, n_cat = None)
    # Fleiss' kappa
    fleiss_k = fleiss_kappa(annotations_numeric_array[0], method = 'fleiss')
    
    # Krippendorff's alpha
    kripp_alpha = alpha(annotations_T, level_of_measurement="nominal")
    
    # Output the computed kappa and alpha for the current type_folder
    print("IAA for three annotators, for 2 labels: contradiction, no contradiction")
    print(f"Fleiss' kappa: {fleiss_k}")
    print(f"Krippendorff's alpha: {kripp_alpha}")       
    
    annotator_1 = combined_2lab_dfs['annotator_1'].values
    annotator_2 = combined_2lab_dfs['annotator_2'].values
    annotator_3 = combined_2lab_dfs['annotator_3'].values
    
    
    kappa_1_2 = cohen_kappa_score(annotator_1, annotator_2)
    kappa_1_3 = cohen_kappa_score(annotator_1, annotator_3)
    kappa_2_3 = cohen_kappa_score(annotator_2, annotator_3)
    
    # Output the computed kappas for the current type_folder
    print("IAA for combined dataframe for two labels: contradiction vs no contradiction")
    print(f"Cohen's kappa between annotators 1 and 2: {kappa_1_2}")
    print(f"Cohen's kappa between annotators 1 and 3: {kappa_1_3}")
    print(f"Cohen's kappa between annotators 2 and 3: {kappa_2_3}")
    print()

         
        

def compute_cohens_kappa(combined_dfs):
    """Calculate Cohen's kappa between pairs of annotaions and 
    percent agreement between pairs of annotations. 
    Percent agreement is computed from the mean of the sum of all cases two annotators agreed on the label
    Params:
     - dataframe annotated and with defined gold labels combined from 4 types dataframes 
    Output:
     - Cohen' kappa
     - Percent agreement
    """
    for type_folder, combined_df in combined_dfs.items():
        # Preprocess annotations for the current dataframe
        combined_df = preprocess_annotations(combined_df)
        # Compute Cohen's kappa between annotators
        
        annotator_1 = combined_df['annotator_1'].values
        annotator_2 = combined_df['annotator_2'].values
        annotator_3 = combined_df['annotator_3'].values
    
        kappa_1_2 = cohen_kappa_score(annotator_1, annotator_2)
        kappa_1_3 = cohen_kappa_score(annotator_1, annotator_3)
        kappa_2_3 = cohen_kappa_score(annotator_2, annotator_3)
        
        percent_agreement_1_2 = (annotator_1==annotator_2).mean()
        percent_agreement_1_3 = (annotator_1==annotator_3).mean()
        percent_agreement_2_3 = (annotator_2==annotator_3).mean()

        
        # Output the computed kappas for the current type_folder
        print(f"For type_folder '{type_folder}':")
        print(f"Cohen's kappa between annotators 1 and 2: {kappa_1_2}")
        print(f"Cohen's kappa between annotators 1 and 3: {kappa_1_3}")
        print(f"Cohen's kappa between annotators 2 and 3: {kappa_2_3}")
        print()
        print(f"Agreement between annotators 1 and 2: {percent_agreement_1_2}")
        print(f"Agreement between annotators 1 and 3: {percent_agreement_1_3}")
        print(f"Agreement between annotators 2 and 3: {percent_agreement_2_3}")
        print()


