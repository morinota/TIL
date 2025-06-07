## pytestのカスタムマーク機能について

- refs:
  - [Pytestでカスタムマークを使って特定のテストのみを実行する](https://dev.classmethod.jp/articles/pytest-mark/)
  - pytest公式 [Working with custom markers](https://docs.pytest.org/en/stable/example/markers.html)

### 何それ??

- pytestのカスタムマーク機能は、テスト関数やクラスに「ラベル」みたいなのをペタッと貼れるやつ。
  - テストをグループ分けしたり、**「このテストだけ実行したい！」とか「これは重いテストだから除外したい！」みたいなときに活用できる**。
- 使い方:
  - `@pytest.mark.好きな名前`で、カスタムマーカーをテスト関数やテストクラスに付けられる。

ex.

```python
import pytest

@pytest.mark.webtest
def test_send_http():
    pass  # ここにテスト処理を書く
```

特定のカスタムマーカーをつけたテストケースだけを実行したい場合は、コマンドラインで`-m`オプションを使う。

```bash
pytest -m webtest
```

反対に、特定のカスタムマーカーをつけたテストケースを除外したい場合は、`not`を使う。

```bash
pytest -m "not webtest"
```

### カスタムマーカーはpytest.iniなどに登録しておくべき!

- pytest 5.0以降は、**pytest.iniにカスタムマーカーを登録**するのが推奨されてる。
  - 登録しておくと、警告（warnings）も出なくなるし、チームメンバーが各マーカーの意味を理解しやすくなる。

例: 以下のように1カスタムマーカーにつき1行書く。

```ini
[pytest]
markers =
    webtest: mark a test as a webtest.
    slow: mark a test as slow.
```

既存マーカーは、`pytest --markers`コマンドで確認できる。

```bash
pytest --markers
@pytest.mark.webtest: mark a test as a webtest.

@pytest.mark.slow: mark test as slow.
...
```

## pytestのモック機能について

- refs:
  - [pytestのmockerについて](https://qiita.com/tasa/items/eccec2705abfcddea87d)

### Pythonにおけるモック機能は2種類ある。

- 1つ目は、`unittest.mock`モジュールを使う方法。
  - Pythonの標準ライブラリに含まれてる。
  - カスタマイズ性が高いが、書き方が少し複雑。
- 2つ目は、`pytest-mock(mocker)`プラグインを使う方法。
  - pytestに完全に統合されてる。
  - よりpytestスタイルに適した書き方ができる。
  - `unittest.mock`よりもシンプルに書ける。
  - `unittest.mock`に比べて機能は制限されるが、多くのテストケースではそれで十分感。

まあ結局 `pytest-mock` は`unittest.mock`をラップしたものなので、ほとんどの機能は使えるみたい。

### pytestのモック機能の使い方

- pytestのモック機能は、`mocker`フィクスチャを使う。
  - `mocker`fixtureは `pytest-mock`プラグインをインストールすると自動的に使えるようになる。
  - `mocker`フィクスチャを使うと、スタブやスパイ、モックといったテストダブルを簡単に作成できる。
  - ちなみに、`mocker`フィクスチャのデータ型は`unittest.mock.MagicMock`。でも`pytest_mock`にタイプアノテーション用の`pytest_mock.MockerFixture`があるので、テスト関数のシグネチャのタイプヒントには`pytest_mock.MockerFixture`を使うと良さそう!

#### modker.stubメソッド

スタブは主に固定の値を返すために使用する。以下の例では、スタブを使用して外部APIからのレスポンスを模倣してる。

```python
def test_get_weather(mocker):
    stub_get_weather = mocker.stub(name='get_current_weather')
    stub_get_weather.return_value = {'temperature': 20}
    # ここでget_current_weather関数を呼び出すと、{'temperature': 20}を返します
``` 

#### mocker.patchメソッド

パッチは特定のメソッドや関数の実装を一時的に置き換えるために使用される。
(stubと同じような使い方ができるが、パッチの方が拡張性が高いっぽい)

```python
def test_get_weather(mocker):
    mock_get_weather = mocker.patch('weather.api.get_current_weather', return_value={'temperature': 20})
    # ここでget_current_weather関数を呼び出すと、{'temperature': 20}を返します
```

#### mockerでできること: 返り値のカスタマイズ

return_valueを使うと、モックの戻り値を自由に設定することができる。

#### mockerでできること: 例外のハンドリング

side_effectを使うと、モックが呼び出されたときに特定の例外を送出するように設定することも可能。
これにより、例外のハンドリングをテストすることが容易になる。

```python
def test_get_weather(mocker):
    mock_get_weather = mocker.patch('weather.api.get_current_weather')
    mock_get_weather.side_effect = Exception('API request failed')
    # ここでget_current_weather関数を呼び出すと、'API request failed'というメッセージの例外が送出されます
```

#### mockerでできること: メソッド呼び出しの確認

`assert_called_hogehoge`メソッドを使うと、モックが期待通りに呼び出されたかどうかを確認できる。

- `assert_called()`: モックが少なくとも1回呼び出されたことを確認する。
- `assert_called_once()`: モックが1回だけ呼び出されたことを確認する。
- `assert_called_with(*args, **kwargs)`: モックが特定の引数で呼び出されたことを確認する。
- `assert_called_once_with(*args, **kwargs)`: モックが1回だけ特定の引数で呼び出されたことを確認する。
- `assert_any_call(*args, **kwargs)`: モックが少なくとも1回は特定の引数で呼び出されたことを確認する。
- `assert_has_calls(calls, any_order=False)`: モックが特定の呼び出し順序で呼び出されたことを確認する。
  - `any_order=True`を指定すると、呼び出し順序を無視して確認できる。
- `assert_not_called()`: モックが呼び出されなかったことを確認する。

```python
def test_get_weather(mocker):
    mock_get_weather = mocker.patch('weather.api.get_current_weather')
    # 何らかの処理...
    mock_get_weather.assert_called_once_with('Tokyo')
    # get_current_weather関数が一度だけ呼び出され、そのときの引数が'Tokyo'であることを確認します
```
