## refs:

- [Amazon EventBridge の料金](https://aws.amazon.com/jp/eventbridge/pricing/)
- [Amazon SageMaker Pipeline の実行をトリガーする新しいオプション](https://aws.amazon.com/jp/about-aws/whats-new/2021/04/new-options-trigger-amazon-sagemaker-pipeline-executions/)

# EventBridge ruleの作り方

指定すべき条件は以下:

- rule名
- ruleのdescription
- rule type(大きく2種類の選択肢がある):
  - 1. **Event pattern**の場合:
    - ruleは、パターンに一致するイベントが発生した場合にが開始される。
    - Event patternの詳細は[Event Patterns in CloudWatch Events](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/CloudWatchEventsandEventPatterns.html).
  - 2. **Schedule**の場合:
    - ruleは、指定されたスケジュールで定期的に開始される。
    - 分、時間、または日単位で、定期時間ごとの実行を指定できる。(ex. 5分に1回、5日に一回)
    - またcron expressionを使用すると、より細かいスケジュールも指定できる。ex. “the first Monday of each month at 8am.”
- event busを選択する
  - (基本的にdefaultで良さそう?よくわかってない)
- ruleのターゲットを指定する:
  - rule 1つ当たり、5つのgargetを指定できる。
  - ex. Sagemaker Pipelineを選び、具体的なpipelineを選択する。
    - key-valueペアを使用して、pipeline実行時に渡すパラメータを指定できる。(パラメータはstaticまたはdynamic)
- EventBridge ruleが持つroleを指定する。(既存のrole or 新しく専用のroleを作る)
- (Optional) tagを追加する。(コストモニタリングとかで使用するやつ...??:thinking:)

# 料金:

- スケジューラー: 月間 14,000,000 回の呼び出しが無料。それ以降は100万回あたり 1.00 USD。
- 5分に1回呼び出すスケジュール実行だったとしても、月間約9000回。バッチMLシステムの運用においては、無料枠内で収まることが多いかもしれない。(pipelineを一度走らせる場合、たぶん呼び出し回数って1回だよね...?:thinking:)
