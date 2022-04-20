# ログレベルとは

ログに出力される情報には、実行時に悪影響を及ぼす度合いによって以下のようにレベル分けがある。

| 名前     | 設定値 | 役割                           |
| -------- | ------ | ------------------------------ |
| NOTSET   | 0      | 設定値などの記録（全ての記録） |
| DEBUG    | 10     | 動作確認などデバッグの記録     |
| INFO     | 20     | 正常動作の記録                 |
| WARNING  | 30     | ログの定義名                   |
| ERROR    | 40     | エラーなど重大な問題           |
| CRITICAL | 50     | 停止など致命的な問題           |

loggingモジュールを使うと、どのレベルからログとして残すかを選択できる。

例えば開発中はDebugまでの全てを出力し、プログラムが出来てからはInfo以降を出力するといった具合です。

# loggingモジュールの基本的な使い方

## Loggerオブジェクトの生成、コンソールへのログ出力

```python
import logging

# ログの出力名を設定（1）
logger = logging.getLogger('LoggingTest')

# ログをコンソール出力するための設定（2）
sh = logging.StreamHandler()
logger.addHandler(sh)

# log関数でログ出力処理（3）
logger.log(20, 'info')
logger.log(30, 'warning')
logger.log(100, 'test')
```

これをコンソールで実行すると

```
python sample.py
```

実行結果

```
warning
test
```

上記サンプルコードのポイント3点。

- getLoggerメソッドを使って**loggerオブジェクトを生成**する。
  - 引数に文字列を入れることで、ログの出力名を設定することが可能。
- StreamHandlerクラスを使ってコンソールにログを出力するよう設定する。
  - 第1引数には、前章のログレベルの数値を渡す
  - 第2引数にはメッセージとしてログに出力する文字列を入力
- log関数を使ってログを出力させる

ログ出力を行うものの総称をロガー(Logger)という。
loggingモジュールの場合、**Loggerオブジェクト**がロガーに当たる。

### 出力するログレベルの変更

また、出力するログレベルを変更するには、Loggerオブジェクトのインスタンス変数`setLevel()`を呼ぶ。(デフォルトは30?)

### 各ログのログレベルの設定方法

たぶんどっちでもOK

```python
# log関数でログ出力処理（3）
logger.log(20, 'info')
logger.log(30, 'warning')
logger.log(100, 'test')
```

```python
#それぞれのログレベルに応じた関数を呼び出す
logger.info('info')
logger.warning('warning')
logger.error('test')
```

## ログをファイルに出力する

これまでのサンプルコードでは、ログファイルの出力先などを決めることはできない。

```python
import logging

# ログの出力名を設定（1）
logger = logging.getLogger('LoggingTest')

# ログレベルの設定（2）
logger.setLevel(10)

# ログのコンソール出力の設定（3）
sh = logging.StreamHandler()
logger.addHandler(sh)

# ログのファイル出力先を設定（4）
fh = logging.FileHandler('test.log')
logger.addHandler(fh)

logger.log(20, 'info')
logger.log(30, 'warning')
logger.log(100, 'test')

logger.info('info')
logger.warning('warning')
```

(4)では、ログのファイル出力先が設定されています。このようにファイル名を指定しておくことにより、ログをファイルに出力することができるようになります。

## ログのフォーマットを指定する

これまでのサンプルコードでは、ログの出力形式の設定はしていませんでした。
ログとして、実行時刻やログの出力した場所、ログレベル名、メッセージなどを揃って出力させる事ができる。

ログの出力形式を設定するためには、`logging`モジュールの`Formatter`クラスを用いる。

```python
import logging

# ログの出力名を設定
logger = logging.getLogger('LoggingTest')

# ログレベルの設定
logger.setLevel(10)

# ログのコンソール出力の設定
sh = logging.StreamHandler()
logger.addHandler(sh)

# ログのファイル出力先を設定
fh = logging.FileHandler('test.log')
logger.addHandler(fh)

# ログの出力形式の設定
formatter = logging.Formatter('%(asctime)s:%(lineno)d:%(levelname)s:%(message)s')
fh.setFormatter(formatter)
sh.setFormatter(formatter)

logger.log(20, 'info')
logger.log(30, 'warning')
logger.log(100, 'test')

logger.info('info')
logger.warning('warning')
```

実行結果

```python
2017-05-16 12:14:49,510:27:INFO:info
2017-05-16 12:14:49,511:28:WARNING:warning
2017-05-16 12:14:49,511:29:Level 100:test
2017-05-16 12:14:49,511:31:INFO:info
2017-05-16 12:14:49,511:32:WARNING:warning
```

`Formatter`クラスの引数に出力形式を渡して、formatterのインスタンスを作成している。この例では、

```
実行時間(年-月-日 時-分-秒,ミリ秒):行番号:ログレベル名:メッセージ文字列
```

の形式で出力されるような設定。

形式のフォーマットは以下。
| フォーマット | 役割 |
|---------------|---------|
| %(asctime)s | 実行時刻 |
| %(filename)s | ファイル名 |
| %(funcName)s | 行番号 |
| %(levelname)s | ログの定義 |
| %(lineno)d | ログレベル名 |
| %(message)s | ログメッセージ |
| %(module)s | モジュール名 |
| %(name)s | 関数名 |
| %(process)d | プロセスID |
| %(thread)d | スレッドID |

# (応用)Configファイルで、ログのフォーマットを指定する。

# 参考

- https://www.sejuku.net/blog/23149
