import json

def read_prem(path):
    premises = []
    for line in open(path, mode='r', encoding='utf-8'):
        reader = json.loads(line)
        #line_lst = []
        for k in reader.keys():
            if k == 'sentence1':
                premises.append(reader[k])                

    return premises

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]