<!-- タイトル: Text2SQLやりたい①まずLLMアプリケーションを設計する上での定石みたいなものを調べてみる -->

## これは何?

- Text2SQLサービス周りを自由研究的に調べていて、個人的に情報収集した内容を雑多にまとめたものです。
- 今回は初回として、まずLLMアプリケーションを設計する上での定石みたいなものを調べてみる。
  - Text2SQLの前に、**まずLLMを使ったアプリケーションをどう設計すると良さそうか**、みたいな設計思想の雰囲気を掴みたかった。
- 具体的には「機械学習システムデザイン」原著者であるChip Huyenさんのブログ「Building A Generative AI Platform」を読んで、内容まとめや感想をメモしています。
  - <https://huyenchip.com/2024/07/25/genai-platform.html>

### まずは最も単純なアーキテクチャから始まる

- 著者の方曰く、各社がどのように生成AIアプリケーションを導入しているかを調査した結果、そのプラットフォームには**多くの共通点**があるっぽい。
  - 記事内では、**生成AIプラットフォームの一般的なコンポーネント**、それらがどう機能するか、それらがどう実装されるか、についてまとめている。

- **まずは最も単純なアーキテクチャから始め、徐々にさらに多くのコンポーネントを追加していく**。
  - ここで、「最も単純なアーキテクチャ」とは下図のような構成を意味する。
    - 具体的には、アプリケーションがクエリを受け取り、それをモデルAPIに送信する。モデルAPIはレスポンスを生成し、それがユーザに返される。
    - ちなみにモデルAPIは、サードパーティAPI(ex. OpenAI, Google, AWS, etc.)でも、内製でホストされたAPIでもOK。

![](https://huyenchip.com/assets/pics/genai-platform/2.png)
追加コンポーネントのない最も単純なアーキテクチャの図(Huyanさんのブログより引用)

この「最も単純なアーキテクチャ」に、必要に応じてコンポーネントを追加していく。もし追加コンポーネントがなくてもシステムが上手く動作する場合は、省略すればいいよね...!:thinking: (省略可能か否かの判断は、開発プロセスの各段階で必要)。

追加され得るコンポーネント達として以下の5つが挙げられていた:

1. Context Construction: モデルが外部情報にアクセス可能にするためのコンポーネント
2. Guardrails: システムとユーザを守るためのコンポーネント
3. 複数のモデルを扱うためのRouterとGateway
4. レイテンシーとコストを削減するためのCache
5. 生成AIシステムの能力を最大限に引き出すための、complex logicやwrite actionの追加  

あと、その他として、ObservabilityとOrchestrationの話もあった。

### 追加コンポーネント1つ目: Context Construction

- システムへの最初の拡張は、**各クエリのために必要な情報を補完できるメカニズム**を導入すること。
  - このように関連情報を集めることを**Context construction(コンテキスト構築?)**と呼ぶ。
- Context constructionはどういうモチベーションで必要なの??
  - 1. まず前提: **LLMの回答の信頼性を向上させたい!!**
    - 多くの場合、**クエリ(i.e. 質問)に対して適切に回答するためには文脈(context)が必要**である。LLMの内部知識だけで対応するにはどうしても限界がある。
  - 2. LLMの内部知識の依存度を下げたい...!!
    - **LLMの内部知識は、学習データと学習方法に大きく依存し、信頼性が低い**。
      - contextが多いほど、LLMが内部知識に頼る必要が少なくなる。
      - (なるほど! 内部知識をあんまり信頼できないから、基本的にはcontextを追加したいモチベーションがあるのか...!:thinking:)
  - 3. LLMの回答が時代遅れになるのを防ぎたい...!!
    - context constructionにより、LLMは新しい情報を継続的に取り込んで意思決定を行い、時代遅れになるのを防ぐことができる。
    - ex.
      - 先週までのデータで訓練されたモデルは、**新しい情報がコンテキストに含まれていない限り、今週に関する質問に答えることができない**...!
      - 最新の情報でモデルのcontextを更新することで、モデルは最新の状態を維持し、カットオフ日を超えるクエリにも応答できるようになる:thinking_face:
    - つまり、従来のMLOpsにおける「継続的訓練(Continual Training)」に近いような役割を果たすと言っても良さそう、みたいなことが主張されてた。

![](https://huyenchip.com/assets/pics/genai-platform/5-agentic-rag.png)

Context Constructionのコンポーネントが追加されたバージョンの図(Huyanさんのブログより引用)

#### 具体的なContext Constructionの手法: RAG

- **Context construction の最も有名な手法として、RAG(Retrieval-Augmented Generation)**がある。
  - RAGは2つのコンポーネントから構成される: 
    - retriever(外部ソースから関連情報を取得する)
    - generator(ex.言語モデル)
- retrieverは、別にRAG固有のコンポーネントではないよね、という話:
  - 検索エンジン、推薦システムなど、他のアプリケーションでも結構使われてる。
    - 2-stages推薦でも、retrieveとrankの2つのステージがある!
  - **なので、従来の検索システム向けに開発された多くの検索アルゴリズムは、RAGにも適用できる!**
- retrieve対象のDocumentとchunkingの話:
  - retrieveにおける外部ソースには通常、メモ・契約書・ニュース記事などの非構造化データ(テキストデータ)が含まれる = これらを総称して **Document** と呼ぶ。
  - 各Documentのtoken数によっては、**1つのDocument全体をcontextとして渡すのが難しい場合**もある。
    - (原因は、LLM APIに渡せる最大コンテキスト長の制約や、アプリケーションのレイテンシー要件など...!)
  - なのでこの場合、**RAGでは通常、各Documentを適切なサイズのchunkに分割する**。
    - 適切なchunkサイズは、LLMの最大コンテキスト長とアプリケーションのレイテンシー要件などを考慮して決定する。
    - (なるほど...! 例えばニュース記事を一つのdocumentとみなす場合、本文全体をLLMに渡すのがアプリケーションの要件的に無理かもしれない。その場合、単一のdocumentを小さなセクションに分割(chunking)する...!!!:thinking:)
    - ちなみにchunkingと最適なchunkサイズについてより詳しく知りたい場合は、Pinecone、Langchain、Llamaindex、Greg Kamradtのチュートリアルを参照、とのこと。
- 主要な2種類のretrieveアプローチの話:
  - アプローチ1: **Term-based retrieval(単語ベースの検索)**
    - ex. 「transformer」というクエリが与えられた場合、このキーワードを含むすべての文書を関連情報としてfetchする。
    - より洗練されたアルゴリズムには、BM25（TF-IDFの活用）とElasticsearch（転置インデックスの活用）がある
    - 単語ベースの検索は、通常テキストデータに用いられるが、タイトル、タグ、キャプション、コメントなどの**テキストメタデータを持つ画像や動画にも有効**。
  - アプローチ2: **Embedding-based retrieval(埋め込みベースの検索、ベクトル検索)**
    - 各Documentのchunkを任意の埋め込みモデルを使用して埋め込みベクトルに変換しておく。(ex. BERT、sentence-transformers、OpenAIやGoogleが提供する独自の埋め込みモデル, etc.)
    - クエリが与えられると、クエリ埋め込みに最も近いデータk個が、任意のベクトル検索アルゴリズム(=ほぼほぼ何らかの近似近傍探索アルゴリズム!)によって関連情報としてfetchされる。
    - **埋め込みベースの検索は、非テキストのDocument(ex. 画像、ビデオ、オーディオ、コード)でも適用できる**。
      - 例えば、コードをDocumentとして扱う場合、多くのケースでは、**SQLテーブルやデータフレームを自然言語に要約してから、これらの要約を使用してretrieve用の埋め込みを生成**する。
      - (うんうん、実際にいくつかのText2SQLの事例でもこの方法を採用してた...!:thinking:)
      - (ちなみに、この方法を使えば、**term-based retrievalでも同様に非テキストデータを扱えるよね...??** これは別にembedding-based retrieval固有の方法ではない気がする...!:thinking:)
  - 両アプローチの比較:
    - **term-based retrievalは、embedding-based retrievalよりもはるかに高速で安価**。
      - (そうなのか...!まあDocumentの件数にもよるだろうけど、そりゃANNしなきゃってモチベーションもあるわけだ:thinking:)
      - BM25とElasticsearchは、業界で広く使用されており、より複雑な検索システムの**強力なベースライン**として機能する。
    - 埋め込みベースの検索は、計算コストが高いが、時間の経過とともに大幅に改善され、単語ベースの検索を上回ることができる。
      - (どうなんだろ、レイテンシーも重要だし...!**元々はRAGってembedding-based retrieval一択なのかなと思ってたけど、アプリケーション要件によってはterm-based retrievalの方が良いケースも結構あるのかも...!**:thinking:)
- まあ本番の検索システムは通常、いくつかのアプローチを組み合わせるハイブリッド検索だよねという話:
  - term-based retrievalとembedding-based retrievalを組み合わせる → ハイブリッド検索
  - よくあるパターン1つ目が、**sequentialパターン** (要するに2-stages推薦みたいな感じか...!:thinking:)
    - - 第一段階として、term-basedシステムなどの安価で精度の低いretrieverが候補を取得
    - 第二段階として、embedding-basedシステムなどのより正確でコストの高いretrieverが候補から最適なものを見つける
      - 第2段階はrerankingとも呼ばれる。(まさに、2-stages推薦と同じじゃん!:thinking:)
  - よくあるパターン2つ目が、**ensembleパターン**
    - 複数のretrieverを使って候補を同時に取得し、それらの異なるランキングを組み合わせて最終的なランキングを生成する。
    - (よくKaggleで目にするような、スコアを平均するようなensembleアプローチではなく、複数のランキングを混ぜ合わせるのでinterleaving的な感じか...!:thinking:)
    
- Context constructionにおいて、Documentの正確なランキングは重要かの話:
  - 検索や推薦と比較するとそれほど重要ではないかもしれないが、Documentの順序は一定重要っぽい。
  - なぜならそれが、**generatorモデルがcontextをどれだけうまく処理できるかに影響を与えるから**
  - generatorモデルは、**contextの最初と最後の文書をよりよく理解する可能性**がある。
  - しかし、対象Documentが含まれてさえいれば、その順序の影響は、検索ランキングと比較したら小さいらしい。

#### RAGのAgenticなバージョン

Context constructionを行うために、**「どの外部ソースからどのretrieve方法でcontextを取得するか」の選択を、LLM自身が行う**ようなケースの話...!:thinking:

- contextを取得する外部ソースとして、インターネットも有効、
  - GoogleやBingのAPIのようなウェブ検索ツールは、各クエリに関連する情報を収集するための豊富で最新のリソースにアクセスできる。
  - ex. 「今年のオスカーは誰が受賞しましたか？」というクエリが与えられた場合、システムは最新のオスカーに関する情報を検索し、この情報をcontextとして使用してユーザに最終的な応答を生成する

前述した2種類のretrieveアプローチ(term-based retrievalとembedding-based retrieval)、自社DBへのSQL実行、ウェブ検索は、**いずれもLLMがContext constructionを行うために取ることができるアクション**である。よってそれぞれのアクションは、モデルが呼び出せる関数とみなせる。これがいわゆるAgenticなRAG!

- (余談) AgenticなLLMシステムにどれくらいのアクション権限を与えるかの話:
  - **AgenticなLLMシステムにおいて、モデルが呼び出す関数(i.e. アクション)は、read-only actionsとwrite actionsに分類できる**。
    - read-only actions: 外部データソースから情報をretrieveするが、状態を変更しないアクション
      - (基本的にcontext constructionのための手段としてRAGを使う場合は、read-only actionsのイメージ...!!:thinking:)
    - write actions: データベースに書き込む、メールを送信するなど、状態を変更するアクション
  - LLMにwrite actionsの権限を与えると、モデルはより多くのタスクを実行できるが、より多くのリスクも伴う。

#### RAGの性能向上に関連するテクニック: Query Rewriting

- 多くの場合、より適切な情報をretrieveするために、ユーザからのクエリを書き換える必要が出てきたりする。
  - (つまり「**関連情報をより良い感じにretrieveするために、クエリをrewriteするぞー！**」という話...!:thinking:)

query rewritingが必要になるユーザクエリの例

```shell
ユーザ: ジョン・ドウが最後に何かを買ったのはいつですか？
AI： ジョンが最後にFruity Fedoraの帽子を買ったのは2週間前の2030年1月3日です。
ユーザ: エミリー・ドウはどうですか？
```

- 最後の質問「エミリー・ドウはどうですか？」は曖昧。
  - **このクエリをそのまま使って文書をretrieveすると、無関係な情報が得られる可能性が高い**。
    - (確かに、対話式のアプリケーションだと特に問題になりそう:thinking:)
- ユーザが実際に尋ねていることを反映させるために、このクエリを書き換える必要がある。
  - 書き換えられた新しいクエリは、単独で意味をなすようになってるはず...!
  - この例では、最後の質問は、「エミリー・ドウが最後に私たちから何かを買ったのはいつですか？」に書き換えるべき...!
- query rewritingは通常、他のAIモデルを使って行われる。「**次の会話が与えられたら、ユーザが実際に尋ねていることを反映させるために、最後のユーザ入力を書き換えてください**」のようなプロンプトを使用する。

- query rewritingは、場合によっては結構、複雑な処理が必要になりそうな話:
  - identity resolutionや、他の知識を組み込む必要がある時など。
    - ざっくり「identity resolution」って??
      - 特定の「人物・物・場所」などを一意に特定するプロセス。
      - 要するに名前解決みたいな感じか...!:thinking:
  - ex.
    - 会話内の言及: 「彼の妻についてもっと知りたい」というクエリが与えられた場合、モデルは「彼」が誰を指しているのかを特定した後で、DBにクエリを送信して「彼」の妻について調べる必要がある。
    - この情報がない場合、**query rewriting用モデルは、名前をhallucinateする代わりに、このクエリが解決できないことを認めて、誤った回答につながるのを防ぐべき**。

(query rewriting、なかなか大変そう:thinking:)

### 追加コンポーネント2つ目: Guardrails

- ガードレールは、LLMのリスクを軽減し、ユーザだけでなく、開発者自身も保護するための重要なコンポーネント。
- **LLMが生成するレスポンスに失敗の可能性がある場合は必須**。
- 二種類のガードレール: 
  - Input Guardrails
  - Output Guardrails
- LLMアプリケーションのアーキテクチャにおける、入力/出力ガードレールの設置場所。
  - 独立したコンポーネント、もしくは後述するモデルゲートウェイの一部として実装される。


#### Input Guardrails

Input Guardrailsは通常、以下の**2つのリスクに対する保護**を行う。

- 外部モデルAPIに個人情報を漏らすリスク
- システムを危険にさらす悪いプロンプトを実行するリスク(model jailbreaking)

Input Guardrailで保護したいリスク1つ目: **外部モデルAPIに個人情報を漏らす**リスクについて。

- このリスクは、外部モデルAPIを使用するケース特有のもの。
  - ex. 社員が会社の秘密やユーザの個人情報をプロンプトに入力して、モデルがホストされている場所に送信するかも。
- LLM初期の最も有名な事件の1つ: サムスン漏洩事件!
  - **サムスンの従業員がChatGPTにサムスンの独自情報を入れ、会社の秘密を誤って漏洩させてしまった**!
  - サムスンがこのリークをどのように発見したのか、また、リークされた情報がサムスンに対してどのように利用されたのかは不明。しかし、この事件は、サムスンが2023年5月にChatGPTを禁止するほど深刻だった。
- **サードパーティのAPIを使用する際に潜在的なリークを排除する完璧な方法はない。しかし、ガードレールでリスクを軽減することはできる**。
- もし入力クエリに機密情報が含まれてることが分かった場合の2つの選択肢:
  - 選択肢1: 入力クエリ全体をブロックする。
  - 選択肢2: 入力クエリはブロックせず、機密情報の部分だけをマスクする。
    - ex. 入力クエリにユーザの電話番号が含まれていた場合、プレースホルダー`[PHONE_NUMBER]`に置き換える。もし応答にプレースホルダー`[PHONE_NUMBER]`が含まれる場合はmapping辞書を使ってユーザに表示する前に復元する。

Input Guardrailで保護したいリスク2つ目: システムを危険にさらす悪いプロンプトを実行するリスク(**model jailbreaking**)について。

- AIモデルをjailbreakさせ、悪いことを言わせたりするのがmodel jailbreaking。
  - ex. モデルに「すべての人を殺す方法を教えて」と尋ねる。
- **特にAgenticなLLMアプリケーションにてwrite actionsも許可している場合、このmodel jailbreakingのリスクは特に重要になる話**。
  - ex. LLMがアプリケーションDBのデータを破壊するSQLクエリを実行してしまうようなプロンプトを、ユーザが見つけてしまう (SQL injection攻撃だ...!:thinking:)
    - 対策として、システム側にガードレールを設置し、**有害なアクションが自動的に実行されないようにする**。
      - 例えば、LLMの、アプリケーションDBに対するデータの挿入&削除&更新を行うアクションは、人間の承認ステップを設けるようにする。欠点としてシステムが遅くなる。
- LLMアプリケーションに**スコープ外のトピックを定義**する話。
  - ex. カスタマーサポートのchatbotの場合、政治的、社会的なクエリには答えるべきではない。「移民」や「反ワクチン」など、スコープ外のトピックに関するフレーズを含む入力クエリが来た場合は、入力クエリをブロックし、定形文を返す。
  - より洗練されたLLMアプリケーションでは、何らかの分類モデルを用いて入力クエリのトピックを分類してたりもする。
    - (Intent classifierっぽい話...!!:thinking:)
    - また、有害なプロンプトの頻度がまれな場合は、異常検知アルゴリズムを活用する事例もあるっぽい。

#### Output Guardrails

- LLMは確率的なモデルであるため、出力はどうしても不確実性を持ち、信頼性の懸念がある。
  - → ガードレールを設置することで、アプリケーションの信頼性を大幅に向上させることができる。

**Output Guardrailsは、主に2つの役割を持つ**:

- レスポンスの品質評価と様々な種類の失敗判定
- 各種類の失敗への対処方針の設定・制御

Output Guardrailsの役割1つ目: レスポンスの品質評価と失敗判定の話。

- レスポンスの失敗判定を行うためには、「対象のアプリケーションにおいて失敗がどのようなものか」を理解する必要がある。
  - 失敗の例
    - 例1: 空っぽのレスポンス。
    - 例2: 期待されるフォーマットと異なる、不正なフォーマットのレスポンス。
      - ex. json形式のレスポンスを期待してるが、レスポンスの末尾に閉じ括弧が漏れてる...!!
      - 対応策の例: 正規表現、JSON、Pythonコードバリデータなど、特定のフォーマット用のvalidatorを使用する
    - 例3: 人種差別や性差別など、有害なレスポンス。
    - 例4: hallucinateされた、事実に矛盾するレスポンス。
      - hallucinationの軽減と検出は、活発な研究分野。
      - 軽減策の例: RAGなどのContext constructionを使用
      - 検出策の例: Search Engine Factuality Evaluator, SelfCheckGPT, etc.
    - 例5: 機密情報を含むレスポンス。
      - 対応策の例: 機密データでモデルをトレーニングしないこと。最初からcontextとして機密データをretrieveすることを許可しないこと。
    - 例6: 自社や競合他社を誤って表現するなど、ブランドリスクのあるレスポンス(例4と近いかも)
      - 対応策の例: キーワード監視。
        - もし自社ブランドや競合他社に関するレスポンスを特定したら、これらの出力をブロックしたり、人間のレビュアーに渡したり、他のモデルを使用してこれらの出力の感情を検出して、正しい感情のみが返されるようにする(なるほど...!:thinking:)
    - 例7: 品質が低いレスポンス。
      - ex. 
        - Text2SQLの場合は、質問に適切に答えられないSQLを生成してしまう。
        - モデルに低カロリーのケーキのレシピを頼んだら、出来上がったレシピに砂糖が過剰に含まれていた。
      - 対応策の例: モデルの回答の質を評価するために、AI Judgeを使用する
        - これは現在、かなり一般的になってるとのこと。**いわゆるLLM-as-a-Judgeってやつか**...!:thinking:
        - 判定に使用するモデルは、汎用モデル（ChatGPT、Claudeなど）、もしくは、具体的なスコアを出力する学習済みモデル。(まあ前者の方が、開発も運用もコストが低く済みそう...!!:thinking:)

Output Guardrailsの役割2つ目: 各種類の失敗への対処方針の設定・制御、の話。

- (最もシンプルな対処法!)**リトライポリシー**の話。
  - 失敗判定時の対応として、多くの失敗は、基本的なリトライロジックを使用して軽減できる。
    - というのもLLMは確率的なもの。なのでもう一度クエリを試せば、違う回答が返ってくるかもしれない。
    - レスポンスが空だった場合は、空でないレスポンスが返ってくるまでX回再試行する。
    - レスポンスが不正なフォーマットだった場合、モデルが期待通りのフォーマットのレスポンスを生成するまでX回再試行する。
  - デメリット: **余分なレイテンシーとコストを発生**。
    - 失敗判定された後にリトライすると、単純にユーザが経験する待ち時間は2倍になる。
    - なので、**待ち時間を減らすために、並列に呼び出すのは有効なアイデア**(なるほど...!:thinking:)
      - ex. それぞれの入力クエリに対して、最初のクエリが失敗するのを待ってからリトライするのではなく、入力クエリをモデルに同時に2回送信して2つのレスポンスを返してもらい、より良い方を選ぶ。
      - この場合、冗長なAPI呼び出しの数は増えるが、レイテンシーは管理可能な範囲に抑えられる...!
- 失敗判定時に**人間に頼るポリシー**の話。
  - トリッキーな入力クエリを処理するために人間に頼ることもよくあること。
    - ex. カスタマーセンターのchatbotにて。入力クエリに特定のキーワードが含まれている場合、人間のオペレーターに転送する。
  - 事例によっては、専門的なモデルを使って、入力クエリを人間に転送するべきタイミングを判定させてたりするケースもあるみたい。
    - ex. 感情分類モデルがユーザが怒っていると検出したときに、chatbotが会話を人間のオペレーターに転送する。
  - (これらの例は、どっちかっていうとInput Guardrails側の話っぽい...??失敗判定時の対処というよりは、失敗を軽減するための操作な感じがする...!:thinking:)

#### ガードレールのトレードオフの話

- **信頼性とレイテンシーのトレードオフ**
  - ガードレール（安全性・信頼性確保の仕組み）の重要性を認識しつつも、レイテンシー（応答速度）を重視するチームもある。
    - 事例によっては、**レイテンシー増加の懸念からガードレールを実装しないことを選択してるケース**もある。
    - ただまあ多くの事例では、「レイテンシーの増加よりもリスクの増大がコスト高」と考えて、ガードレールを取り入れてるらしい。
- 信頼性vsレイテンシーに関連して、Stream Completionモードと出力ガードレールの話。
  - まずStream Completionモードって?
    - **通常は全体のレスポンスを生成し終わってからユーザに表示するが、Stream Completionモードではトークンが生成されると同時にユーザにストリーミングされる。ユーザの待ち時間が短く済む、というメリットがある。**
  - どうしても部分的なレスポンスの評価が難しいので、不適切な応答が出力ガードレールで失敗判定してブロックされる前に、ユーザに表示される可能性がある。


#### Input/Output Guardrailsの設置場所

生成AIプラットフォームのアーキテクチャ内で、ガードレールは、独立したコンポーネント、もしくは後述するモデルゲートウェイの一部として実装される。

![](https://huyenchip.com/assets/pics/genai-platform/8-guardrails.png)

2つ目の追加コンポーネントとして、入力/出力ガードレールが追加されたアーキテクチャの図(Huyenさんのブログより引用)

### 追加コンポーネント3つ目: RouterとGateway

- アプリケーションが複雑化し、より多くのモデルを扱うようになると、**複数のモデルを扱うのに役立つ2種類のツール**が利用されるようになった。
  - Router
  - Gateway

#### Routerの話

- LLMアプリケーションは、異なる種類の入力クエリに対応するために、複数のモデルを使用することがよくある。
  - (まあ必ずしも1種類のモデルで全てのクエリに対応する必要もないもんな...!:thinking:)
- **異なる種類の入力クエリに対して異なるソリューションを持つことには、いくつかの利点がある**
  - 第一に、特化型のモデルを使用できる。
    - 特化型のモデルは、汎用モデルよりも性能が向上し得る。
    - (まあ特化型モデルを内製するとしたら、開発・運用コストが追加でかかるというデメリットもあると思うけど...!:thinking:)
  - 第二に、コスト削減に役立つ
    - すべての入力クエリを高価なモデルにルーティングする代わりに、より安価なモデルに簡単な入力クエリをルーティングすることができる
      - (なるほど。例えば、入力クエリが難しそうだと判断されたらGPT-o1を使い、簡単そうだと判断されたら安いGPT-4o-miniを使う、みたいな感じか...!:thinking:)
- **ルーターは通常、ユーザが何をしようとしているかを予測するintent classifier(意図分類器)で構成される**。
  - 予測された意図に基づいて、入力クエリは適切なソリューション(i.e. モデル)にルーティングされる。
    - ex. カスタマーサポートのchatbotの場合
      - 入力クエリが「パスワードをリセットしたい」だったら、ユーザをパスワードリセットのページに誘導する。
      - 入力クエリが「請求ミスを訂正したい」だったら、ユーザを人間のオペレーターにルーティングする。
      - 入力クエリが「技術的な問題のトラブルシューティングをしたい」だったら、トラブルシューティング用に細かく調整されたモデルにルーティングする。
  - また、**intent classifierはシステムがスコープ外の会話を避けるのにも役立つ**。(そうそう! 入力ガードレールっぽいなって思った...!!:thinking:)
    - 入力クエリがアプリケーションのスコープ外と判断された場合、chatbotはAPIコールを無駄にすることなく、予め用意された定型文の1つを使って丁寧に拒否することができる(ex. 「申し訳ありませんが、その情報は提供できません。プロダクトに関する質問があればお知らせください」)
- システムが複数のアクションにアクセスできる場合、**ルーターはnext action predictorを含めることができ**、システムが次にどのアクションを取るかを決定するのに役立つ。
  - (Agenticな感じだ...! まあmodel routing自体がアクションを選択してる訳だし、ルーターを導入した時点でAgenticなLLMアプリケーションって感じなのかな...!:thinking:)
  - **入力クエリがあいまいな場合は、説明を求めることも有効なアクションの1つ** (なるほど確かに...!:thinking:)
    - ex. ユーザクエリ「freeeze!」を受け取った場合、システムは「アカウントを凍結したいのですか?それとも天気について話しているのですか?」や「申し訳ありません。詳しく説明していただけますか？」と尋ねることができる。
- Intent classifierやNext action predictorの実装は、汎用モデル or 特化された分類モデルが利用され得る。
  - **特化した分類モデルは、通常、汎用モデルよりもはるかに小さく高速であり**、システムが多数のモデルを使用しても、大幅な追加のレイテンシーやコストをかけることなく使用できる、という利点がある。
  - (まあ少なくともレイテンシーの要件が緩いアプリケーションの場合は、開発・運用コストを考慮すると、基本的には外部APIの汎用モデルを使用する感じなのかな...!:thinking:)

#### Gatewayの話

- モデルゲートウェイは、**開発組織が、異なるモデルに対して統一された安全な方法でインターフェースを持つことを可能にする中間層**。
- モデルゲートウェイの最も基本的な役割 = 「**開発者が異なるモデルに同じ方法でアクセスできるようにすること**」(大事だ...!:thinking:)
  - コードの保守が容易になる。
    - モデルAPIが変更された場合、そのモデルAPIを使用するすべてのアプリケーションを更新する必要がある代わりに、モデルゲートウェイだけを更新すればよい!
  - なので、モデルゲートウェイの最もシンプルな例では、統一されたwrapper関数を提供するだけ。
- モデルゲートウェイの他の役割たち:
  - 役割1: アクセス制御とコスト管理。
    - OpenAI APIにアクセスしたい人全員に自社組織のトークンを渡すのではなく、**モデルゲートウェイにアクセス権を与えることで、中央集権化された制御されたアクセスポイント**を作成する
    - また、どのユーザやアプリケーションがどのモデルにアクセスできるかを指定する**細かいアクセス制御**を実装することができる
    - 加えて、API呼び出しの使用状況を監視し、制限することで、乱用を防ぎ、コストを効果的に管理することができる。
    - (うんうん、**モデル利用状況の管理の観点から、モデルサービスとの窓口は1箇所 = 中央集権化されている方が都合がいい**んだよね...気持ちわかるぜ...!:thinking:)
  - 役割2: フォールバック戦略の実装の場所。
    - モデルゲートウェイは、レート制限や外部APIの失敗を克服するためのフォールバックポリシーの実装場所として利用できる。
      - (あ、推論モデルに不具合があった場合になんとか対応するためのフォールバック戦略か...!:thinking:)
    - メインのLLMが利用できない場合、リクエストを代替モデルにルーティングしたり、短い待ち時間を経て再試行したり、他の様々な戦略で失敗対応できる
      - -> **アプリケーションが中断することなくスムーズに動作することが保証**できる(アプリケーションの要件にもよるが、大事だ...!:thinking:)
  - 役割3: ルーティング、ロードバランシング、ロギング、キャッシュなどの**他の様々な機能を実装するのに適した場所**。
    - なので、前述の入力/出力ガードレールをモデルゲートウェイの中に実装するのもあり。

![](https://huyenchip.com/assets/pics/genai-platform/10-model-gateway.png)

3つ目の追加コンポーネントとして、モデルゲートウェイ(Router含む)が追加されたアーキテクチャの図(Huyenさんのブログより引用)

### 追加コンポーネント4つ目: Cache

LLMアプリケーションにおけるキャッシュ(Cache)は、レイテンシーを削減し、コストを抑えるための重要な要素である。
LLMの代表的な推論キャッシュ技術として、以下の3つがある:

- 1つ目: Prompt Cache(プロンプトキャッシュ)
- 2つ目: Exact Cache(厳密なキャッシュ)
- 3つ目: Semantic Cache(意味的なキャッシュ)

Prompt Cacheについて。

- 何をキャッシュする?
  - プロンプト（入力クエリ）の一部をキャッシュして、再利用することで処理時間を短縮する。
  - ex. すべての入力クエリで同じシステムプロンプトを使う場合、毎回処理するのではなく、一度キャッシュして使い回すことができるはず。
    - システムプロンプト = 様々なプロンプトで重複する共通のテキストセグメント。
- **長いシステムプロンプトを伴うアプリケーションの場合、プロンプトキャッシュは、レイテンシーとコストの両方を大幅に削減できる。**
  - 仮に、システム・プロンプトが1000トークンで、LLMアプリケーションが今日100万回のLLM APIの呼び出しを行う場合、プロンプトキャッシュを使えば、1日に約10億回の繰り返し入力トークンの処理を省くことができる。
- しかし（当然!）プロンプトキャッシュは無料ではない。KV(key-value)キャッシュと同様にエンジニアリングの努力が必要。
- Gim et alによって2023年11月に導入されて以来、Prompt Cacheはすでにいくつかの外部モデルAPIに組み込まれてる。
  - 例えばGemini APIは、2024年6月にcontext cacheという名称でPrompt Cache機能を提供。
    - キャッシュされた入力トークンは、通常の入力トークンに比べて75％割引されるが、キャッシュストレージのために追加料金を支払う必要がある。

Exact Cacheについて。

- プロンプトキャッシュに比べて、Exact cacheはより一般的で直接的。
  - **システムは処理されたアイテムを保存し、同一のアイテムが要求されたときに後で再利用する**。
  - ex. **あるユーザが商品の要約をモデルに求めた場合、システムはキャッシュをチェックし、この商品の要約がキャッシュされているかどうかを確認する**。キャッシュされてたらそのまま返す。キャッシュされてなかったらモデルにリクエストを投げて生成結果をキャッシュする。
    - ユースケースによっては導入しやすそう...!:thinking:
- **またExact Cacheは、RAGにおける埋め込みベースの検索でも使用され得る**。
  - 冗長なベクトル検索を避けるため。
  - 入力クエリがすでにベクトル検索キャッシュに存在する場合、キャッシュされた結果を取得する。
  - **Exact Cacheは、複数のステップ(ex. chain-of-thought)や処理時間のかかるアクション（検索、SQL実行、ウェブ検索など）を必要とするLLMアプリケーションには特に有効になり得る**。
- 実装方法について。
  - 高速な検索のためにインメモリ・ストレージを使用して実装され得る。
    - もしくはインメモリは容量制限もあるので、PostgreSQLやRedisなどのDB、あるいは速度とストレージ容量のバランスを取るための階層型ストレージを使用して実装するケースもある。
  - 実装時には、**Eviction policy(立ち退きポリシー?)**が重要。
    - キャッシュがいっぱいになった場合、どのアイテムを削除するかを決定するために使用される。
    - 一般的なEviction policyには、Least Recently Used (LRU)、Least Frequently Used (LFU)、First In, First Out (FIFO)などがある。(ほげ〜...!:thinking:)
  - クエリのキャッシュ期間は、そのクエリが再度呼び出される可能性がどの程度あるかによって決まる。
    - 例えば、「私が最近買った商品は?」などの**ユーザ固有のクエリは、他のユーザに再利用される可能性が低い。よってキャッシュすべきでない**。
    - また、「今の天気はどうですか?」のような**時間に敏感なクエリも、キャッシュすべきでない**。
    - 一部の事例では、**「入力クエリをキャッシュすべきか否か」を判定する分類器を学習して採用してるケース**もあるらしい...!

Semantic Cacheについて。

- Semantic Cacheは**類似したクエリの再利用**を目的としたもの。
  - 例えばあるユーザが「ベトナムの首都は？」と尋ね、「ハノイ」という回答を生成。
  - その後、別のユーザが「ベトナムの首都はどこですか？」と尋ねる (「どこ」という余分な単語が追加された)。
  - **システムが新しい入力クエリをゼロから計算する代わりに、「ハノイ」という答えを再利用できること = これがSemantic Cacheのアイデア!**
- セマンティックキャッシュは、**2つのクエリが意味的に類似しているかどうかを信頼性高く判断できる方法**を持ってる場合にのみ機能する。
  - 一般的なアプローチは、埋め込みベースの類似性を使った方法(ex. コサイン類似が閾値以上であれば、意味的に同じだと判定する)
- **上述した2つのキャッシュ技術と比べて、Semantic Cacheは、その多くのコンポーネントが故障しやすいため、より疑わしい**。(なるほど、不確実性が高いというか...!:thinking:)
  - うまく機能するには、高品質な埋め込み、ベクトル検索アルゴリズム、信頼できる類似性metricsが必要。
    - (信頼できる類似性metricsって、要するに、**どんなmetricsがどれくらいの値以上だったら類似してると判定するか、の設定が難しすぎるよなぁ**...!:thinking:)
- Semantic Cacheを採用する意思決定をする際は、計算効率、開発・運用コスト、パフォーマンスリスク(ex. 逆にレイテンシー悪化)をしっかり考慮しよう...!

キャッシュコンポーネントは、LLMアプリケーションのアーキテクチャのどこに追加される?

![](https://huyenchip.com/assets/pics/genai-platform/12-cache.png)

4つ目の追加コンポーネントとして、キャッシュが追加されたアーキテクチャの図(Huyenさんのブログより引用)

- プロンプトキャッシュは通常、外部モデルAPIの内部に実装されたりする(なので図には現れない)
- 生成されたレスポンスをキャッシュに追加する新しい矢印が追加された。
  - (ちなみに、Context constructionの部分にもcacheのコンポーネントがあるのは、Exact CacheがRAGの埋め込みベースの検索にも使用され得るって話...!:thinking:)

### 追加コンポーネント5つ目: Complex LogicやWrite Action

- 前述までのコンポーネントたちが追加されたLLMアプリケーションは、かなりシンプルなフローを持つ。
  - LLMが生成した出力は、(出力ガードレールに引っかからない限り)ユーザに返されるだけ。
- **しかし実際のアプリケーションのフローは、より複雑になり得る** (ループや条件分岐、生成結果を元に何らかのアクション実行...!)

#### Complex Logicの話

- モデルの出力を特定の条件を満たしたら別のモデルに渡したり、次のステップへの入力の一部として同じモデルにフィードバックしたり。これは、システム内のモデルが最終的なレスポンスをユーザに返すべきであると判断するまで続く。
  - (要するにLLM-as-a-Judgeっぽいイメージ...!:thinking:)
- これは、**システムに次の行動を計画し決定する能力を与えたとき**に起こりうる。
  - (i.e. アプリケーションのAgentic度合いを高めたとき...!:thinking:)
  - 例: 「パリの週末の旅行日程を計画して！」という入力クエリ
    - まずモデルは、アクティビティのリストを生成する(ex. エッフェル塔へ行く、セーヌ川のクルーズをする、美術館を訪れるなど)。
    - 各アクティビティのそれぞれをモデルに再入力して、より詳細な計画を生成する。(ex. 「エッフェル塔へ行く」について、「営業時間の確認」、「チケットの購入」、「アクセス方法の検索」「近くのレストランの検索」などのサブタスクを生成)
    - この反復プロセスは、包括的で詳細な旅程が作成された、と判断されるまで続けられる。


LLMアプリケーションのアーキテクチャ図で言うと、**モデルに生成されたレスポンスをContext Constructionに戻す矢印が追加されるイメージ**。

![](https://huyenchip.com/assets/pics/genai-platform/13-loop.png)

5つ目の追加コンポーネント(の1つ目)として、Complex Logicが追加されたアーキテクチャの図(Huyenさんのブログより引用)

#### Write Actionの話

- Context constructionに使用されるアクションはread-onlyアクションである。
  - (うんうん、外部ソースの状態を変更するようなwriteアクションはないよね:thinking:)
  - しかし場合によっては、システムはwriteアクションを行い外部ソースや世界の状態を変更することもできる。
    - ex. モデルが 「XさんにメッセージYのEメールを送信する」と出力(i.e. 判断...!:thinking:)した場合、システムは `send_email(recipient=X, message=Y)`アクションを呼び出す。
      - (ん〜Agentic! Agenticですねぇ〜:thinking:)

![](https://huyenchip.com/assets/pics/genai-platform/14-write-actions.png)

5つ目の追加コンポーネント(の2つ目)として、Write Actionsが追加されたアーキテクチャの図(Huyenさんのブログより引用)

- **writeアクションを許可することは、LLMアプリケーションをはるかに強力にする**。
  - ex. 潜在的な顧客の調査、連絡先の検索、メールの起案、最初のメールの送信、返信の読み取り、フォローアップ、注文の抽出、新しい注文でデータベースを更新するなど、**顧客アウトリーチのワークフロー全体を自動化できたりする。
- しかし当然リスクもある。
  - **インターンに本番データベースを削除する権限を与えてはいけないように、信頼性のないAIに銀行振込を開始させてはいけない**。
  - model jailbreakやprompt injection対策を行い、有害なアクションを実行させようとする悪質なユーザからシステムを守る必要がある。
  - **多くの企業が恐れているシナリオは、AIシステムに社内データベースへのアクセス権を与え、攻撃者がこのシステムを騙してデータベースから個人情報を漏えいさせること**。
- AIを活用しようとする組織は、安全性とセキュリティに真剣に取り組む必要がある。
  - しかし、こうしたリスクがあるからといって、AIシステムに現実世界で行動する能力を与えてはいけないというわけではない。
  - なぜなら、**AIシステムは失敗する可能性があるが、人間も失敗する可能性がある。**
