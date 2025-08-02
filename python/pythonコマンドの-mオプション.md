- refs:
  - https://misprochef.com/posts/python-m-option/

# pythonコマンドの-mオプションの話

- `-m`オプションは「**module option**」と呼ばれる。
- `python -m <module-name>`の形式で使用する。
  - モジュールとはPythonの文が入ったファイルのこと。(i.e. `.py`ファイル)
  - モジュールの他に、パッケージも`-m`オプションを付与して実行できる。
- どういう仕組み??
  - `-m`の後に続く指定されたモジュールを`sys.path`から探し、それを`__main__`のスクリプトとして実行する。
  - パッケージの場合は、トップディレクトリにある`__init__.py`の内容から、`__main__`のスクリプトを探して実行する。
