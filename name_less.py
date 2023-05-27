# output the cui which has name-less in the file cui2name.txt
import argparse

def name_less_detector(file_path):
    with open(f"{file_path}", "r") as fl:
        lines = fl.readlines()
    for line in lines:
        line = line.strip()
        cui = line.split("||")[0]
        cui_name = line.split("||")[1]
        if cui_name == 'NAME-less':
            print(cui)
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help='train or test')
    args = parser.parse_args()
    if args.input == 'train':
        name_less_detector("dataset/train/cui2name.txt")
    elif args.input == 'test':
        name_less_detector("dataset/gold/cui2name.txt")