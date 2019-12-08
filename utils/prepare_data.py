# encoding:utf-8
import codecs
import random
import numpy as np
import pickle as pk
from sklearn.metrics import precision_score, recall_score, f1_score
import pdb, time

def print_time():
    print('----------{}----------\n'.format(time.strftime("%Y-%m-%d %X", time.localtime())))

def load_word2vector(embedding_dim, embedding_dim_pos, train_file_path, embedding_path):
    print('load embedding...\n')

    words = []
    with open(train_file_path, 'r') as f1:
        for line in f1.readlines():
            line = line.strip().split(',')
            emotion, clause = line[2], line[-1]
            words.extend([emotion] + clause.split())
        words = set(words)  # redupliction removing
        word_idx = dict()

if __name__ == '__main__':
    print_time()