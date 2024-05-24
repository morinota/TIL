## memo

python 3.10のAWS提供のコンテナを使って、カスタム推論スクリプトでSagemaker推論エンドポイントをデプロイしたいです。
sagemaker.model.Modelクラスを使って実装してください。
model.tar.gzの構造は以下です。
```
model_artifact
├── code
│   ├── inference.py
│   ├── loader.py
│   ├── models.py
│   ├── recommender.py
│   └── type_aliases.py
├── model.pth
├── movie_vectors
│   └── 000.gz
├── requirements.txt
└── user_vectors
    └── 000.gz
```

inference.pyに/pingとinvocationsを定義する必要があるのですか?? model_fn()、input_fn()、predict_fn()、output_fn()の4つの関数を定義するだけで良いのかと思っていました。
