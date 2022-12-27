from typing import Tuple

import torch
from pairwise_distances import pairwise_distances
from torch import Tensor


def batch_all_triplet_loss(
    labels: Tensor,
    embeddings: Tensor,
    margin: float,
    squared: bool = False,
) -> Tuple[Tensor, Tensor]:
    """Build the triplet loss over a batch of embeddings.
    We generate all the valid triplets and average the loss over the positive ones.

    Parameters
    ----------
    labels : Tensor
        labels of the batch, of size (batch_size,)
    embeddings : Tensor
        tensor of shape (batch_size, embed_dim)
    margin : float
        margin for triplet loss
    squared : bool, optional
        If true, output is the pairwise squared euclidean distance matrix.
        If false, output is the pairwise euclidean distance matrix.,
        by default False

    Returns
    -------
    Tuple[Tensor, Tensor]
        triplet_loss: scalar tensor containing the triplet loss
    """
    # Get the pairwise distance matrix
    pairwise_distance_matrix = pairwise_distances(embeddings, squared=squared)
    anchor_positive_dist = pairwise_distance_matrix.unsqueeze(dim=2)  # 指定されたidxにサイズ1の次元をinsertする
    # -> (batch_size, batch_size, 1)
    anchor_negative_dist = pairwise_distance_matrix.unsqueeze(dim=1)
    # -> (batch_size, 1, batch_size)

    # Compute a 3D tensor of size (batch_size, batch_size, batch_size)
    # triplet_loss[i, j, k] will contain the triplet loss of anchor=i, positive=j, negative=k
    # Uses broadcasting where the 1st argument has shape (batch_size, batch_size, 1)
    # and the 2nd (batch_size, 1, batch_size)
    triplet_loss = anchor_positive_dist - anchor_negative_dist + margin
    # Put to zero the invalid triplets
    # (where label(a) != label(p) or label(n) == label(a) or a == p)


def _get_triplet_mask(labels: Tensor) -> Tensor:
    """Return a 3D mask where mask[a, p, n]
        is True iff the triplet (a, p, n) is valid.

    A triplet (i, j, k) is valid if:
        - i, j, k are distinct
        - labels[i] == labels[j] and labels[i] != labels[k]

    Parameters
    ----------
    labels : Tensor
        int32 `Tensor` with shape [batch_size]

    return:Tensor
    """
    pass


def test_batch_all_strategy() -> None:
    embeddings = Tensor([[1, 2], [3, 4], [5, 6]])  # ベクトル数:3, 次元数:2
    labels = Tensor([0, 1, 1])
    print(embeddings.shape)
    distances_actual = pairwise_distances(embeddings, squared=True)
    print(distances_actual)
    distance_expected = Tensor([[0.0, 8.0, 32.0], [8.0, 0.0, 8.0], [32.0, 8.0, 0.0]])

    assert torch.equal(distances_actual, distance_expected)


if __name__ == "__main__":
    embeddings = Tensor([[1, 2], [3, 4], [5, 6]])  # ベクトル数:3, 次元数:2
    labels = Tensor([0, 1, 1])
    margin = 0.5
    batch_all_triplet_loss(
        labels=labels,
        embeddings=embeddings,
        margin=margin,
    )
