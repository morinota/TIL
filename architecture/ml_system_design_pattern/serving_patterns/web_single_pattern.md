## link
- https://mercari.github.io/ml-system-design-pattern/Serving-patterns/Web-single-pattern/design_ja.html


# Web Single Pattern 

## Usercase

- もっともシンプルな構成で推論器を素早くリリースしたいとき

## Architecture

- Webシングル・パターンはWebサーバにモデルを同梱させるパターン.
- 同一サーバにRESTインターフェイス（もしくはGRPC）と前処理、学習済みモデルをインストールすることによって、シンプルな機械学習推論器をつくることができる.
- 複数台のWebサーバで運用する場合はロードバランサーを導入して負荷分散することができる. 
- ただしインターフェイスをGRPCで実装する場合、クライアントロードバランサーを用意するか、L7ロードバランサーを使用する必要がある.
- Webシングル・パターンへのモデルの含め方はモデル・イン・イメージ・パターン、モデル・ロード・パターンのいずれも実現可能.
