# 1. Locustについてのメモ

## 1.1. refs

- <https://qiita.com/k-keita/items/9811ab2597992da8c0cc>
- 公式ドキュメント: <https://docs.locust.io/en/stable/index.html>
- <https://zenn.dev/secondselection/articles/locust_sample>

## 1.2. locustの概要

- OSSの負荷テストツール。
- 特徴1: Pythonでテストシナリオを記述可能
  - **通常のPythonコードとしてテストシナリオを記述できる**。
  - 繰り返し処理、条件分岐、計算などもPythonの構文で記述可能。
  - 各ユーザーは独自のグリーンレット（軽量プロセス/コルーチン）内で実行。
  - コールバックや特殊な構文を使わず、直感的なブロッキングコードで記述可能。
  - テストを通常のコードとしてバージョン管理やIDEで編集できる。
-

## 1.3. locustfile.pyの書き方について

Locustを使った負荷テストの際には、テストシナリオをPythonコードとして記述する必要がある。その際には、`locustfile.py`というファイルにテストシナリオを記述するのが一般的。

### 1.3.1. Locustfileの最小構成

```python
from locust import HttpUser, task, between

class MyUser(HttpUser):
    @task
    def my_task(self):
        self.client.get("/")

    wait_time = between(1, 5)
```

- `HttpUser`クラス
  - 負荷テストを行うユーザを表すクラス。
  - このクラス内にタスクを記述して、ユーザが行う操作をシミュレートする。
  - **テストが開始されると、Locustはシミュレートするユーザ毎に、このクラスのインスタンスを作成し、各ユーザは独自のグリーンレット内(i.e. 軽量プロセス/コルーチン)で実行される**。
- `@task`デコレータ
  - ユーザが行う操作を記述するメソッドに付与するデコレータ。
  - **宣言されたタスクはランダムに選ばれる**。
  - タスクの実行が終わると、ユーザは`wait_time`属性で指定された時間だけスリープし、そこから新しいタスクを選択する。
  - **タスクの選択は、`@task`デコレートされたメソッドだけが選ばれるので、開発者は好きなように内部のhelperメソッドを定義してOK**!!
- `wait_time`属性
  - 各タスクの実行後に、ユーザに待ち時間を設定するための属性。
  - [詳細は `wait_time` attribute の項目を参照。](https://docs.locust.io/en/stable/writing-a-locustfile.html#wait-time)
- `self.client`属性
  - self.clientは`HttpSession`のインスタンス。`HttpSession`は、`requests.Session`をwrapしたもの。**このwrapperによって、リクエスト結果をLocustに記録できる**（success/fail, response time, response length, name, etc.）。
  - [より詳しいリクエストやレスポンスの検証方法は、こちらを参照](https://docs.locust.io/en/stable/writing-a-locustfile.html#client-attribute-httpsession)。

### 1.3.2. タスク間の重みづけ

ユーザが複数の操作を行う場合、どのタスクをどの程度の割合で実行するかを設定することができる。
下記の例の場合、`high_priority_task`は`low_priority_task`の3倍多く実行される。

```python
from locust import HttpUser, task, between

class MyUser(HttpUser):
    @task(3)
    def high_priority_task(self):
        self.client.get("/important")

    @task(1)
    def low_priority_task(self):
        self.client.get("/less_important")

    wait_time = between(1, 2)
```

### 1.3.3. ユーザごとに異なるデータや状態を管理する

`on_start`メソッドや`on_stop`メソッドを使って、ユーザごとに異なるデータや状態を管理することができる。

- `on_start`メソッド
  - テスト開始時に、ユーザ固有のデータを初期化する。
- `on_stop`メソッド
  - テスト終了時に、リソースの解放やログの出力などの後処理を行う。

```python
from locust import HttpUser, task, between

class MyUser(HttpUser):
    @task
    def my_task(self):
        self.client.get(f"/user/{self.user_id}")

    def on_start(self):
        self.user_id = 42  # ユーザー固有のデータを初期化

    def on_stop(self):
        print(f"ユーザー {self.user_id} のテスト終了")
```
