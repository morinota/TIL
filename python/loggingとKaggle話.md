# なぜKaggleでログを取りたいか

Kaggleのようなコンペティションにおいて、ログを取る目的は大きく二つ。

## プログラムの実行記録。デバッグやボトルネックの発見のため

- 機械学習プログラムの実行時間は長くなりがち。試行錯誤の回数を得るためにもボトルネックは把握して解消したい。
- バグもエラーが出るものばかりではない。自分の意図した処理になっているのか後から確認できるようにしたい。

## 実験や各種試行錯誤、機械学習の学習過程の記録のため

- いろいろ思いついたことを片っ端から試していくことになる。何をやって何をやってないのかの記録が必要。
- 機械学習を行った際の学習過程は次の試行の方針を決めるために必要な情報。当然取得して記録したい。

# どういう情報が欲しいか

次に、前節を踏まえてどのような情報がどのような形式で欲しいかを考える。

## 実行時間の記録

- それぞれのモジュール単位で確認できればベスト。そうでなくともログの記録時には時間も一緒に記録してほしい。
- 実行時には標準出力に実行過程の概略を流しつつ詳細は別途ログファイルに保存とかしたい。
- 出来れば簡潔に記述したい。timeモジュールを使って挟みこむようなものはあまり書きたくない。

## 処理過程の記録

- 例えばDataFrameの列数を記録するなどはしたい。学習直前に行えば利用している特徴量の記録になる。
- 特に学習過程の記録はフォーマットをそろえて後からスクリプトやノートブックで取り扱いがしやすい形にしておくと便利。

上記の記録をそれぞれ管理しつつコンペ中に実施する多量の実験ごとに整理したい。

# 現状の著者のログ取得方法

## 基本

pythonのloggingモジュールを利用して記録する。

- 公式でも推奨されているように可能な限りroot loggerは使わずにすましたい。
- しかし、複数のモジュールに渡って同じ実験ごとのloggerにログを投げ込んでほしい。
- かと言ってすべての関数にloggerを引数として与えるなんてことはしたくない。

そこで以下のようなモジュールを作り、これを利用して関数としてloggerを取得することにする。

```python
## base_log.py

from pathlib import Path
from logging import getLogger, Formatter, FileHandler, StreamHandler, INFO, DEBUG


def create_logger(exp_version):
    log_file = ("path / to / log / {}.log".fomat(exp_version)).resolve()

    # logger
    logger_ = getLogger(exp_version, mode="w")
    logger_.setLevel(DEBUG)

    # formatter
    fmr = Formatter("[%(levelname)s] %(asctime)s >>\t%(message)s")

    # file handler
    fh = FileHandler(log_file)
    fh.setLevel(DEBUG)
    fh.setFormatter(fmr)

    # stream handler
    ch = StreamHandler()
    ch.setLevel(INFO)
    ch.setFormatter(fmr)

    logger_.addHandler(fh)
    logger_.addHandler(ch)


def get_logger(exp_version):
    return getLogger(exp_version)
```

あとは上記のモジュールを実際の実験スクリプトや各種モジュールで読み込んで以下のように記述する。

```python
## main.py
from base_log import create_logger, get_logger

VERSION = "xxxx" # 実験番号

if __name__ == "__main__":
    create_logger(VERSION)
    get_logger(VERSION).info("メッセージ")
```

これで"path / to / log / VERSION.log"が生成され実験番号に応じたログが取れる。

## 実行時間の記録

[https://qiita.com/hisatoshi/items/7354c76a4412dffc4fd7]を参考にしてデコレータを用いた実行時間計測を行う。この時にデコレータ側で実験番号に応じたloggerを呼び出してあげれば実行時間をloggerを利用して計測と記録ができる。

```python
## time_keeper.py
import time
from functools import wraps
from base_log import get_logger

def stop_watch(VERSION):

    def _stop_watch(func):
        @wraps(func)
        def wrapper(*args, **kargs):
            start = time.time()

            result = func(*args, **kargs)

            elapsed_time = int(time.time() - start)
            minits, sec = divmod(elapsed_time, 60)
            hour, minits = divmod(minits, 60)

            get_logger(VERSION).info("[elapsed_time]\t>> {:0>2}:{:0>2}:{:0>2}".format(hour, minits, sec))
        return wrapper

    return _stop_watch
```

あとは上記のモジュールを利用するだけ。

```python
## main.py
from base_log import create_logger, get_logger
from time_keeper import stop_watch

VERSION = "xxxx" # 実験番号


@stop_watch(VERSION)
def function():
    "--- hoge hoge ---"


if __name__ == "__main__":
    create_logger(VERSION)
    function()
```

## 処理過程の記録

これは一番最初の方法を用いて"メッセージ"に適宜ほしい情報を入れてしまうのが良いと思われるので省略。

## 実験の記録

この辺りは先達のkagglerの方たちの記事があるので[コレ](https://yutori-datascience.hatenablog.com/entry/2017/08/19/195049)とか[ソレ](https://amalog.hateblo.jp/entry/lightgbm-logging-callback)の方を見ていただいた方が良いかもしれない。というか二つ目のamaotone(@SakuEji)さんの記事なんかもろ一致。じゃあここで何を書くのかだが素直にコードを載せるくらいにしておく。

方針は今までと一緒で外部モジュールにして読み込んで実験スクリプトで利用することを想定している。

## lgbm_log.py

```python
from logging import DEBUG
from lightgbm.callback import _format_eval_result
from base_log import get_logger


def lgbm_logger(VERSION, level=DEBUG, period=1, show_stdv=True):

    def _callback(env):
        if period > 0 and env.evaluation_result_list and (env.iteration + 1) % period == 0:
            result = '\t'.join([_format_eval_result(x, show_stdv) for x in env.evaluation_result_list])
            get_logger(VERSION).log(level, "[%d]\t%s" % (env.iteration + 1, result))
    _callback.order = 10
    return _callback
```

あとは上記のモジュールをよしなに。

```python
## main.py
from base_log import create_logger, get_logger
from time_keeper import stop_watch

VERSION = "xxxx" # 実験番号

def function():
    "--- hoge hoge ---"
    clf = lgb.LGBMClassifier(**lgb_params)
    clf.fit(
        train,
        y,
        "--- hoge hoge ---"
        callbacks=[lgbm_logger(VERSION)]
    )

if __name__ == "__main__":
    create_logger(VERSION)
    function()
```

# 参考

- Python Logging in Kaggle
  - https://icebee.hatenablog.com/entry/2018/12/16/221533
