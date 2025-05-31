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
