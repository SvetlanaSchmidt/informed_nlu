import nltk
nltk.download('wordnet')
import json
import tqdm
import re
import csv
import pandas as pd
from nltk.corpus import wordnet as wn

synsets_list = []
for syn in list(wn.all_synsets()):
    synsets_list.append(syn)

with open ('vocab.txt', 'w') as f:
    for synset in synsets_list:
        f.write(str(synset).split("(")[-1][:-1].replace(".", "_"))
        f.write('\n')
        
#add paths to your SNLI data
train_file = ""
val_file = ""
test_file = ""

def read_data(path):
    data = []

    for line in open(path, mode='r', encoding='utf-8'):
   
        reader = json.loads(line)
        line_lst = []
        for k in reader.keys():
            if k == 'gold_label' or k == 'sentence1' or k == 'sentence2' or k == 'sentence1_pos' or k == 'sentence2_pos':
                line_lst.append(reader[k])
        data.append(line_lst)
    return data

train_data = read_data(train_file)
val_data = read_data(val_file)
test_data = read_data(test_file)

def get_hypernyms(data_labeled):
    labels = []
    sent1 = []
    sent2 = []
    premise = []
    hypothesis = []
    hypernyms1 = []
    hypernyms2 = []
    for sentence_pair in tqdm.tqdm(data_labeled):
        # punctuation and digit removal
        sentence_1_prep = re.sub(r'[^\w\s]',' ', sentence_pair[1])
        print(sentence_pair[1])
        sentence_2_prep = re.sub(r'[^\w\s]',' ', sentence_pair[2])
        sentence_1_prep = re.sub(r'[0-9]+', ' ', sentence_1_prep)
        sentence_2_prep = re.sub(r'[0-9]+', ' ', sentence_2_prep)
        sentence_1_prep = " ".join(sentence_1_prep.split())
        sentence_2_prep = " ".join(sentence_2_prep.split())
        
        sent1.append(sentence_1_prep)
        sent2.append(sentence_2_prep)
        hyper_sent1 = []
        premise_tok = []
        for word in sentence_1_prep.split(" "):
            premise_tok.append(word)
            if len(wn.synsets(word)) > 0:
                synset = wn.synsets(word)[0]
                if len(synset.hypernyms()) > 0:
                    hypernym = synset.hypernyms()[0]
                    hyper_sent1.append(str(hypernym).split("(")[-2][:-2].replace(".", "_"))
            else:
                hyper_sent1.append("no_hypernym")
        
        
        hyper_sent2 = []
        hypothesis_tok = []
        for word in sentence_2_prep.split(" "):
            hypothesis_tok.append(word)
            if len(wn.synsets(word)) > 0:
                synset = wn.synsets(word)[0]
                if len(synset.hypernyms()) > 0:
                    hypernym = synset.hypernyms()[0]
                    hyper_sent2.append(str(hypernym).split("(")[-2][:-2].replace(".", "_"))
            else:
                hyper_sent2.append("no_hypernym")
        

        labels.append(sentence_pair[0])
        hypernyms1.append(hyper_sent1)
        hypernyms2.append(hyper_sent2)
        premise.append(premise_tok)
        hypothesis.append(hypothesis_tok)
            
        
    return labels, sent1, sent2, premise, hypothesis, hypernyms1, hypernyms2

def get_synonym_corpus(data_labeled):
    pos_lookup = ["NOUN", "VERB", "ADJ", "ADV"]
    labels = []
    sent1 = []
    sent2 = []
    premise = []
    hypothesis = []
    sent1_syn = []
    sent2_syn = []
    for sentence_pair in tqdm.tqdm(data_labeled):
        #punctuation and digit removal
        sentence_1_prep = re.sub(r'[^\w\s]',' ', sentence_pair[1])
        sentence_2_prep = re.sub(r'[^\w\s]',' ', sentence_pair[2])
        sentence_1_prep = re.sub(r'[0-9]+', ' ', sentence_1_prep)
        sentence_2_prep = re.sub(r'[0-9]+', ' ', sentence_2_prep)
        sentence_1_prep = " ".join(sentence_1_prep.split())
        sentence_2_prep = " ".join(sentence_2_prep.split())
        pos1 = sentence_pair[3]
        pos2 = sentence_pair[4]
        sent1.append(sentence_1_prep)
        sent2.append(sentence_2_prep)

        sentence_1_new = []
        premise_tok = []
        for word, pos in zip(sentence_1_prep.split(" "), pos1):
            if pos in pos_lookup:
                premise_tok.append(word)
                if len(wn.synsets(word)) > 0:
                    synset = wn.synsets(word)[0]
                    syn = (str(synset).split("(")[-1][:-1].replace(".", "_"))
                    sentence_1_new.append(syn.strip("'"))
                else:
                    sentence_1_new.append("no_syn")
            else: 
                sentence_1_new.append("no_syn")
                    
        
        sentence_2_new = []
        hypothesis_tok = []
        for word, pos in zip(sentence_2_prep.split(" "), pos2):
            if pos in pos_lookup:
                hypothesis_tok.append(word)
                if len(wn.synsets(word)) > 0:
                    synset = wn.synsets(word)[0]
                    syn = (str(synset).split("(")[-1][:-1].replace(".", "_"))
                    sentence_2_new.append(syn.strip("'"))
                else:
                    sentence_2_new.append("no_syn")
            else: 
                sentence_2_new.append("no_syn")
            
                    
        labels.append(sentence_pair[0])
        sent1_syn.append(sentence_1_new)
        sent2_syn.append(sentence_2_new)
        premise.append(premise_tok)
        hypothesis.append(hypothesis_tok)

    return labels, sent1, sent2, premise, hypothesis, sent1_syn, sent2_syn


def write_data_file(path, data_labeled):
    labels, sent1, sent2, premise, hypothesis, sent1_syn, sent2_syn = get_synonym_corpus(data_labeled)
    dict_synsets = {'gold_labels': labels, 'sentence1': sent1, 'sentence2': sent2, 'premise': premise, 'hypothesis': hypothesis,'sentence1_syn': sent1_syn, 'sentence2_syn': sent2_syn}
    df = pd.DataFrame.from_dict(dict_synsets)
    df.to_json(path_or_buf=path, orient="records", lines=True)

train = write_data_file('snli_train_original_synsets.json', train_data)
val = write_data_file('snli_val_original_synsets.json', val_data)
test = write_data_file('snli_test_original_synsets.json', test_data)
