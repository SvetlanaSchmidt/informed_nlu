from sklearn.metrics import f1_score, accuracy_score, matthews_corrcoef

# todo maybe refactor to make it more generic

def get_metrics_binary(predictions, labels):
    acc = accuracy_score(labels, predictions)
    f1_contr = f1_score(labels, predictions, pos_label=1)
    f1_no_contr = f1_score(labels, predictions, pos_label=0)
    mcc = matthews_corrcoef(labels, predictions)
    return acc, f1_contr, f1_no_contr, None, mcc


def get_metrics_three(predictions, labels):
    acc = accuracy_score(labels, predictions)
    f1_neutr, f1_contr, f1_ent = f1_score(predictions, labels, average=None)
    mcc = matthews_corrcoef(labels, predictions)
    return acc, f1_contr, f1_neutr, f1_ent, mcc


def choose_metric_fn(num_labels_bool):
    return get_metrics_binary if num_labels_bool else get_metrics_three
