## refs

- [gokartを使ってみる](https://www.nogawanogawa.com/entry/gokart)
- [機械学習プロジェクト向けPipelineライブラリgokartを用いた開発と運用](https://www.m3tech.blog/entry/2019/09/30/120229)
- [Gokart Intro](https://gokart.readthedocs.io/en/latest/intro_to_gokart.html)

# ログについて

- gokartは機械学習に必要なすべての情報を記録する。

  - デフォルトでは、`resource`はスクリプトと同じディレクトリに生成される。
  - タスクをダンプした結果は`__name__`(**main**とか!)ディレクトリに保存される。

- タスクのパラメータに応じてハッシュ値が与えられており、ログファイル名は`{task名}_{ハッシュ値}.pkl`になる。
  - タスクのパラメータを変更すると、ハッシュ値が変更され、出力ファイルも変更される。
    - これはパラメータを変更したり、実験したりするときに非常に便利!
  - taskのパラメータについては[タスクパラメータセクション](https://gokart.readthedocs.io/en/latest/task_parameters.html)を参照。
  - また、ログの出力先を返す方法については、[TaskOnKart](https://gokart.readthedocs.io/en/latest/task_on_kart.html)セクションを参照。

さらに、以下のファイルが自動的にログとして保存される:

- module_versions： スクリプト実行時にインポートされた全モジュールのバージョン。再現性のため。
- processing_time： タスクの実行時間。
- random_seed： pythonとnumpyのランダムシード。機械学習での再現性のため。[タスク設定](https://gokart.readthedocs.io/en/latest/task_settings.html)のsectionを参照。
- task_log： タスクロガーの出力。
- task_params: タスクのパラメータ [タスクパラメータ](https://gokart.readthedocs.io/en/latest/task_parameters.html)ーのsectionを参照。

# Taskの実行方法

- Taskを走らせるには`run()`もしくは`build()` methodを呼ぶ。それぞれが異なる目的を持つ:

  - `run()`: シェルの引数を使える。(たぶん直接渡す事はできなさそう?)
  - `build()`:jupyter notebookやIPythonなどのインラインコードで使用する。(runとは異なり、buildはパラメータを引数にわたすってこと?)

- 注意点:
  - gokart.runとgokart.buildを同じスクリプトで一緒に使用することは非推奨。
    - ->gokart.buildは`luigi.register`(??)の内容をクリアしてしまうから。

## gokart.run

```python
import gokart
import luigi

class SampleTask(gokart.TaskOnKart):
    param = luigi.Parameter()

    def run(self):
        self.dump(self.param)

gokart.run()
```

run()の場合は、↑をshellで実行する。

```shell
python sample.py SampleTask --local-scheduler --param=hello
```

これをPythonで書くと、次のような動作になる。(実際には動かないやつ??)

```python
gokart.run(['SampleTask', '--local-scheduler', '--param=hello'])
```

## gokart.build

run()に対して、build()はinline codeで動く

```python
import gokart
import luigi

class SampleTask(gokart.TaskOnKart):
    param = luigi.Parameter()

    def run(self):
        self.dump(self.param)

gokart.build(SampleTask(param='hello'), return_value=False)
```

各タスクのログを出力するには、以下のように`log_level`パラメータをbuild()に渡す:

```python
gokart.build(SampleTask(param='hello'), return_value=False, log_level=logging.DEBUG)
```

- この機能は、jupyterノートブック上で~gokartを実行する際に非常に便利。
  - いくつかのタスクが失敗すると、gokart.buildはGokartBuildErrorを発生させる。
  - トレースバックを取得する必要がある場合は、log_levelを`logging.DEBUG`に設定してください。

# Make gokart project

cookiecutter自体は、gokartに関わらず、python project のtemplateを作るやつっぽい。(https://github.com/cookiecutter/cookiecutter)

cookiecutter-gokartを使ってprojectを作る。(確かテンプレート的なやつだっけ?)(デフォルト値でいい場合は空白のままEnterを押せばOK)

```shell
cookiecutter  https://github.com/m3dev/cookiecutter-gokart

project_name [project_name]: m3sample   # プロジェクトのルートディレクトリ名
package_name [package_name]: sample    # Pythonモジュールにする際のパッケージ名
python_version [3.6]:    # 利用するPythonバージョン
author [your name]: m3dev    # 作成者の名前
package_description [What is this project?]: this is sample    # 作るプロジェクトの説明文
license [MIT License]:    # 利用するライセンス
```

↑で、以下の様なgokartプロジェクトのディレクトリツリーが作られる:

```
tree example/

example/
├── Dockerfile
├── README.md
├── conf # configファイルのサンプル
│   ├── logging.ini
│   └── param.ini
├── gokart_example
│   ├── __init__.py
│   ├── model
│   │   ├── __init__.py
│   │   └── sample.py # sample taskのスクリプト
│   └── utils
│       └── template.py
├── main.py # sampleタスクを動作させる為のmain
├── pyproject.toml
└── test
    ├── __init__.py
    └── unit_test # sampleタスクのunit testスクリプト
        └── test_sample.**py**

# モジュールとして利用する為のsetup.pyもあるはずなんだけど...??
```

内容は以下:

- sampleタスクのスクリプト
- configのsample
- sampleタスクを動作させるためのmain.py
- sampleタスクのunittestスクリプト
- モジュールとして利用するためのsetup.py
- unittestをチェックするためのGitHub Actions CI/CD
- LICENSE、README.md

- このcookiecutter-gokartを利用する事で、GitHub上でgokartプロジェクトをすぐ始められるはず。
  - エムスリー社内でも社内向けの設定を付与したものを多く利用している程、**gokartでcookiecutterを利用する価値は高い**と考えている。
  - Pipelineで忘れがちなテストコードについてもサンプルを示していますので、参考にして!

## 注意点:

module version(の管理の話??)の観点からpoetryを使用する方が良い。(.requirements.txtでも多分良さそう。)

```
poetry lock
poetry run python main.py gokart_example.Sample --local-scheduler
```

さらに安定させたい場合は docker を使ってください。

```
docker build -t sample .
docker run -it sample "python main.py gokart_example.Sample --local-scheduler"
```

## Taskを作ってみる。

gokart-likeなtaskを作ってみる.

```python
from logging import getLogger
import gokart
from gokart_example.utils.template import GokartTask
logger = getLogger(__name__)


class Sample(GokartTask):
    def run(self):
        self.dump('sample output')


class StringToSplit(GokartTask):
    """Like the function to divide received data by spaces."""
    task = gokart.TaskInstanceParameter()

    def run(self):
        sample = self.load('task')
        self.dump(sample.split(' '))


class Main(GokartTask):
    """Endpoint task."""
    def requires(self):
        return StringToSplit(task=Sample())
```

- MainとStringToSplitを追加した。
  - `StringToSplit`は関数のようなタスクで、任意のタスクの結果をロードしてスペースで分割する。
  - `Main`は`StringToSplit`にSampleを注入する。Endpointのようなもの。

Let’s run the `Main` task.

```
python main.py gokart_example.Main --local-scheduler
```

loggerのoutputを見てみる.

```
===== Luigi Execution Summary =====

Scheduled 3 tasks of which:
* 1 complete ones were encountered:
    - 1 gokart_example.Sample(...)
* 2 ran successfully:
    - 1 gokart_example.Main(...)
    - 1 gokart_example.StringToSplit(...)

This progress looks :) because there were no failed tasks or missing dependencies

===== Luigi Execution Summary =====
```

ログが示すように、Sampleは一度実行されているので、キャッシュが使われる。(なるほど...!:thinking:) 今回動いたのはMainとStringToSplitだけ。

出力は以下のようになり、結果はStringToSplit_b8a0ce6c972acbd77eae30f35da4307e.pklに入っている。

## Taskの再実行(Rerun)

taskのrerunには2つの方法がある。

- `rerun parameter`を変更する(各taskの`rerun` argumentをTrueを指定する??)
- `parameters of the dependent tasks`を変更する

`gokart.TaskOnKart`クラスはそれぞれ、`rerun`parameter を指定できる:

```python
class Main(GokartTask):
    rerun=True

    def requires(self):
        return StringToSplit(task=Sample(rerun=True), rerun=True)
```

もしくは、依存しているタスクに新しいパラメータを追加する。(rerunしたいケースの度に都度書き換えるってこと? まあTaskが同一ではなくなればキャッシュは使えないだろうし:thiknking:)

```python
class Sample(GokartTask):
    version = luigi.IntParameter(default=1)

    def run(self):
        self.dump('sample output version {self.version}')
```

- どちらの方法でも、依存する全てのTaskが再実行される。
- 2つの方法の違いは、出力ファイルに与えられるハッシュ値が同じか変わるか。
  - 一つ目の方法において、reurnパラメータはハッシュ値に影響を与えない。つまり、同じハッシュ値で再実行される。
  - 一方で2つ目の方法では、Sampleタスクに新しいパラメータを追加するので、このパラメータはSampleのハッシュ値を変更し、別の出力ファイルを生成する。そして、依存タスクであるStringToSplitのハッシュ値も変更され、再実行される。

## tutorialの終わり

ゴーカートのチュートリアルはこれで終わりです。チュートリアルはいくつかの機能の紹介です。まだまだ便利な機能があります。

タスクの便利な機能については、[TaskOnKart](https://gokart.readthedocs.io/en/latest/task_on_kart.html)セクション、[For Pandas](https://gokart.readthedocs.io/en/latest/for_pandas.html)セクション、[タスクパラメータ](https://gokart.readthedocs.io/en/latest/task_parameters.html)セクションを参照してください。

それではよいゴカートライフを。
