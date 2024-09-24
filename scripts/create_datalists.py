import nltk
nltk.download('wordnet')
import json
import tqdm
import re
import stanza
import pandas as pd
import nltk
from nltk.corpus import wordnet as wn
from informed_nlu.utils.disambig import *

stanza.download('en')

"""Developed by Svetlana Schmidt"""       
 
def read_data(path):
    """save the sentence pairs and labels from SNLI to list of lists
    """
    data = []

    for line in open(path, mode='r', encoding='utf-8'):   
        reader = json.loads(line)
        line_lst = []
        for k in reader.keys():
            if k == 'gold_label' or k == 'sentence1' or k == 'sentence2' or k == 'sentence1_tokenized' or k == 'sentence2_tokenized' or k == 'sentence1_pos' or k == 'sentence2_pos':
                line_lst.append(reader[k])
        data.append(line_lst)
    return data

def extract_dep(data, nlp):
    """
    Parse the premises of SNLI corpus with Stanza parser and extract the POS, dependencies, and morphological features
    """
    sent1 = []
    sent1_tok = []
    sent1_pos = []
    deps1 = []
    features1 = []
    for sentence_pair in tqdm.tqdm(data):
        sentence_1_prep = sentence_pair[1]
        if sentence_1_prep not in sent1:
            sent1.append(sentence_1_prep)
            pos1 = sentence_pair[5]
            sent1_pos.append(pos1)
            premise_tok = []
            dep = []
            feat = []
            doc = nlp(sentence_1_prep)
            for sent in doc.sentences:
                for token in sent.words:
                    premise_tok.append(token.text)
                    dep.append(token.deprel)
                    feat.append(token.feats)
                    
            sent1_tok.append(premise_tok)
            deps1.append(dep)
            features1.append(feat)
        
    return sent1, sent1_tok, sent1_pos, deps1, features1

def write_data_file(path, nlp, data_labeled):
    sent1, sent1_tok, sent1_pos, deps1, features1 = extract_dep(data_labeled, nlp)
    dict_synsets = {'sentence1': sent1, 'premise_tok': sent1_tok, 'sent1_pos': sent1_pos, 'sent1_deps': deps1, 'sent1_features':features1}
    df = pd.DataFrame.from_dict(dict_synsets)
    df.to_json(path_or_buf=path, orient="records", lines=True)
   
   
if __name__ == "__main__":
    
    train_file = "/cluster/svetlana/data/snli_train_pos_dep.json"
    val_file = "/cluster/svetlana/data/snli_dev_pos_dep.json"
    test_file = "/cluster/svetlana/data/snli_test_pos_dep.json"
    
    train_data = read_data(train_file)
    val_data = read_data(val_file)
    test_data = read_data(test_file)
    
    #sent = train_data[0][1]
    nlp = stanza.Pipeline('en')
    
    #parse sentences, add dependencies and features
    train_deps = write_data_file('train_deps.json', nlp, train_data[:10000])
    val_deps = write_data_file('val_deps.json', nlp, val_data[:5000])
    test_deps = write_data_file('test_deps.json', nlp, test_data[:5000])
      
    #disambiguate parsed sentences
    train_samples = []
    val_samples = []
    test_samples = []
    with open("train_deps.json", "r") as f_t:
        for line in f_t:
            train_samples.append(json.loads(line))
            
    with open("val_deps.json", "r") as f_d:
        for line in f_d:
            val_samples.append(json.loads(line))
            
    with open("test_deps.json", "r") as fp:
        for line in fp:
            test_samples.append(json.loads(line))
            
    print("Parsing of dependencies and morphologic features is complete")
    
    up_train = disambig(train_samples, path = "train_deps_syn.json")
    up_dev = disambig(val_samples, path = "val_deps_syn.json")
    up_test = disambig(test_samples, path = "test_deps_syn.json")
    
    print("Disambiguation of sentences is complete")
    
