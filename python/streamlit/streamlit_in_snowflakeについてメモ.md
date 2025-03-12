## これは何?

- Streamlit in Snowflake (以下SiS)で、軽量なアプリケーションを開発するためのメモです。

## 参考文献

- その1 [Streamlit in Snowflakeの設計で意識すると良さそうなポイント](https://zenn.dev/datum_studio/articles/ba80a63100db4e)

## SiSを使ったアプリ開発の際に意識した方が良さそうなことメモ

(主に参考文献1より)

- その1: ローカルの開発環境を用意しておくこと!
  - **SiSでは、アプリの接続がアクティブな間はウェアハウスが起動した状態に保たれる。よって、開発作業中にセッションを接続したままにすると、その分だけ課金が発生し続ける**。
  - よって、開発中はローカル上でStreamlitアプリを動作させ、不要なウェアハウスの課金を避けるのがbetter!
    - (なるほど! **じゃあ基本的にSiS上でアプリのコードをいじることはないな**...!:thinking:)
    - (Sagemaker Notebookなどの話と似てそう! notebookインスタンスの起動中はお金がかかり続けるので、あんまりnotebook上で試行錯誤させづらい...!:thinking:)
  - 関連して、実装する際にはローカル環境とSiSの環境差分をできる限り減らすことを意識すべき...!! (実装のコードも、パッケージ依存関係なども)
- その2: environment.ymlとsnowflake.ymlの作成
  - SiSのアプリ設定は、environment.ymlとsnowflake.ymlファイルにより定義できる。バージョン管理できる。

```
dependencies:
- streamlit=1.35.0
- pandas
```

```
definition_version: 1
streamlit:
  name: my_streamlit_app
  stage: my_streamlit_app_stage
  query_warehouse: my_wh
  main_file: main.py
  env_file: environment.yml
  pages_dir: pages/
  additional_source_files:
  - utils.py
```

- その3. クエリ結果のキャッシュ
  - SiSでも、Streamlitのキャッシュ機能を活用してクエリ結果を再利用することができる。
    - クエリ結果をキャッシュすることで、無駄なリソース消費を防ぎ、アプリのパフォーマンスを向上できる。
    - (**ダッシュボードなどをSiSで作る時は、キャッシュ機能を使いどころが多々ありそう**...!:thinking:)
  - ちなみにStreamlitのキャッシュ機能って??
    - `@st.cache`デコレータを使うことで、任意の関数の結果をキャッシュできる。

- その4. SnowCLIからデプロイ
  - ローカル環境で開発したコードは、**SnowCLIを使ってSiSにデプロイ**できる。
    - https://docs.snowflake.com/en/developer-guide/snowflake-cli/command-reference/streamlit-commands/deploy
  - 公式ドキュメントのGithub Actionを使ったデプロイフローも参考になる.
    - https://docs.snowflake.com/en/developer-guide/streamlit/create-streamlit-snowflake-cli

### 場合によってはやった方が良いこと

- 小規模なアプリの場合はここまでやる必要はないかも。

####  その1. placeholderによるレイアウトの作成


- まず前提として、**Streamlitのレイアウトは、withを使った表記法が推奨されてる**。
  - (そうなのかs?!また後で調べてみる...!:thinking:)
  - with表記による実装がStreamlit公式の推奨です。基本的にはwithで書いた方が書き味は良い。
- ただ、状況によってはwith下のネストがかなり深くなってしまう場合がある。この場合は、**with句を使った表現ではなく、st.empty()を使ってplaceholder的に実装するのが有効かもしれない**、とのこと。
  - ちなみにここで「placeholder」とは??
    - **まず特定の位置に要素を配置し、後からその内容を動的に更新できること**。
    - (なるほど。「まず特定の位置を確保して、後でその中身を埋めていく」みたいな作り方がplaceholderって感じか...!:thinking:)
  - それこそ一定大きいアプリケーションを作る場合とか?? まあそもそもStreamlitで大きいアプリケーションを作る機会はなさそうだけど。
- また、with句でレイアウトを構成すると、**表示するデータの取得・作成ロジックと、レイアウトを決定するためのロジックが混ざってしまいがち**。
  - st.emptyを用いて、プレースホルダー要素を使ったレイアウトだけを事前定義することで、データのロジックとレイアウトをある程度分離できる。
  
例: Streamlit推奨のwith表記法の場合

```python
import streamlit as st

col1, col2, col3 = st.columns(3)

with col1:
    st.header("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg")

with col2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg")

with col3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg")
```

例: with句の代わりに、placeholder的に実装する場合

```python
import streamlit as st

# レイアウトを定義 (「特定の位置を確保」するフェーズ...!)
col1, col2, col3 = st.columns(3)

col1.header("A cat")
col1_image_placeholder = col1.empty()
col2.header("A dog")
col2_image_placeholder = col2.empty()
col2.header("An owl")
col2_image_placeholder = col3.empty()

# データの取得方法を定義 (「特定の位置に中身を埋めていく」フェーズ...!)
col1_image_placeholder.image("https://static.streamlit.io/examples/cat.jpg")
col2_image_placeholder.image("https://static.streamlit.io/examples/dog.jpg")
col3_image_placeholder.image("https://static.streamlit.io/examples/owl.jpg")
```

#### その2. モデルクラスの作成

- プレースホルダーを使ってレイアウトとロジックを分離したとしても、まだロジックが大きすぎる場合がある。
  - **「データ取得のロジック」と「表示する形にデータを編集するロジック」のそれぞれが大きいケース**である。
- なお、**StreamlitでdataclassやEnumを使用する際、公式ドキュメントでも解説されているように、セッション中で複数回クラスが定義されることで、予期しない動作を起こすことがあるらしい**。
  - 多くの場合、モデルをメインのpyファイルとは別のファイルにすることで回避できる、とのこと。

```python
raw_df = execute_query(query)

# モデルに生データを渡して加工
model = Model(raw_df)
view_df = model.filter_data()
metrics = model.get_metrics(view_df)
pivot_df = model.get_pivot_data(view_df)

# メトリクス表示
st.metric("データ件数", metrics["件数"])
st.metric("最大", metrics["最大"])
st.metric("最小", metrics["最小"])
st.metric("平均", metrics["平均"])

# グラフ表示
st.bar_chart(pivot_df)
```

### テンプレ構成

```
.
├── environment.yml
├── pages
├── snowflake.yml
└── src
    ├── main.py
    └── utils.py
```

```yml::environment.yml
dependencies:
- streamlit=1.35.0
- pandas
```

```yml::snowflake.yml
definition_version: 1
streamlit:
  name: my_streamlit_app
  stage: my_streamlit_app_stage
  query_warehouse: my_wh
  main_file: src/main.py
  env_file: environment.yml
  pages_dir: pages/
  additional_source_files:
  - src/utils.py
```
