import pickle
import logging
from typing import Optional, Dict

import pandas as pd
import json
from torch.utils.data import Dataset
"""Developed by Maren Pielka"""
logger = logging.getLogger(__name__)

class PreTrainDataset(Dataset):

    def __init__(self, path: str):
        self.data = json.load(open(path, "r"))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        sample = self.data[index]

        return sample
    
    def to_dict(self):
        return self.__dict__
    
    
class ClassificationDataset(PreTrainDataset):

    def __init__(self, path: str, label_mapping: Dict[str, int]):

        super().__init__(path)
        # drop samples with invalid labels
        old_len = len(self.data)
        self.data = [sample for sample in self.data if sample["gold_label"] in label_mapping.keys()]
        if old_len != len(self.data):
            logger.warning(f"Dropped {old_len - len(self.data)} examples with invalid labels")

        # Process labels
        for d in self.data:
            d.update({"label": label_mapping[d["gold_label"]]})

    def get_label_count(self):
        ones = sum(self.labels)
        zeros = abs(len(self.labels) - ones)
        return [zeros, ones]

    def save(self, path):
        dataset_dict = self.to_dict()
        with open(path, "w") as file:
            pickle.dump(dataset_dict, path)

