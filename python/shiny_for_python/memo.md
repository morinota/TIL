## refs:

- [Shiny for Python: Overview](https://shiny.posit.co/py/docs/overview.html)

# Shinyの概要:

## めっちゃ基礎:

- Shiny appsは一般的に、**input components** と **output components** から構成される。
  - input components: ユーザから情報を受け取るためのコンポーネント。
  - output components: ユーザに情報を表示するためのコンポーネント。
    - input componentsへの入力をreactive(反応的)にrenderingする。
      - (rendering = あるデータを処理または演算し表示することっぽい??:thinking_face:)

```python
from shiny.express import input, render, ui

# input component
ui.input_slider("val", "Slider label", min=0, max=100, value=50)

# output component ()
@render.text
def slider_val():
    return f"Slider value: {input.val()}" # 上のinput componentのidを指定して、入力値を取得してる。
```

- 補足:
  - input components は **`ui.input_*`関数**を使って作成する。
    - 第一引数 `id` はinputの名前で、入力値をreadするために使用される。
  - output components は`@render.*`decoratorで、任意の関数をdecorate(=装飾!)することで作成する。
    - render関数の中では、input componentsの入力値をreactiveにreadする事ができる。
    - **input componentsの入力値が変更されると、Shinyはたぶん自動で最小限に出力値を再renderする**。(i.e. 再計算する)

## 様々なUI components:

- Shinyには、inputs, outputs, displaying messagesなどの多くのUI componentsがある。
  - 詳細は[components gallery](https://shiny.posit.co/py/components/)を参照。

## Output components:

- outputs componentsには、dynamic plots, tablesなどinteractiveなwidgets(=component?)がある。
  - **実装に必要なのは、適当なオブジェクトを返す関数に`@render.*`decoratorを付けるだけ**...!!
  - 基本的には、`render`モジュールに色んなdecoratorが用意されてる感じ。
  - (shiny extensionsを使うと、よりカスタマイズされたoutput componentsを作成できるっぽい??)
- renderモジュールのdecoratorの例:
  - `@render.plot`decorator: matplotlib plotを表示する。
    - Figureオブジェクトを返す関数に適用できる感じ? どうやら明示的にFigureオブジェクトを返さなくても適用できるっぽい...!:thinking_face:
  - `@render.data_frame` decorator: pandas DataFrameを返す関数に適用できる。テーブルを表示する。
