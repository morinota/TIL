## refs

- https://www.wantedly.com/companies/wantedly/post_articles/302887
- https://slack.dev/bolt-python/ja-jp/tutorial/getting-started

# Slack API 概要

## 通信の種類

大きく３種類の通信方法がある:

- slack-app(=自作のサービス側) から Slack API にリクエストを送って Slack ワークスペースを操作したり情報を取得する **Web API**
  - アプリ -> Slack APIへの通信
- Slack ワークスペース上でのイベントを slack-app(=自作のサービス側) に送ってくれる **Events API**
  - Slack API ->アプリ への通信
- Interactive Component の操作を送ってくれる **Interactivity**
  - Slack API ->アプリ への通信

### blocksとInteractive Component

- slackのUI Componentsは、**blocks**と呼ばれる。
  - 参考: https://www.slideshare.net/NavitimeJapan/slackuxblock-kit を読むとお気持ちがわかるらしい。
- blocksの実態はjsonのメッセージ。
- blocksは様々なcomponentsによって構成される。
- Interactive Componentは特別なcomponent
