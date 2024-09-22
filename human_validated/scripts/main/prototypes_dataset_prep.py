import nltk
nltk.download('wordnet')
import json
import tqdm
import re
import csv
import stanza
import pandas as pd
import nltk
from nltk.corpus import wordnet as wn
from collections import Counter
import random
import numpy as np

       

def read_data(path, prototypes):
    """
    Read SNLI and prototypical data and output the lists of cleaned samples
    1. read data in
    2. remove samples with not defined gold labels
    3. save samples to list 
    Params:
     - path
     - prototypes: if prototypes count the number of contradictions and no contradictions
    """
    raw_data = []
    data = []
    for line in open(path, mode='r', encoding='utf-8'):   
        reader = json.loads(line)
        #line_lst = []
        # for k in reader.keys():
        #     #if k == 'gold_label' or k == 'sentence1' or k == 'sentence2':
            #line_lst.append({'gold_label': reader['gold_label'], 'sentence1': reader['sentence1'], 'sentence2':reader['sentence2']})
        if 'gold_label' in reader.keys():
            raw_data.append({'gold_label': reader['gold_label'], 'sentence1': reader['sentence1'], 'sentence2':reader['sentence2']})
        elif 'gold_labels' in reader.keys():
            raw_data.append({'gold_label': reader['gold_labels'], 'sentence1': reader['sentence1'], 'sentence2':reader['sentence2']})
    for line in raw_data:
        if line['gold_label'] != "-" and line['gold_label'] != "NA":
            data.append(line)
    if prototypes:
        contradictions_number = 0
        non_contradictions_number = 0
        for line in raw_data:
            if line['gold_label'] == "contradiction":
                contradictions_number += 1
            elif line['gold_label'] == "no contradiction":
                non_contradictions_number += 1
        return data, contradictions_number, non_contradictions_number
    return data

def read_bbc_data(path):
    """
    Read structural contradictions from BBC dataset
    and save to samples lists with sentence 1, sentence 2, and gold label
    """
    raw_data = []
    data = []
    with open(path, mode='r', encoding='utf-8') as file:
        reader = json.load(file)
    for item in reader:
            if str(item['contradiction_label']) == str(1):
                raw_data.append({
                    'gold_label': "contradiction", 
                    'sentence1': item['premise'], 
                    'sentence2': item['hypothese']
                })
                    
    for line in raw_data:
        if line['gold_label'] != "-" and line['gold_label'] != "NA":
            data.append(line)
    return data


def remove_contradictions(reduced_data, prototypes):
    """
    Remove contradicitons from the reduced SNLI
    the number of removed contradictions is equal to the length of prototypes list
    1. count the number of pretotypical contradictions 
    2. randomize the reduced data
    3. replace the SNLi contradictions with prototypical
    if there are any prototypical not contradictory samples replace 
    SNLI no contradictions with prototypical
    """
    prototypes_size = len(prototypes)
    contr_size = 0
    non_contr_size = 0
    
    for line in prototypes:
        if line['gold_label'] == 'contradiction':
            contr_size += 1
        elif line ['gold_label'] != 'contradiction':
            non_contr_size += 1
            
    random.shuffle(reduced_data)
    
    contr_count = 0
    non_contr_count = 0

    """for tiny datasets"""
    ## for tiny datasets
    # for line in reduced_data:
    #     if contr_count < prototypes_size:
    #         reduced_data.remove(line)
    #         contr_count += 1 
                
    for line in reduced_data:        
        if contr_count < contr_size:
            if line['gold_label'] == 'contradiction':            
                reduced_data.remove(line)
                contr_count += 1 
                
    #remove no contr for replacement with proto            
    for line in reduced_data:
        if non_contr_count < non_contr_size:
            if line['gold_label'] != 'contradiction':            
                reduced_data.remove(line)
                non_contr_count += 1  
                     
    return reduced_data

def reduce_balance_dataset(data, reduction_fraction):
    """
    Reduces and balances SNLI dataset, prepares smaller datasets for training transformers
    Params:
     - data: cleaned SNLI data without undefined labels --> total size of cleaned SNLi is 549367
     - reduction fraction: the desired percentage of the result dataset size --> 
     eg: if 0.3, the resulting dataset is 30% of the original SNLi
    Return:
     - the dataset of reduced size

    """
    total_size = len(data)
    target_size = int(total_size * reduction_fraction)
    # Count the occurrences of each label in the data
    label_counts = Counter(line['gold_label'] for line in data)
    
    # Calculate the number of elements to keep for each label
    keep_counts = {label: int(count * reduction_fraction)+1 for label, count in label_counts.items()}
    #print(keep_counts)
    # Create a new list to store the reduced and balanced data
    reduced_data = []
    
    # Track how many elements have been kept for each label
    kept_counts = {label: 0 for label in label_counts}
    
    for line in data:
        label = line['gold_label']
        if kept_counts[label] < keep_counts[label]:
            #print(keep_counts[label])
            reduced_data.append(line)
            kept_counts[label] += 1
    
    return reduced_data[:target_size]

def label_count(data):
    label_counts = {'entailment': 0, 'neutral': 0, 'contradiction':0}
    for line in data:
        label = line.get('gold_label')
        if label in label_counts:
            label_counts[label] += 1
    return label_counts
    
def reduce_dataset(data, reduction_fraction):
    """
    Reduces dataset to the desired size
    Params:
     - data: cleaned SNLI data without undefined labels --> total size of cleaned SNLi is 549367
     - reduction fraction: the desired percentage of the result dataset size --> 
     eg: if 0.3, the resulting dataset is 30% of the original SNLi
    Return:
     - the dataset of reduced size
    """
    total_size = len(data)
    target_size = int(total_size * reduction_fraction)
    
    # shuffle the data
    random.shuffle(data)
    
    # select the target size from the shuffled data
    reduced_data = data[:target_size]
    
    return reduced_data


def add_prototypes(data, prototypes, reduced_size):
    """
    Replaces the contradictions from the reduced SNLI with protoypical contradicitons
    1. reduces the dataset size. Optional: balances and reduces the data
    2. replaces the contradictions from SNLi with prototypical
    """
    """comment out for smaller datasets to ensure the reduced datasets are balanced"""
    #reduced_balanced_snli = reduce_balance_dataset(data, reduced_size)
    reduced_balanced_snli = reduce_dataset(data, reduced_size)
    removed_contr_data = remove_contradictions(reduced_balanced_snli, prototypes)

    return removed_contr_data, prototypes


def save_to_json(data, file_path):
    """
    Saves prepared data to JSON file
    """
    with open(file_path, 'w') as file:
        for item in data:
            json_str = json.dumps(item)
            file.write(json_str + "\n")


def shuffle_and_split(data, train_ratio=0.8, dev_ratio=0.1, test_ratio=0.1):
    """
    Shuffle the data and split it into training, development, and test sets.

    Parameters:
    data (numpy.ndarray): The data to be shuffled and split.
    train_ratio (float): The proportion of data to be used for training (default is 0.8).
    dev_ratio (float): The proportion of data to be used for development (default is 0.1).
    test_ratio (float): The proportion of data to be used for testing (default is 0.1).

    Returns:
    tuple: A tuple containing the training, development, and test sets.
    """
    
    labels = list(set([entry["gold_label"] for entry in data]))
    
    label_dict = {label: i for i, label in enumerate(labels)}
    
    if not np.isclose(train_ratio + dev_ratio + test_ratio, 1.0):
        raise ValueError("The sum of train_ratio, dev_ratio, and test_ratio must be 1.")
    
    # Shuffle the data
    np.random.shuffle(data)
    
    # Split the data
    total_size = len(data)
    train_end = int(train_ratio * total_size)
    dev_end = train_end + int(dev_ratio * total_size)
    
    train_data = data[:train_end]
    dev_data = data[train_end:dev_end]
    test_data = data[dev_end:]
    
    return train_data, dev_data, test_data, label_dict




if __name__=="__main__":
    data = read_data("/shared_with_maren/contradiction_detection/data/raw/snli_data_original/tokenized_format/snli_train_pos_dep.json", prototypes = False)
    val_data = read_data("/shared_with_maren/contradiction_detection/data/raw/snli_data_original/tokenized_format/snli_dev_pos_dep.json", prototypes = False)
    test_data = read_data("/shared_with_maren/contradiction_detection/data/raw/snli_data_original/tokenized_format/snli_test_pos_dep.json", prototypes = False)
    
    #prototypes, c_n, nc_n = read_data("/scratch/contradiction_detection/contradiction_detection/data/all_prototypes.json", prototypes = True)
    prototypes, c_n, nc_n = read_data("/scratch/contradiction_detection/contradiction_detection/data/all+noun_antonyms.json", prototypes=True)
    rte_prototypes = read_data("/cluster/svetlana/data/rte_real_life_contradictions.json", prototypes=False)
    bbc_structural = read_bbc_data("/cluster/svetlana/data/bbc_news.json")
    reduction_fraction = 0.3  # Reduce to 90% of the original size
    reduced_data = reduce_dataset(data, reduction_fraction=0.002)
    reduced_data_balance = reduce_balance_dataset(data, reduction_fraction=0.2)
    proto_rte = prototypes+rte_prototypes
    #proto_rte = prototypes+rte_prototypes+bbc_structural
    snli_data, proto_data = add_prototypes(data, proto_rte, reduced_size=0.2)
    #snli_data, proto_data = add_prototypes(data, prototypes, reduced_size=0.1)
    mix = snli_data+proto_data
    save_to_json(mix, "/cluster/svetlana/data/reduced_snli+prototypes+rte+noun_ants_0.2_snli_1.json")
    #save_to_json(reduced_data_balance, "/cluster/svetlana/data/reduced_snli_original_0.2.json")

