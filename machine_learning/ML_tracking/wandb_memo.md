## refs:

- https://zenn.dev/mugi_cha/articles/a12a90da9a0b4d

## チームでprojectを共有できる??

- 無料プランでも少人数だったらチームを組んでprojectを共有できるらしい。
  - 無料プランは「保存できるデータ容量」に上限あり（プロジェクトやチーム合計でGB単位の制限、いっぱいになると追加アップロード不可）
  - 小規模チーム向け。
  - 重い画像や、モデルのチェックポイントなどを保存する場合は、データサイズが大きいので有料プランを検討する必要があるらしい。
    - **ストレージ上限は5GBまでらしい。あと権限管理が「管理者/メンバー」のみ。trackingに関連する制限はこれくらい!**
    - じゃあ逆に、configやmetricsの値や軽いテーブルデータのログだけなら無料プランで十分かも??:thinking:

## Sagemaker TrainingJobなどのAWSコンテナ環境からwandbを使う場合

- refs:
  - 公式のdocs: https://docs.wandb.ai/guides/integrations/sagemaker/
- `WANDB_API_KEY`を環境変数にセットさえしておけば良いっぽい。
  - **まあ実運用では、parameter storeとかにAPI keyを保存しておいて、TrainingJobの起動後に取得するのが無難そう??**
  - 公式docsだと、`secrets.env`というファイルに保存する方法を紹介してた。

## 運用tips

- 単体テスト時などはどうする?
  - テスト実行ごとに毎回オンラインでWandBにログ上げちゃうとランが無駄に増えて大混乱してしまうので、避けたい。
  - 解決策:
    - **テスト実行時に`WANDB_MODE=disabled`が環境変数にセットされるようにしておく。**
    - もしくは、テスト用configではWandBイニシャライズ自体をスキップする条件分岐入れてもOK。


