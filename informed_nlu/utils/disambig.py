import json
import requests
import tqdm
import time
import pandas as pd

def disambig(data, path):
    sentences = []
    premise_tok = []
    pos = []
    deps = []
    feats = []
    sent_dis = []
    for sample in tqdm.tqdm(data):       
        sentences.append(sample['sentence1'])
        premise_tok.append(sample['premise_tok'])
        pos.append(sample['sent1_pos'])
        deps.append(sample['sent1_deps'])
        feats.append(sample['sent1_features'])
        words=sample['premise_tok']
        try:
            r_en = eval(requests.get(f"http://api.syntagnet.org/disambiguate?lang=EN&text={sample['sentence1']}", timeout=5).content)
            time.sleep(0.5)
            tokens_idx = []
            for token_en in r_en["tokens"]:
                tokens_idx.append(((token_en["position"]["charOffsetBegin"], token_en["position"]["charOffsetEnd"]), token_en["senseID"]))
                sorted_tokens = sorted(tokens_idx, key=lambda x: x[0])
            
            word_index = 0
            for i, word in enumerate(words):
                word_start = word_index
                word_end = word_index + len(word)
                for (ids1, ids2), sense_id in sorted_tokens:
                    if word_start == ids1 and word_end == ids2:
                        words[i]=sense_id
                        break
                    
                word_index += len(word) + 1            
            
        except Exception as e:
            print(e)
    
        sent_dis.append(words)
          
    dict_contr = {'sentence1': sentences, 'premise_tok': premise_tok, 'sent1_pos': pos, 'sent1_deps': deps, 'sent1_features': feats, "sent1_disambig": sent_dis}
    df = pd.DataFrame.from_dict(dict_contr)
    df.to_json(path_or_buf=path, orient="records", lines=True)


if __name__ == "__main__":
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
    
    up_train = disambig(train_samples, path = "train_deps_syn.json")
    up_dev = disambig(val_samples, path = "val_deps_syn.json")
    up_test = disambig(test_samples, path = "test_deps_syn.json")
