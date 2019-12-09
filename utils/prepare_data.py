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
        word_idx = dict((c, k + 1) for k, c in enumerate(words))  # each word and its position
        word_idx_rev = dict((k + 1, c) for k, c in enumerate(words))

    w2v = {}
    with open(embedding_path, 'r') as f2:
        f2.readline()  # Q
        for line in f2.readlines():
            line = line.strip().split(' ')
            w, ebd = line[0], line[1:]
            w2v[w] = ebd

    embedding = [list(np.zeros(embedding_dim))]
    hit = 0
    for item in words:
        if item in w2v:
            vec = list(map(float, w2v[item]))
            hit += 1
        else:
            vec = list(np.random.rand(embedding_dim) / 5. - 0.1)  # take randomly from the uniform distribution[-0.1, 0.1]
        embedding.append(vec)
    print('w2v_file: {}\nall_words: {} hit_words: {}'.format(embedding_path, len(words), hit))

    embedding_pos = [list(np.zeros(embedding_dim_pos))]
    embedding_pos.extend([list(np.random.normal(loc=0.0, scale=0.1, size=embedding_dim_pos)) for i in range(200)])
    embedding, embedding_pos = np.array(embedding), np.array(embedding_pos)
    print('embedding.shape: {} embedding_pos.shape: {}'.format(embedding.shape, embedding_pos.shape))
    print('load embedding done!\n')
    return word_idx_rev, word_idx, embedding, embedding_pos



if __name__ == '__main__':
    print_time()