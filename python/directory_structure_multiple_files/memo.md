## refs:

- [FastAPI ユーザガイド Bigger Applications - Multiple Files](https://fastapi.tiangolo.com/ja/tutorial/bigger-applications/)

# ディレクトリ構造について。

- アプリケーションやWeb APIを構築する場合、全てを1つのファイルにまとめられることはまずない。

## ディレクトリ構造の例:

```plaintext
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   └── routers
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   └── internal
│       ├── __init__.py
│       └── admin.py
```

意味合い:

- appディレクトリには全てが含まれている。
  - そして、`app/__init__.py`という空のファイルがあるので、これは`app`という"Python package"("Python module"の集まり)として扱われる。
- `app/main.py`ファイルがある。
  - これはPython package (__init__.pyファイルがあるディレクトリ)の中にあるので、そのpackageの"module"である。
  - `app.main` module。
- `app/dependencies.py`ファイルがある。
  - これもPython packageの中にあるので、そのpackageの"module"である。
  - `app.dependencies` module。
- `app/routers/`というサブディレクトリがあり、その中に別の`__init__.py`ファイルがある。
  - よって、これは `app.routers` という"Python subpackage"である。
- `app/routers/items.py`ファイルがある。
  - これは `app.routers.items` というsubmoduleである。
- `app/routers/users.py`ファイルがある。
  - これも同様に、 `app.routers.users` というsubmoduleである。
- `app/internal/`というサブディレクトリがあり、その中に別の`__init__.py`ファイルがある。
  - よって、これも `app.internal` という"Python subpackage"である。
  - `app.internal.admin.py`ファイルがある。これは `app.internal.admin` というsubmoduleである。

同じファイル構造にコメントをつけたもの:

```plaintext
.
├── app                  # "app" is a Python package
│   ├── __init__.py      # this file makes "app" a "Python package"
│   ├── main.py          # "main" module, e.g. import app.main
│   ├── dependencies.py  # "dependencies" module, e.g. import app.dependencies
│   └── routers          # "routers" is a "Python subpackage"
│   │   ├── __init__.py  # makes "routers" a "Python subpackage"
│   │   ├── items.py     # "items" submodule, e.g. import app.routers.items
│   │   └── users.py     # "users" submodule, e.g. import app.routers.users
│   └── internal         # "internal" is a "Python subpackage"
│       ├── __init__.py  # makes "internal" a "Python subpackage"
│       └── admin.py     # "admin" submodule, e.g. import app.internal.admin
```

### dependencies moduleについて

- アプリケーションのいくつかの場所で使用される依存関係が必要になりそう。
  - (ここでの依存関係って?
- なので、それらを独自のdependencies module (`app/dependencies.py`)に配置する。



### relative importsがどのように動作するか??

```python:app/routers/items.py
from ..dependencies import get_token_header

...
```

#### single dot `.` の動作

```python
from .dependencies import get_token_header
```

上のようなsingle dotが意味すること:

- **このモジュール(app/routers/items.py)と、同じパッケージ(app/routers/ディレクトリ)から開始する**。
- モジュールの依存関係（app/routers/dependencies.py にある架空のファイル）を見つける。
- そこから `get_token_header` 関数をインポートする。


#### double dot `..` の動作


```python
from ..dependencies import get_token_header
```

上のようなdouble dotが意味すること:

- このモジュール(app/routers/items.py)がある同じパッケージ (app/routers/ディレクトリ) から始める...
- 親パッケージ (app/ディレクトリ) に移動する...
- で、そこからdependencies module (`app/dependencies.py`) を見つける。
- そこから、`get_token_header` 関数をインポートする。

同様に、tripple dot `...` が意味することも以下:

```python
from ...dependencies import get_token_header
```

- このモジュール(app/routers/items.py)がある同じパッケージ (app/routers/ディレクトリ) から始める...
- 親パッケージ (app/ディレクトリ) に移動する...
- 更に親パッケージ に移動する... (appはtop levelなので、親パッケージは存在しない)
  - app/の上にある、独自ファイル`__init__.py`などを持つパッケージを参照しようとするが、しかし我々はそれを用意していない。なのでこの例ではエラーになる...!
  - (`__init__.py`ファイルがないと、Pytshonはディレクトリをパッケージとして扱わないのか...??)S
- で、そこからdependencies moduleを見つけようとする。
- そこから、`get_token_header` 関数をインポートしようとする。



