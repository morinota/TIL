# code competitionのデメリット

- 提出コードを Kaggle Notebook 上にまとめる必要があり、Notebook が非常に長くなる
- オレオレライブラリやコードが手元にある場合はいちいち Notebook 上にコピペが必要になる
- notebook に移す過程でローカルで作ってたコードに微修正が必要になる

これらの対策については、次の3つの方法がありそう...

- 1. utility script を使って自分のコードをアップロード
  - utility scriptはKaggleで用意されている公式の機能。
  - 特定のスクリプトをモジュールとしてNotebookに追加する事ができる。
  - 参考
    - https://qiita.com/cfiken/items/a36b5742e9d26e0b4567#1-utility-script-%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6%E8%87%AA%E5%88%86%E3%81%AE%E3%82%B3%E3%83%BC%E3%83%89%E3%82%92%E3%82%A2%E3%83%83%E3%83%97%E3%83%AD%E3%83%BC%E3%83%89
  - めちゃ使いづらいらしい...
- 2. 自分のコードを base64 などに encode し、Notebook 上にコピペして、Notebook 上で decode する
  - 
- 3. 自分の Github リポジトリを Kaggle Datasets にまるごとあげて、Notebook から使う

# github actionsの活用

## 参考

- Git Hub Actions入門
  - https://zenn.dev/hashito/articles/7c292f966c0b59

# 参考

- https://logmi.jp/tech/articles/325898
- githubのcodeをgithub actionsの機能を使ってkaggle datasetにアップロードする
  - https://zenn.dev/hattan0523/articles/c55dfd51bb81e5
- Github 上の自分のコードを Kaggle Code Competition で使うのを CI で自動化
  - https://qiita.com/cfiken/items/a36b5742e9d26e0b4567
