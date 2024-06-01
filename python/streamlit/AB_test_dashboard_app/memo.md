streamlitとpolarsとpatitoを使って、ABテスト時に監視・評価したいmetricsを可視化するダッシュボード的なwebアプリケーションを作りたいです。
まずはディレクトリ構造から一緒に考えてください。
- 実際に運用する際には外部のDBとやりとりしますが、今回はそこを抽象化して、Repositoryクラスから擬似データを取得するようにします。
- 擬似データは以下のようなテーブル達を想定します。
  - アプリ起動ログ(user_id, timestamp, event_name)
  - user_id-ABテストのvariantのmapping (user_id, abtest_id, variant)
  - ユーザのmetadata (user_id, is_paid_user, age, sex, account_create_date)
- アプリのUIからの入力として、abtest_idを選択すると、そのABテストの結果を可視化するようにします。
  - 可視化する結果は以下:
    - 各variantのユーザ数
    - 各variantのDAU, 日次のアプリ起動率の推移

