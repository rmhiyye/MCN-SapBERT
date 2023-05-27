import argparse

import src.config
from src.data_loader import data_loader
from src.trainer import n2c2Trainer
from src.utils import eval_map

import os
os.environ["CUDA_VISIBLE_DEVICES"]=src.config.cuda_visible_devices

def main(config, args):
    
    print('Loading data...')

    train_dataset, test_dataset, validation_dataset, train_ref_dataset, test_ref_dataset, train_cui_less_dict, train_span_split, test_span_split = data_loader()

    trainer = n2c2Trainer(args, train_dataset, test_dataset, validation_dataset, train_ref_dataset, test_ref_dataset)

    if args.do_train:
        print('CUI-less in train set:', len(train_cui_less_dict.keys()))
        print('Span split in train set:', train_span_split)
        print('Training...')
        trainer.train()

    if args.do_eval:
        print('Span split in test set:', test_span_split)
        print('Evaluating...')
        predictions = trainer.inference()

        MAP_k1 = eval_map(test_dataset, predictions)
        print('MAP', MAP_k1)
        MAP_k5 = eval_map(test_dataset, predictions, k=5)
        print('MAP@5', MAP_k5)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--do_train', action='store_true', help='Whether to run training.')
    parser.add_argument('--do_eval', action='store_true', help='Whether to run eval on the test set.')
    parser.add_argument('--save_tb', action='store_true', help='Whether to save tensorboard.')

    args = parser.parse_args()

    config = src.config

    main(config, args)