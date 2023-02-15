from typing import List, Tuple

import torch
import torch.nn as nn
from torch import Tensor
from torch.utils.data import DataLoader, Dataset
from zmq import device


class BayesianPersonalizedRanking(nn.Module):
    def __init__(
        self,
        num_users: int,
        num_items: int,
        embedding_dim: int,
    ) -> None:
        """
        user_num: number of users;
        item_num: number of items;
        factor_num: number of predictive factors.
        """
        super(BayesianPersonalizedRanking, self).__init__()
        self.embed_user = nn.Embedding(num_users, embedding_dim)
        self.embed_item = nn.Embedding(num_items, embedding_dim)

        nn.init.normal_(self.embed_user.weight, std=0.01)
        nn.init.normal_(self.embed_item.weight, std=0.01)

    def forward(
        self,
        user_indices: Tensor,
        item_indices: Tensor,
    ) -> Tensor:
        user_embeddings: Tensor = self.embed_user.forward(user_indices)
        item_embeddings: Tensor = self.embed_item.forward(item_indices)
        preference_scores = torch.sum(user_embeddings * item_embeddings, dim=1)
        return preference_scores

    def bpr_loss(self, positive_scores: Tensor, negative_scores: Tensor) -> Tensor:
        score_diffs = torch.sigmoid(positive_scores - negative_scores)
        loss = -torch.sum(torch.log(score_diffs))
        return loss
