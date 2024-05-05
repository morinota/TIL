## refs:

- Continuous Deliveryの公式っぽい記事[What is Continuous Delivery?](https://continuousdelivery.com/)

# 複雑性を管理する

- モジュラー性:
  - システムのcomponentsが分割、再結合されている度合い。
- 凝集度:
  - モジュール内の要素が一体的である度合い。
- 関心の分離(SoC, Separation of Concerns):
  - それぞれが別々の関心(小さな問題)を持つような各componentsからプログラムを組み立てる設計原則。
- 情報隠蔽と抽象化:
  - 要は、コードの中に境界線もしくはシームを引き、「外部」からはその詳細を考えないようにすること。
- カップリングの管理:
  - components間の相互依存の度合い
