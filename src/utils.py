####################
# id_combination, lowercaser_mentions
####################
from sklearn.metrics import f1_score

def id_combination(norm_dict):
    '''
    input:
        {"0034":
            {"N000":
                {"cui": .. ,
                 "mention", ..}
            }
        }
    output:
        {"0034_N000":
            {"cui": .. ,
             "mention", ..}
        }
    '''
    combin_dict = dict()
    for file_id in norm_dict.keys():
        for norm_id in norm_dict[file_id].keys():
            combin_id = file_id + "_" +norm_id
            combin_dict[combin_id] = norm_dict[file_id][norm_id]
    return combin_dict

def lowercaser_mentions(train_dict):
    for key in train_dict.keys():
        train_dict[key]["mention"] = train_dict[key]["mention"].lower()
    return train_dict

def eval_accuracy(actual, predicted):
    acc = 0
    for i, key in enumerate(actual.keys()):
        if isinstance(actual[key], dict):
            true_cui = actual[key]['cui']
        else:
            true_cui = actual[key]
        pred_cui = predicted[i]['first candidate'][0]
        if true_cui == pred_cui:
            acc += 1
    return acc / len(actual.keys())

# calculate mean average precision (k=1, 5)
def eval_map(actual, predicted, k=1):
    aps = []
    for i, key in enumerate(actual.keys()):
        if isinstance(actual[key], dict):
            true_cui = actual[key]['cui']
        else:
            true_cui = actual[key]
        pred_cui = predicted[i]['first candidate'] if k == 1 else predicted[i]['top 5 candidates']
        
        num_relevant_items = 0
        sum_precisions = 0
        for i, pred in enumerate(pred_cui, start=1):
            if pred == true_cui:
                num_relevant_items += 1
                precision_at_i = num_relevant_items / i
                sum_precisions += precision_at_i

        ap = sum_precisions / num_relevant_items if num_relevant_items > 0 else 0
        aps.append(ap)
    
    return sum(aps) / len(aps)