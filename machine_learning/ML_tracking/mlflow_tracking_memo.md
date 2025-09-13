# mlflow tracking雑多メモ

## refs:

## リモートにMLFlow Tracking Serverを立てる以外の選択肢

- 実はTracking Serverを立てない選択肢も結構メジャーらしい。
- 直でDB (SQLiteなど) に書き込んで、UIをローカルで`mlflow ui`で立ち上げる方法。
- ローカルUI × S3に保存、という組み合わせも結構ありえるっぽい??
