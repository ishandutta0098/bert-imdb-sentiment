import torch
import config

class BERTDataset:
    def __init__(self, review, target):
        self.review = review    # Movie review text
        self.target = target    # Target (0/1)
        self.tokenizer = config.TOKENIZER
        self.max_len = config.MAX_LEN

    def __len__(self):
        return len(self.review)

    def __getitem__(self, item):
        review = str(self.review[item])
        review = " ".join(review.split())

        inputs = self.tokenizer.encode_plus(
            review, 
            None,    # Because encode_plus can encode 2 strings at a time
            add_special_tokens = True,
            max_len = self.max_len
        )

        ids = inputs["input_ids"]
        mask = inputs["attention_mask"]
        token_type_ids = inputs["token_type_ids"]

        padding_length = self.max_len - len(ids)
        ids = ids + ([0] * padding_length)
        mask = mask + ([0] * padding_length)
        token_type_ids = token_type_ids + ([0] * padding_length)

        return {
            'ids': torch.tensor(ids, dtype = torch.long),
            'mask': torch.tensor(mask, dtype = torch.long),
            'token_type_ids': torch.tensor(token_type_ids, dtype = torch.long),
            'target': torch.tensor(self.target[item], dtype = torch.float)
        }
