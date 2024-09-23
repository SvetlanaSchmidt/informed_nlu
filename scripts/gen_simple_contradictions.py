import json
import tqdm
import random
import pandas as pd
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from create_datalists import read_data
from utils.rule_utils import flatten, read_deps

"""Developed by Svetlana Schmidt"""

def create_num_cont(data_labeled):
    """The generation of the numeric based contradictions
    Params:
     - the data from SNLI corpus: for each sentence 
    (PREMISE: 'A person on a horse jumps over a broken down airplane.', 
    DEP: ['det', 'nsubj', 'case', 'det', 'nmod', 'root', 'case', 'det', 'amod', 'amod', 'obl', 'punct'],
    MORPH FEAT: ['Definite=Ind|PronType=Art', 'Number=Sing', None, 'Definite=Ind|PronType=Art', 
    'Number=Sing', 'Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin', None, 
    'Definite=Ind|PronType=Art', 'Tense=Past|VerbForm=Part', 'Degree=Pos', 'Number=Sing', None])
    return:
     - list [label, premise, generated hypothesis]
    """
    f = open("numerals.txt", 'r')
    num_lines = f.readlines()
    numerals = [num.split('\n')[0] for num in num_lines]
    premises = []
    hypotheses = []
    labels = []
    for sentence_pair in tqdm.tqdm(data_labeled):
        premise = sentence_pair[0]
        premise = word_tokenize(premise)
        deps = sentence_pair[3]
        feats = sentence_pair[4]
        premise_new = []
        hypothesis = []
        contradict=False
        for n, (token, dep, feat) in enumerate(zip(premise, deps, feats)):
            if 'nummod' in deps:
                contradict=True                 
                if dep == 'nummod' and token.lower() != 'one':
                    if token.lower() in numerals:
                        numerals.remove(token.lower())
                        if n == 0:
                            numeral = random.choice(numerals)
                            numeral = numeral[0].upper() + numeral[1:]
                            premise_new.append(token)
                            hypothesis.append(numeral)
                        else:
                            numeral = random.choice(numerals)
                            premise_new.append(" " + token)
                            hypothesis.append(" " + numeral)
                else:
                    if n == 0 or dep == 'punct':
                        premise_new.append(token)
                        hypothesis.append(token)
                    else:
                        premise_new.append(" " + token)
                        hypothesis.append(" " + token)

        if len(premise_new) > 0 and len(hypothesis) > 0:
            premises.append("".join(premise_new))
            hypotheses.append("".join(hypothesis))
        
    
    for i in range(len(premises)):
        labels.append('contradiction')

    return labels, premises, hypotheses

def create_neg_cont(data_labeled):
    """The generation of the negation based contradictions
    Params:
     - the data from SNLI corpus: for each sentence 
    (PREMISE: 'A person on a horse jumps over a broken down airplane.', 
    DEP: ['det', 'nsubj', 'case', 'det', 'nmod', 'root', 'case', 'det', 'amod', 'amod', 'obl', 'punct'],
    MORPH FEAT: ['Definite=Ind|PronType=Art', 'Number=Sing', None, 'Definite=Ind|PronType=Art', 
    'Number=Sing', 'Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin', None, 
    'Definite=Ind|PronType=Art', 'Tense=Past|VerbForm=Part', 'Degree=Pos', 'Number=Sing', None])
    return:
     - list [label, premise, generated hypothesis]
    """
    premises = []
    hypotheses = []
    labels = []
    for sentence_pair in tqdm.tqdm(data_labeled):
        premise = sentence_pair[0]
        premise = word_tokenize(premise)
        deps = sentence_pair[3]         
        feats = sentence_pair[4]
        premise_new = []
        hypothesis = []
        contradict = False
        for n, (token, dep, feat) in enumerate(zip(premise, deps, feats)): 
            if 'root' in deps:                           
                if dep == 'root' and feat != None:
                    if "Number=Sing" in feat and "Tense=Pres" in feat:
                        neg = "does not " + token
                    elif "Number=Plur" in feat and "Tense=Pres" in feat:
                        neg = "do not " + token
                    elif "Tense=Pres|VerbForm=Part" in feat:
                        neg = "not " + token
                    if n == 0:
                        premise_new.append(token)
                        hypothesis.append(neg[0] + neg[1:])
                        contradict=True 
                    else:
                        premise_new.append(" " + token)
                        hypothesis.append(" " + neg)
                        contradict=True 
                else:
                    if n != 0 and dep != "punct":
                        premise_new.append(( " " + token))
                        hypothesis.append(( " " + token))
                        contradict=True
                    else:
                        premise_new.append(token)
                        hypothesis.append(token)
                        contradict=True 
        
        if len(premise_new) > 0 and len(hypothesis) > 0:
            premises.append("".join(premise_new))
            hypotheses.append("".join(hypothesis))                     
    
    for i in range(len(premises)):
        labels.append('contradiction')
        
    return labels, premises, hypotheses
                                    

def create_adj_ant(data_labeled):
    """The generation of the antonymy based contradictions
    Params:
     - the data from SNLI corpus: for each sentence 
    (PREMISE: 'A person on a horse jumps over a broken down airplane.', 
    POS: []'DET', 'NOUN', 'ADP', 'DET', 'NOUN', 'VERB', 'ADP', 'DET', 'VERB', 'ADP', 'NOUN', 'PUNCT']
    DEP: ['det', 'nsubj', 'case', 'det', 'nmod', 'root', 'case', 'det', 'amod', 'amod', 'obl', 'punct'],
    MORPH FEAT: ['Definite=Ind|PronType=Art', 'Number=Sing', None, 'Definite=Ind|PronType=Art', 
    'Number=Sing', 'Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin', None, 
    'Definite=Ind|PronType=Art', 'Tense=Past|VerbForm=Part', 'Degree=Pos', 'Number=Sing', None]
    SYNSETS: ['A', 'wn:00007846n', 'on', 'a', 'wn:02374451n', 'wn:01963942v', 'over', 'a', 'wn:00202569v', 
    'down', 'wn:02691156n', '.'])
    return:
     - list [label, premise, generated hypothesis]
     - antonyms of aligned words in the premise and hypothesis
    """
    premises = []
    hypotheses = []
    labels = []
    antonym_pairs = []
    for sentence_pair in tqdm.tqdm(data_labeled):
        premise = sentence_pair[0]
        premise = word_tokenize(premise)
        pos = sentence_pair[2]
        deps = sentence_pair[3]
        feats = sentence_pair[4]
        sent_syn=[]
        for syn in sentence_pair[5]:
            if 'wn:' in syn:
                sent_syn.append(syn)
            else:
                sent_syn.append(None)

        premise_new = []
        hypothesis = []
        antonym_sent = []
        contradict = False
        antonym=False  
        if "ADJ" in pos: 
            for n, (token, dep, p, feat, s) in enumerate(zip(premise, deps, pos, feats, sent_syn)):          
                if p == "ADJ" and dep != "compound": 
                    ant_adj = []
                    antonyms = [] 
                    if s != None: 
                        syn = wn.synset_from_pos_and_offset(s[len(s)-1], int(s[3:len(s)-1]))     
                        for l in syn.lemmas():
                            if l.antonyms():
                                ant_adj.append(l.antonyms())# get antonym for the subject

                    ant_adj = list(flatten(ant_adj))
                    ant_synsets = [ant.synset() for ant in ant_adj]
                    
                    for ant_s in ant_synsets:
                        antonyms.append(ant_s.lemma_names())
                    antonyms = [ant for subl in antonyms for ant in subl if "_" not in ant]
                        
                    if len(antonyms) > 0:
                        if n != 0: 
                            antonym=True
                            premise_new.append((" " + token))
                            hypothesis.append((" " + antonyms[0]))
                            antonym_sent.append((token, antonyms[0]))
                        else:
                            premise_new.append((token))
                            hypothesis.append((antonyms[0]))
                            antonym_sent.append((token, antonyms[0]))
                            
                    elif len(antonyms) == 0:
                        if n != 0: 
                            antonym = True
                            premise_new.append((" " + token))
                            hypothesis.append((" " + token))
                            antonym_sent.append(None)
                        else:
                            premise_new.append((token))
                            hypothesis.append((token))
                            antonym_sent.append(None)            
                elif p != "ADJ":
                    if n != 0 or dep != "punct":
                        premise_new.append((" " + token))
                        hypothesis.append((" " + token))
                        antonym_sent.append(None)
                    else:
                        premise_new.append((token))
                        hypothesis.append(token)
                        antonym_sent.append(None)
        
        if len(premise_new) > 0 and len(hypothesis) > 0 and antonym==True and premise_new != hypothesis:
            premises.append("".join(premise_new))
            hypotheses.append("".join(hypothesis))
            antonym_pairs.append(antonym_sent)
    
    for i in range(len(premises)):
        labels.append('contradiction')
                
    return labels, premises, hypotheses, antonym_pairs

def create_proto(data):
    """
    Generates the contradictory data for the premises from SNLI
    return:
     - the lists of simple generated contradiction pairs 
     for antonymy, negation, numeric mismatch concatenated together
    """
    neg_labels, n_prem, n_hypot = create_neg_cont(data[:200])
    num_labels, num_prem, num_hypot = create_num_cont(data[:200])
    adj_labels, adj_prem, adj_hypot, ant_list = create_adj_ant(data[:200])
    
    #adjectival antonymy
    labels = neg_labels + num_labels + adj_labels
    premise = n_prem + num_prem + adj_prem
    hypothese = n_hypot + num_hypot + adj_hypot

    
    return labels, premise, hypothese
        

def write_data_file(path, data_contr, data_labeled):
    """Save the contradictory data to a JSON file
    optional: add the entailments and neutral sentence pairs
    """
    labels_gold = []
    premise_gold = []
    hypothese_gold = []
    for s in data_labeled:
        if s[0] != 'contradiction':
            labels_gold.append(s[0])
            premise_gold.append(s[1])
            hypothese_gold.append(s[2])
            
    proto_labels, proto_premise, proto_hypothese = create_proto(data_contr)  
    # labels = proto_labels+labels_gold[:len(proto_labels)] # comment out to save not only contrad
    # premise = proto_premise+premise_gold[:len(proto_premise)] # add the same number of non contradictions 
    # hypothese = proto_hypothese+hypothese_gold[:len(proto_hypothese)] 
    #generate only contradictions
    labels = proto_labels 
    premise = proto_premise
    hypothese = proto_hypothese
 
    
    dict_contr = {'gold_labels': labels, 'sentence1': premise, 'sentence2': hypothese}
    df = pd.DataFrame.from_dict(dict_contr)
    df.to_json(path_or_buf=path, orient="records", lines=True)


if __name__ == "__main__":
    #add paths to snli data
    all_train = "/cluster/svetlana/data/snli_train_pos_dep.json"
    all_dep = "/cluster/svetlana/data/snli_dev_pos_dep.json"
    all_test = "/cluster/svetlana/data/snli_test_pos_dep.json"

    train_data = read_data(all_train)
    val_data = read_data(all_dep)
    test_data = read_data(all_test)
   
    train_file = "train_deps_syn.json"
    val_file = "val_deps_syn.json"
    test_file = "test_deps_syn.json"
    
    train_proto = read_deps(train_file)
    val_proto = read_deps(val_file)
    test_proto = read_deps(test_file)
    
    train = write_data_file('train_simple_prototypes.json', data_contr = train_proto, data_labeled = train_data)
    val = write_data_file('val_simple_prototypes.json', data_contr = val_proto, data_labeled = val_data)
    test = write_data_file('test_simple_prototypes.json', data_contr = test_proto, data_labeled = test_data)
