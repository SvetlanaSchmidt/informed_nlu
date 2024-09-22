import os
import json
import csv
import pandas as pd
import numpy as np
from sklearn.metrics import cohen_kappa_score
from krippendorff import alpha
from statsmodels.stats.inter_rater import fleiss_kappa, aggregate_raters
from sklearn.preprocessing import LabelEncoder
from human_validated.scripts.main.validated_proto_utils.utils import coincidence_matrix_from_reliability, observed_agreement_matrix, expected_agreement_matrix, observed_disagreement_matrix, expected_disagreement_matrix, coincidence_matrix, reliability_matrix
from human_validated.scripts.main.validated_proto_utils.iaa_measure import preprocess_annotations


def compute_fleiss_kappa(combined_dfs, n_categories):
    # Initialize variables to store observed and expected agreements
    observed_agreements = np.zeros(n_categories)
    expected_agreements = np.zeros(n_categories)
    n_total = 0
    
    for type_folder, combined_df in combined_dfs.items():
        # Preprocess annotations for the current dataframe
        combined_df = preprocess_annotations(combined_df)
        n_total += len(combined_df)
        
        # Compute observed agreement for each category
        observed_agreement_matrix = np.zeros((n_categories, n_categories))
        for category in range(n_categories):
            for annotator in range(1, 4):  # Assuming 3 annotators
                annotator_labels = combined_df[f'annotator_{annotator}']
                category_counts = np.sum(annotator_labels == category, axis=0)
                observed_agreement_matrix[category, annotator - 1] = category_counts

        observed_agreements += np.sum(observed_agreement_matrix ** 2 - len(combined_df), axis=1) / (len(combined_df) * (len(combined_df) - 1))
        
        # Compute expected agreement for each category
        p_j = np.sum(observed_agreement_matrix, axis=0) / (len(combined_df) * 3)
        expected_agreements += np.sum(p_j ** 2, axis=0)
    
    # Compute Fleiss' kappa for each category
    fleiss_kappas = (observed_agreements - expected_agreements) / (1 - expected_agreements)
    
    return fleiss_kappas, n_total


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
