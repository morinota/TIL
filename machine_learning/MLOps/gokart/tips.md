## refs

- [テーブルデータの推論結果をS3に出力するpipelineをgokartを使って書く / Write a pipeline using gokart to output inference results of table data to S3](https://speakerdeck.com/sansan_randd/write-a-pipeline-using-gokart-to-output-inference-results-of-table-data-to-s3?slide=18)

# tips 一覧:

- 全タスクをまとめた一つのタスク`RunTask`を用意し、`requires`にpipelineを書く。(全体像や各タスク間の依存関係がすぐにわかる)
- 精度確認用のtaskを挟む。(応答分布分析とか)
- テストが必要な関数は、static methodやclassmethodに切り出す。
- タスクのinput or output のpd.DataFrameのvalidationを行う為に`pandera`を利用する。
- pipelineが巨大になった際に、`RunTask`のrequiresを更にnestする。
