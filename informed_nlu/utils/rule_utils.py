import json

def flatten(l):
    for sublist in l:
         if isinstance(sublist, list):
             for item in sublist:
                yield item
         else:
             yield sublist
    return
        
def read_deps(path):
    data = []
    for line in open(path, mode='r', encoding='utf-8'):
        reader = json.loads(line)
        line_lst = []
        for k in reader.keys():
            if k == 'sentence1' or k == 'premise_tok' or k == 'sent1_pos' or k == 'sent1_deps' or k == 'sent1_features' or k == 'sent1_disambig':
                line_lst.append(reader[k])                
        data.append(line_lst)

    return data
