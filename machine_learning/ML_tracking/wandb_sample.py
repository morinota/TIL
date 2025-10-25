import wandb

print("start wandb")
print(f"{wandb.__version__=}")

wandb.init(
    project="test-project",  # The name of the project(実験の人まとまり)
    # 1回の実行(run)名 (同名のrunが作れてしまうので注意! 実際にはrun_idでユニークに識別されてるらしい。)
    # なので基本的には、timestampなどでユニークにするのが良さそうかも。
    name="test-run-1",
    config={  # hyperparameterなどを記録
        "my_dummy_param": 42,
        "my_other_param": "foo",
        "my_list_param": [1, 2, 3],
    },
)
# wandb.init()の返り値はRunオブジェクト。wandb.runでもアクセス可能。

if wandb.run:
    print(f"{wandb.run=}, {wandb.run.id=}")

# wandb.configはinit()に渡したconfigを保持するdict-likeなオブジェクト
config = wandb.config
print(f"{config.my_dummy_param=}")

# ログを記録 (wandb.log()に辞書を渡す)

for epoch_idx in range(5):
    # 例えば、epochごとにlossとaccuracyを計算したとする
    dummy_loss = 0.1 * (5 - epoch_idx)  # ダミーのloss
    dummy_accuracy = 0.2 * epoch_idx  # ダミーのaccuracy

    # 学習の経過をlogに記録
    wandb.log(
        {
            "epoch": epoch_idx,
            "train_loss": dummy_loss,
            "train_accuracy": dummy_accuracy,
            "valid_loss": dummy_loss + 0.05,  # ダミーのvalid loss
            "valid_accuracy": dummy_accuracy + 0.03,  # ダミーのvalid accuracy
        }
    )

# テスト結果も同様にログ
test_loss = 0.15  # ダミーのtest loss
test_accuracy = 0.85  # ダミーのtest accuracy
wandb.log(
    {
        "test_loss": test_loss,
        "test_accuracy": test_accuracy,
    }
)

# ベースライン指標も一緒に記録する例
# 推薦タスクで、DNN推薦とベースライン（ランダム推薦、CB推薦）を比較するケース

# 最終epoch後にベースラインも含めて評価指標を記録
# 例：precision@100の比較
baseline_random_precision = 0.05  # ランダム推薦のprecision@100
baseline_cb_precision = 0.35  # CB推薦のprecision@100
dnn_precision = 0.65  # DNN推薦のprecision@100

# 1回のrunで全てのモデルの指標を記録
# /で区切るとwandbのUIで階層的に表示されるので便利...!:thinking:
wandb.log(
    {
        "precision@100/random": baseline_random_precision,
        "precision@100/cb": baseline_cb_precision,
        "precision@100/dnn": dnn_precision,
    }
)

# 同様に他の指標も記録可能
wandb.log(
    {
        "recall@100/random": 0.03,
        "recall@100/cb": 0.28,
        "recall@100/dnn": 0.52,
        "ndcg@100/random": 0.04,
        "ndcg@100/cb": 0.31,
        "ndcg@100/dnn": 0.61,
    }
)

# summaryとしても記録しておくと、run一覧で簡単に比較できる
if wandb.run:
    wandb.run.summary["final_precision@100/random"] = baseline_random_precision
    wandb.run.summary["final_precision@100/cb"] = baseline_cb_precision
    wandb.run.summary["final_precision@100/dnn"] = dnn_precision

# 定性的な結果もログ可能 (例えば、画像やテキストなど)
# ここではサンプルユーザへの推薦コンテンツリストをログ
data = [
    [12345, "cont001", "推しアイテムA", 1],
    [12345, "cont002", "推しアイテムB", 2],
    [12345, "cont003", "推しアイテムC", 3],
    [12345, "cont004", "推しアイテムD", 4],
    [12345, "cont005", "推しアイテムE", 5],
    [12345, "cont006", "推しアイテムF", 6],
    [12345, "cont007", "推しアイテムG", 7],
    [12345, "cont008", "推しアイテムH", 8],
    [12345, "cont009", "推しアイテムI", 9],
    [12345, "cont010", "推しアイテムJ", 10],
]
columns = ["user_id", "content_id", "title", "rank"]
wandb.log({"sample_recommended_items": wandb.Table(data=data, columns=columns)})
# # 実行終了時にwandb.finish()を呼ぶ (省略可、自動で呼ばれる)
# wandb.finish()
