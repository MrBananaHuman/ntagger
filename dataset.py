from __future__ import absolute_import, division, print_function

import os
import pdb

import torch
from torch.utils.data.dataset import Dataset
from torch.utils.data import TensorDataset

class CoNLLGloveDataset(Dataset):
    def __init__(self, path):
        all_token_ids = []
        all_pos_ids = []
        all_label_ids = []
        with open(path,'r',encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                items = line.split('\t')
                token_ids = [int(d) for d in items[1].split()]
                pos_ids   = [int(d) for d in items[2].split()]
                label_ids = [int(d) for d in items[0].split()]
                all_token_ids.append(token_ids)
                all_pos_ids.append(pos_ids)
                all_label_ids.append(label_ids)
        all_token_ids = torch.tensor(all_token_ids, dtype=torch.long)
        all_pos_ids = torch.tensor(all_pos_ids, dtype=torch.long)
        all_label_ids = torch.tensor(all_label_ids, dtype=torch.long)

        self.x = TensorDataset(all_token_ids, all_pos_ids)
        self.y = all_label_ids
 
    def __len__(self):
        return len(self.y)

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]

class CoNLLBertDataset(Dataset):
    def __init__(self, path):
        # load features from file
        features = torch.load(path)
        # convert to tensors and build dataset
        all_input_ids = torch.tensor([f.input_ids for f in features], dtype=torch.long)
        all_input_mask = torch.tensor([f.input_mask for f in features], dtype=torch.long)
        all_segment_ids = torch.tensor([f.segment_ids for f in features], dtype=torch.long)
        all_pos_ids = torch.tensor([f.pos_ids for f in features], dtype=torch.long)
        all_label_ids = torch.tensor([f.label_ids for f in features], dtype=torch.long)

        self.x = TensorDataset(all_input_ids, all_input_mask, all_segment_ids, all_pos_ids)
        self.y = all_label_ids
 
    def __len__(self):
        return len(self.y)

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]
