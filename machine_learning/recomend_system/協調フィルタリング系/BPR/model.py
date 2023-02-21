from typing import List, Tuple

import torch
import torch.nn as nn
from scipy import sparse
from torch import Tensor
from torch.utils.data import DataLoader, Dataset


class BeyesianPersonalizedRankingLoss(nn.Module):
    def __init__(
        self,
        lambda_theta: float,
    ) -> None:  # 小さい値をepsとして定義
        super(BeyesianPersonalizedRankingLoss, self).__init__()
        self.lambda_theta = lambda_theta

    def forward(
        self,
        positive_scores: Tensor,
        negative_scores: Tensor,
        model: nn.Module,
    ) -> Tensor:
        score_diffs = torch.sigmoid(positive_scores - negative_scores)

        loss = -torch.sum(torch.log(score_diffs))
        loss += self._calc_l2_reg_term(model)
        return loss

    def _calc_l2_reg_term(self, model: nn.Module) -> Tensor:
        """Add regularization term to the loss"""
        l2_reg_term = torch.tensor(0.0, requires_grad=True)
        for param in model.parameters():
            l2_reg_term += torch.norm(param) ** 2
        return l2_reg_term

    def _print_scores(self, pos_scores: Tensor, neg_scores: Tensor) -> None:
        for idx in range(pos_scores.shape[0]):
            print(pos_scores[idx], neg_scores[idx])


class MatrixFactorization(nn.Module):
    def __init__(
        self,
        num_users: int,
        num_items: int,
        embedding_dim: int,
        is_regularized: bool = True,
    ) -> None:
        """
        user_num: number of users;
        item_num: number of items;
        factor_num: number of predictive factors.
        """
        super(MatrixFactorization, self).__init__()
        self.embed_user = nn.Embedding(num_users, embedding_dim)
        self.embed_item = nn.Embedding(num_items, embedding_dim)
        self.is_regularized = is_regularized

    def forward(self, user_indices: Tensor, item_indices: Tensor) -> Tensor:
        user_embeddings: Tensor = self.embed_user.forward(user_indices)
        item_embeddings: Tensor = self.embed_item.forward(item_indices)
        preference_scores = torch.sum(user_embeddings * item_embeddings, dim=1)
        return preference_scores

    def fit(
        self,
        user_item_reactions: sparse.csr_matrix,
        loss_func: BeyesianPersonalizedRankingLoss,
        optimizer: torch.optim.Optimizer,
        batch_size: int,
        num_epochs: int,
        device: torch.device,
    ) -> List[float]:
        """BPRの学習を実行する."""
        self.to(device)
        loss_history = []
        train_data = self._sampling_dataset(user_item_reactions)
        train_dataloader = DataLoader(train_data, batch_size, shuffle=True)
        for epoch_idx in range(num_epochs):
            self.train()
            running_loss = 0.0
            for batch in train_dataloader:
                user_indices, pos_item_indices, neg_item_indices = batch
                user_indices: Tensor = user_indices.to(device)
                pos_item_indices: Tensor = pos_item_indices.to(device)
                neg_item_indices: Tensor = neg_item_indices.to(device)

                optimizer.zero_grad()
                pos_scores = self.forward(user_indices, pos_item_indices)
                neg_scores = self.forward(user_indices, neg_item_indices)

                print(pos_scores)

                loss = loss_func.forward(pos_scores, neg_scores, model=self)
                print(loss)
                running_loss += loss.item()
                loss.backward()
                optimizer.step()

            print(f"Epoch {epoch_idx + 1}, loss={running_loss:.4f}")
            loss_history.append(running_loss)
        return loss_history

    def _sampling_dataset(self, user_item_reactions: sparse.csr_matrix) -> Dataset:
        """implicitデータである user_item_reactionsから、
        (u, i, j) \in D_sのTripletをサンプリングしてDatasetとして返す.
        """
        pass
