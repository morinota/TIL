import wandb

print("start wandb")
print(f"{wandb.__version__=}")

wandb.init(
    project="test-project",  # The name of the project(実験の人まとまり)
    # 1回の実行(run)名 (同名のrunが作れてしまうので注意!)
    # なので基本的には、timestampなどでユニークにするのが良さそうかも。
    name="test-run-1",
    config={  # hyperparameterなどを記録
        "my_dummy_param": 42,
        "my_other_param": "foo",
        "my_list_param": [1, 2, 3],
    },
)
# wandb.init()の返り値はRunオブジェクト。wandb.runでもアクセス可能。

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

# # 実行終了時にwandb.finish()を呼ぶ (省略可、自動で呼ばれる)
# wandb.finish()
