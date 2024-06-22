import numpy as np
import pytest
import torch
from model import BPRLossZerosumRegularized, MatrixFactorization
from scipy import sparse
from torch.utils.data import DataLoader, TensorDataset


@pytest.fixture
def bpr_reg_loss_func() -> BPRLossZerosumRegularized:
    return BPRLossZerosumRegularized(is_regularized=True)


@pytest.fixture
def mf_model() -> MatrixFactorization:
    return MatrixFactorization(num_users=100, num_items=50, embedding_dim=16)


@pytest.fixture
def user_item_reactions() -> sparse.csr_matrix:
    user_ids = [1, 2, 3]
    item_ids = [1, 2, 3]

    reactions = np.array([1, 1, 1])
    user_indices = np.array([0, 1, 2])
    item_indices = np.array([1, 0, 2])

    return sparse.csr_matrix((reactions, (user_indices, item_indices)), shape=(len(user_ids), len(item_ids)))


def test_bpr_loss(bpr_reg_loss_func: BPRLossZerosumRegularized) -> None:

    # create some test data
    positive_scores = torch.tensor([3.0, 2.0, 4.0])
    negative_scores = torch.tensor([1.0, 1.5, 1.0])

    # calculate expected loss
    expected_loss = (
        # BPR Loss Term
        -torch.log(torch.sigmoid(positive_scores[0] - negative_scores[0]))
        - torch.log(torch.sigmoid(positive_scores[1] - negative_scores[1]))
        - torch.log(torch.sigmoid(positive_scores[2] - negative_scores[2]))
        # Zerosum Regularization Term
        + torch.log(1 - torch.tanh(positive_scores[0] + negative_scores[0]))
        + torch.log(1 - torch.tanh(positive_scores[1] + negative_scores[1]))
        + torch.log(1 - torch.tanh(positive_scores[2] + negative_scores[2]))
    )

    actual_loss = bpr_reg_loss_func.forward(positive_scores, negative_scores)

    assert torch.isclose(actual_loss, expected_loss)


def test_train_bpr(
    mf_model: MatrixFactorization,
    user_item_reactions: sparse.csr_matrix,
    bpr_reg_loss_func: BPRLossZerosumRegularized,
) -> None:
    optimizer = torch.optim.Adam(mf_model.parameters(), lr=0.01)
    num_epochs = 2
    loss_histroy = mf_model.fit(
        user_item_reactions,
        bpr_reg_loss_func,
        optimizer,
        batch_size=32,
        num_epochs=num_epochs,
        device=torch.device("cpu"),
    )

    assert len(loss_histroy) == num_epochs

    for epoch_loss in loss_histroy:
        assert epoch_loss >= 0
