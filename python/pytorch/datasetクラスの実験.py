import numpy as np
import pandas as pd
import polars as pl
import torch
from sklearn.model_selection import KFold
from torch.utils.data import DataLoader, Dataset, Subset


# Pandas Dataset
class PandasCustomDataset(Dataset):
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, idx) -> tuple[torch.Tensor, torch.Tensor]:
        features = self.dataframe.iloc[idx, :-1]
        target = self.dataframe.iloc[idx, -1]
        return torch.tensor(features, dtype=torch.float32), torch.tensor(target, dtype=torch.float32)


# Polars Dataset
class PolarsCustomDataset(Dataset):
    def __init__(self, dataframe) -> None:
        self.dataframe = dataframe

    def __len__(self) -> int:
        return len(self.dataframe)

    def __getitem__(self, idx) -> tuple[torch.Tensor, torch.Tensor]:
        features = np.array(self.dataframe.row(idx)[:-1])
        target = np.array(self.dataframe.row(idx)[-1])
        return torch.tensor(features, dtype=torch.float32), torch.tensor(target, dtype=torch.float32)


# Numpy Dataset(テーブルデータなら可能だが...)
class NumpyCustomDataset(Dataset):
    def __init__(self, ndarray) -> None:
        self.ndarray = ndarray

    def __len__(self) -> int:
        return len(self.ndarray)

    def __getitem__(self, idx) -> tuple[torch.Tensor, torch.Tensor]:
        features = torch.Tensor(self.ndarray[idx, :-1])
        target = torch.Tensor([self.ndarray[idx, -1]])
        return torch.tensor(features, dtype=torch.float32), torch.tensor(target, dtype=torch.float32)


def main():
    # ダミーデータ
    rng = np.random.default_rng()
    data = {
        "feature1": rng.random(10000),
        "feature2": rng.random(10000),
        "target": rng.random(10000),
    }

    pldf = pl.DataFrame(data)
    pddf = pd.DataFrame(data)
    nparray = np.array([data["feature1"], data["feature2"], data["target"]]).T

    # データセットを初期化
    pldataset = PolarsCustomDataset(pldf)
    pddataset = PandasCustomDataset(pddf)
    npdataset = NumpyCustomDataset(nparray)

    # Cross-validationのためのK-Foldを設定
    dataset = pldataset
    # dataset = pddataset
    # dataset = npdataset
    kf = KFold(n_splits=3)
    for _fold, (train_index, valid_index) in enumerate(kf.split(range(len(dataset)))):
        train_dataset = Subset(dataset, train_index)
        valid_dataset = Subset(dataset, valid_index)

        batch_size = 4
        train_dataloader = DataLoader(train_dataset, batch_size, shuffle=True)
        valid_dataloader = DataLoader(valid_dataset, batch_size, shuffle=False)

        num_epochs = 10
        for i in range(num_epochs):
            for feats, target in train_dataloader:
                pass


if __name__ == "__main__":
    main()
