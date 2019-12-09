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
        f2.readline()  # Q read the first line: 43593 200
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

    embedding_pos = [list(np.zeros(embedding_dim_pos))]  # Q2
    embedding_pos.extend([list(np.random.normal(loc=0.0, scale=0.1, size=embedding_dim_pos)) for i in range(200)])
    embedding, embedding_pos = np.array(embedding), np.array(embedding_pos)
    print('embedding.shape: {} embedding_pos.shape: {}'.format(embedding.shape, embedding_pos.shape))
    print('load embedding done!\n')
    return word_idx_rev, word_idx, embedding, embedding_pos

def load_data(input_file, word_idx, max_doc_len = 75, max_sen_len = 45):
    print('load data_file: {}'.format(input_file))
    y_position, y_cause, y_pairs, x, sen_len, doc_len = [], [], [], [], [], []
    doc_id = []

    n_cut = 0
    with open(input_file, 'r') as f1:
        while True:
            line = f1.readline()
            if line == '': break
            line = line.strip().split()
            doc_id.append(line[0])  # 212 10
            d_len = int(line[1])
            pairs = eval('[' + f1.readline().strip() + ']')
            doc_len.append(d_len)
            y_pairs.append(pairs)
            pos, cause = zip(*pairs)
            y_po, y_ca, sen_len_tmp, x_tmp = np.zeros((max_doc_len, 2)), np.zeros((max_doc_len, 2)), np.zeros(max_doc_len,dtype=np.int32), np.zeros((max_doc_len, max_sen_len),dtype=np.int32)
            for i in range(d_len):
                y_po[i][int(i+1 in pos)] = 1
                y_ca[i][int(i+1 in cause)] = 1
                words = f1.readline().strip().split(',')[-1]
                sen_len_tmp[i] = min(len(words.split()), max_sen_len)
                for j, word in enumerate(words.split()):
                    if j >= max_sen_len:
                        n_cut += 1
                        break
                    x_tmp[i][j] = int(word_idx[word])

            y_position.append(y_po)
            y_cause.append(y_ca)
            x.append(x_tmp)
            sen_len.append(sen_len_tmp)

        y_position, y_cause, x, sen_len, doc_len = map(np.array, [y_position, y_cause, x, sen_len, doc_len])
        for var in ['y_position', 'y_cause', 'x', 'sen_len', 'doc_len']:
            print('{}.shape {}'.format(var, eval(var).shape))
        print('n_cut {}'.format(n_cut))
        print('load data done!\n')
        return doc_id, y_position, y_cause, y_pairs, x, sen_len, doc_len


if __name__ == '__main__':
    print_time()
    embedding_dim = '200'
    embedding_dim_pos = '50'
    train_file_path = '../data_combine/clause_keywords.csv'
    embedding_path = '../data/w2v_200.txt'

    # words = []
    # with open(train_file_path, 'r') as f1:
    #     for line in f1.readlines():
    #         line = line.strip().split(',')
    #         emotion, clause = line[2], line[-1]
    #         words.extend([emotion] + clause.split())
    #     words = set(words)  # redupliction removing
    #     word_idx = dict((c, k + 1) for k, c in enumerate(words))  # each word and its position
    #     word_idx_rev = dict((k + 1, c) for k, c in enumerate(words))