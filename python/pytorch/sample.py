import torch
import torch.nn as nn


def main() -> None:
    embedding_gender = nn.Embedding(num_embeddings=2, embedding_dim=8)
    embedding_job = nn.Embedding(num_embeddings=22, embedding_dim=8)

    # カテゴリカル特徴量をTensorで渡す
    gender_features = torch.tensor(["male", "female", "female", "male"])
    job_features = torch.tensor(["engineer", "doctor", "artist", "teacher"])

    # ラベルエンコーディング

    # Entity Embeddingによって埋め込みベクトルに変換
    gender_emb = embedding_gender(gender_idx)
    job_emb = embedding_job(job_idx)

    # Entity Embedding化したカテゴリ特徴量とその他の数値特徴量をconcatenateしてMLPへ〜
    numeric_features = torch.tensor([[0.5, 1.2], [0.3, 0.7], [0.9, 1.5], [0.4, 1.0]])
    x = torch.cat([gender_emb, job_emb, numeric_features], dim=1)
    print(x)  # 4サンプル分の特徴量ベクトル


if __name__ == "__main__":
    main()
