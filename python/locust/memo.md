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
  - **テストが開始されると、Locustはシミュレートするユーザ毎に、このクラスのインスタンスを作成し、各ユーザは独自のgreedlet内(i.e. 軽量プロセス/コルーチン)で実行される**。
- `@task`デコレータ
  - ユーザが行う操作を記述するメソッドに付与するデコレータ。
  - **宣言されたタスクはランダムに選ばれる**。
  - タスクの実行が終わると、ユーザは`wait_time`属性で指定された時間だけスリープし、そこから新しいタスクを選択する。
  - **タスクの選択は、`@task`デコレートされたメソッドだけが選ばれるので、開発者は好きなように内部のhelperメソッドを定義してOK**!!
  - 単一タスク内のコードは通常のPythonコードと同様にsequentialに実行される。(じゃあ、**ユーザの操作に順番を持たせたい場合は、同一タスク内に記述すれば良さそう**...!!:thinking_face:)
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

## テストの実行コマンドについて

- 参考: <https://docs.locust.io/en/stable/configuration.html>

### テストの実行

locustコマンドでテストを実行する。

```bash
locust -f locustfile.py --host http://example.com
```

これを実行すると...

- Web UIが起動
  - <http://localhost:8089> にアクセスすると、テスト設定画面が表示される。
  - 同時にテストするユーザー数（コンカレントユーザー数）や、1秒あたりの新規ユーザー生成数を設定できます。

また、Web UIではなく、**CLI上で直接実行も可能**。

```bash
locust --headless -u 10 -r 1 -t 1m --host http://example.com
```

ここで...

- `--headless`: GUIを表示せずにCLIモードで実行。
- `-u`: テストユーザ数(ex. 10)
- `-r`: 1秒あたり生成する新規ユーザ数
- `-t`: テストの実行時間 (ex. 1分)

### テスト結果の確認

csvでレポート保存

```bash
locust --headless -u 10 -r 1 -t 1m --host http://example.com --csv=results
```

- `--csv=`オプションで指定したprefix以下に、`_requests.csv`と`_stats.csv`が保存される。
  - 上記の例では`--csv=results`と指定しているので、`results_requests.csv`と`results_stats.csv`が保存される。

### locustコマンドのオプション指定方法

- 前提として、オプションの設定方法は、3種類くらいありそう。
  - 1. locustコマンドの後にオプションを指定する方法
  - 2. 環境変数として設定する方法
    - `LOCUST_*`で始まる環境変数を設定することで、オプションを設定できる。典型的に、コマンドライン引数と同名で、`LOCUST_`を付けて大文字にしたものを指定できる。
  - 3. configファイルに設定する方法
    - locustはデフォルトで、`~/.locust.conf`, `./locust.conf`, `./pyproject.toml`を探すとのこと。
    - `locust --config path/to/myconfig.conf`のように明示的に指定することもできる。

### locustコマンドのオプション一覧メモ

基本設定(general settings)(よく使いそう!:thinking_face:)

- `-f, --locustfile` / `LOCUST_LOCUSTFILE` / `locustfile`
  - テストを記述したPythonファイルまたはモジュールを指定。
  - 例: `my_test.py`、複数のファイルをカンマ区切りで指定可能。
  - デフォルト: `locustfile`
- `-H, --host` / `LOCUST_HOST` / `host`
  - 負荷テスト対象のホストURL。
  - 例: `http://example.com`
- `-u, --users` / `LOCUST_USERS` / `users`
  - 最大同時ユーザー数を指定。
- `-r, --spawn-rate` / `LOCUST_SPAWN_RATE` / `spawn-rate`
  - 1秒あたりに生成する新規ユーザー数。
- `-t, --run-time` / `LOCUST_RUN_TIME` / `run-time`
  - テスト実行時間を指定。
  - 例: `300s`（秒）、`10m`（分）、`1h`（時間）。
- `--config-users` / `LOCUST_CONFIG_USERS` / `config-users`
  - ユーザー設定をJSON文字列またはJSONファイルで指定。

タスク制御（Task Control）

- **`-T, --tags` / `LOCUST_TAGS` / `tags`**
  - 実行するタスクのタグを指定。
- **`-E, --exclude-tags` / `LOCUST_EXCLUDE_TAGS` / `exclude-tags`**
  - 実行しないタスクのタグを指定。

ログと統計情報（Logging and Statistics）

- **`--csv` / `LOCUST_CSV` / `csv`**
  - テスト結果をCSV形式で保存。
- **`--csv-full-history` / `LOCUST_CSV_FULL_HISTORY` / `csv-full-history`**
  - 統計履歴をCSVに完全保存。
- **`--print-stats` / `LOCUST_PRINT_STATS` / `print-stats`**
  - 定期的に統計情報を表示。
- **`--only-summary` / `LOCUST_ONLY_SUMMARY` / `only-summary`**
  - ヘッドレスモードで詳細統計を無効化。
- **`--reset-stats` / `LOCUST_RESET_STATS` / `reset-stats`**
  - 統計情報をリセット。
- **`--html` / `LOCUST_HTML` / `html`**
  - HTML形式のテスト結果を保存。

Web UI設定（Web UI Settings）(まあローカルで起動する分にはあまり使わなさそう)

- `--web-host` / `LOCUST_WEB_HOST` / `web-host`
  - Webインターフェースがlistenする(=リクエストを受け付ける)ホストアドレス。
  - デフォルト: `*`（すべてのインターフェース）
- `--web-port, -P` / `LOCUST_WEB_PORT` / `web-port`
  - Web UIがlistenするポート番号。
  - デフォルト: `8089`
- `--headless` / `LOCUST_HEADLESS` / `headless`
  - Webインターフェースを無効化し、即座にテストを開始。
- `--autostart` / `LOCUST_AUTOSTART` / `autostart`
  - Web UIを有効にしたままテストを自動開始。
- `--autoquit` / `LOCUST_AUTOQUIT` / `autoquit`
  - テスト終了後、指定秒後にLocustを終了。
- `--web-login` / `LOCUST_WEB_LOGIN` / `web-login`
  - Web UIにアクセスするための認証情報を設定。
  - 形式: `username:password`
- `--tls-cert` / `LOCUST_TLS_CERT` / `tls-cert`
  - HTTPS用のTLS証明書ファイルのパス。
- `--tls-key` / `LOCUST_TLS_KEY` / `tls-key`
  - HTTPS用のTLS秘密鍵のパス。
- `--web-base-path` / `LOCUST_WEB_BASE_PATH` / `web-base-path`
  - Web UIのベースパスを設定（例: `/locust`）

その他のオプション（Miscellaneous）

- **`--skip-log-setup` / `LOCUST_SKIP_LOG_SETUP` / `skip-log-setup`**
  - Locustのデフォルトログ設定を無効化。
- **`--loglevel, -L` / `LOCUST_LOGLEVEL` / `loglevel`**
  - ログレベルを指定（例: `DEBUG`, `INFO`, `WARNING`）。
- **`--logfile` / `LOCUST_LOGFILE` / `logfile`**
  - ログファイルの保存先。
- **`--exit-code-on-error` / `LOCUST_EXIT_CODE_ON_ERROR` / `exit-code-on-error`**
  - テスト失敗時の終了コードを設定。
  - **デフォルト**: `1`
- **`-s, --stop-timeout` / `LOCUST_STOP_TIMEOUT` / `stop-timeout`**
  - 全ユーザーのタスク終了を待機する時間。
