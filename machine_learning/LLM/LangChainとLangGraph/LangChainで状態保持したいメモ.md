## これは何?

- LangChainで状態保持したいメモを書いていく。

## 参考文献

- わかりやすかったブログ: [langchain version0.3におけるメモリ機能の備忘録](https://qiita.com/ayoyo/items/276b4a6dc49037782b92)
- LangChain公式のv0.2からv0.3のメモリ移行についてまとめたページ: [How to migrate to LangGraph memory](https://python.langchain.com/docs/versions/migrating_memory/)
- Streamlitでチャット履歴を実装するならこれを参考にできそう
  - [RAG機能付きチャットボットを作ろう-5_チャット表示のMarkdown化](https://zenn.dev/bluetang/articles/chatbot_with_lc_st_chromadb_05)
  - Streamlitのアップデートでchat UIが追加されて、実装が簡単になったらしい...!実装時はこれか公式docを参照したら良さそう![Streamlitを使ってチャットアプリを簡単に作る](https://zenn.dev/nishijima13/articles/7ed472f51240b5)

## LangChainの状態保持について

- ざっくり、LangChainのv0.2からv0.3へのアップデートで、推奨される状態保持の方法が変わったらしい。
  - v0.2では、`langchain.memory`の8種類のメモリ関連のクラス&関数を使うのが推奨されてた。
  - v0.3では、LangGraphのメモリ機能が優秀なので全てそっちを使う形が推奨になった。
    - なぜ? LangGraphによる永続化の利点は以下。
      - ①複数ユーザ・複数会話のbuild-inサポート。
      - ②複雑な会話を保存し、いつでも再開できること。
        - これは以下の点で嬉しい。
          - エラーの回復。
          - AIワークフローへの人間の介入。
          - 異なる会話パスの探索(タイムトラベル機能)
      - ③従来の言語モデルと最新のチャットモデルの両方との完全な互換性。
      - ④高度なカスタマイズ性。
        - どのようにメモリが動作するかを完全にコントロールし、**異なるストレージバックエンドを選択できる**。
        - Redisに保存したり、RDBに保存したり、インメモリに保存したり、ファイルに保存したり、など。

  - **ただしv0.2で推奨されてたメモリ関連のクラス達は、当面廃止されないのでそのまま使っても大丈夫!**

### langchain.memoryの8種類のメモリ機能クラスについて。

v0.2で推奨されていた8つのメモリ機能クラスについて。

#### 最もシンプルなCoversionBufferMemoryクラス

- CoversionBufferMemoryクラス: 最もシンプルなメモリ機能クラス。
  - 会話の履歴を保持する。
  - 会話の履歴を全て保持するため、会話が長くなるとプロンプトが膨大になる。

#### 直近k個の会話や直近n個のトークンのみを保持するクラス

- ConversationBufferWindowMemoryクラス: 直近k個の会話を保持する。
- ConversationTokenBufferMemoryクラス: 直近n個のトークンを保持する。

#### 過去の会話を要約して保持するクラス

- ConversationSummaryMemoryクラス: 過去の会話を要約して保持する。
- ConversationSummaryBufferMemory: 過去の会話の要約と、直近の会話(トークン数で指定)を保持する。

#### 長期記憶用のメモリクラス

- ConversationEntityMemoryクラス: Entity(=固有名詞?)に関してのみメモリを保持する。
- ConversationKGMemoryクラス: ナレッジグラフを作って会話についての情報を保持する。
- ConversationVectorStoreTokenBufferMemoryクラス: 過去会話をベクターストアに保持し、関連する会話のみ探索して用いる。

