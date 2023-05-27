'''
    use umls_api to convert cui in train_norm.txt and test_norm.txt into cui_name
    write out the file with the following format:
    cui || cui_name
'''
import argparse
import os
import umls_api
from requests.exceptions import HTTPError
from tqdm import tqdm

def main(arg):

    ################################################
    print("\nConverting cui to concept name:\n")
    ################################################
    
    file_name = arg.input_name # train_norm.txt or test_norm.txt
    replace = arg.replace
    if file_name == 'train_norm':
        file_path = os.getcwd() + "/dataset/train"
    elif file_name == 'test_norm':
        file_path = os.getcwd() + "/dataset/gold"
    else:
        raise ValueError("file_name should be either text_norm or test_norm")
    
    # create a file to write out the cui2name_dict
    # check if the file exists
    if os.path.exists(f"{file_path}/cui2name.txt"):
        os.remove(f"{file_path}/cui2name.txt")

    with open(os.path.join(file_path, file_name) + '.txt', 'r') as fl:
        lines = fl.readlines()
    
    write_cui_names(lines, file_path, replace)

def write_cui_names(lines, file_path, replace):
    cui2name_dict = dict()
    # if arg.replace == True: remove the existing file
    # else: keep the existing file
    if replace == True and os.path.exists(f"{file_path}/cui2name.txt"):
        os.remove(f"{file_path}/cui2name.txt")
    else:
        with open(f"{file_path}/cui2name.txt", 'w') as fl:
            for line in tqdm(lines):
                line = line.strip()
                if line not in cui2name_dict.keys():
                    cui_name = get_cui_name(line)
                    cui2name_dict[line] = cui_name
                    fl.write(f"{line}||{cui_name}\n")
    print("Done.")

def get_cui_name(cui):
    key = '64a17e8c-3406-4dbc-bb2e-1afbe350bc37'
    try:
        api = umls_api.API(api_key=key)
        name = api.get_cui(cui)['result']['name']
    except HTTPError:
        print(f"HTTPError occurred for CUI: {cui}")
        name = 'NAME-less'
    return name

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_name", type=str, default="train_norm", help="the name of the input file")
    parser.add_argument("--replace", type=bool, default=False, help="whether to replace the existing file")
    arg = parser.parse_args()
    main(arg)