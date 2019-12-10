import torch
import torch.nn as nn
import torch.nn.functional as F

class BiLSTM(nn.Module):
    def __init__(self, w2v_file, embedding_dim, embedding_size, embedding_dim_pos, max_sen_len, max_doc_len, n_hidden, n_class, batch_size):
        super(BiLSTM, self).__init__()

        self.batch = batch_size
        self.embedding_size = embedding_size  # len(word_idx)
        self.embedding_dim = embedding_dim
        self.embedding_pos_dim = embedding_dim_pos
        self.hidden_dim =

        self.lstm = nn.LSTM(imput_size=self.embedding_dim+self.embedding_pos_dim*2, hidden_size=)