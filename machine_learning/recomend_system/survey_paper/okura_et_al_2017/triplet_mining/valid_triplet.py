import torch
from torch import Tensor


class TripletValidetor:
    """tripletが有効か無効かを判定する為のクラス"""

    def __init__(self) -> None:
        pass

    def get_mask(self, labels: Tensor) -> Tensor:
        """有効な(valid) triplet(i,j,k)->True, 無効な(invalid) triplet(i,j,k)->Falseとなるような
        Tensor(batch_size*batch_size*batch_size)を作成して返す.
        Return a 3D mask where mask[i, j, k]
            is True iff the triplet (i, j, k) is valid.

        A triplet (i, j, k) is valid if:有効なtripletである条件は以下の2つ:
            - i, j, k are distinct
            - labels[i] == labels[j] and labels[i] != labels[k]

        Parameters
        ----------
        labels : Tensor
            int32 `Tensor` with shape [batch_size]

        return:Tensor
            shape = (batch_size, batch_size, batch_size)
            mask[i, j, k] は $(i,j,k)$ が有効なトリプレットであれば真
        """
        # 条件1:Check that i, j and k are distinct  独立したindicesか否か
        indices_equal = torch.eye(n=labels.size(0)).bool()  # labelsのサイズに応じた単位行列を生成し、bool型にキャスト
        indices_not_equal = ~indices_equal  # boolを反転する
        i_not_equal_j = indices_not_equal.unsqueeze(dim=2)
        i_not_equal_k = indices_not_equal.unsqueeze(dim=1)
        j_not_equal_k = indices_not_equal.unsqueeze(dim=0)
        distinct_indices = i_not_equal_j & i_not_equal_k & j_not_equal_k

        # 条件2: Check if labels[i] == labels[j] and labels[i] != labels[k]
        label_equal = labels.unsqueeze(0) == labels.unsqueeze(1)
        i_equal_j = label_equal.unsqueeze(2)
        i_equal_k = label_equal.unsqueeze(1)
        valid_labels = i_equal_j & (~i_equal_k)

        return distinct_indices & valid_labels
