## credential情報の設定

- `aws configure`コマンドで設定できる。
- 入力した情報は、`~/.aws/credentials`と`~/.aws/config`に保存される。

何も指定しなければ、[default]というprofile名の情報が使用される。
`--profile`オプションで指定することで、複数のcredential情報を管理できる。

## 適切なcredential情報が設定されているか否かの確認:

例えば `aws s3 ls` でS3のbucket一覧が表示されればOK。

```sh
% aws s3 ls --profile default
2023-04-16 21:37:40 cdk-hnb659fds-assets-882697291358-ap-northeast-1
2024-03-10 19:31:58 sagemaker-ap-northeast-1-882697291358

# profileオプションを指定しない場合はdefault profileが使用される。
% aws s3 ls
2023-04-16 21:37:40 cdk-hnb659fds-assets-882697291358-ap-northeast-1
2024-03-10 19:31:58 sagemaker-ap-northeast-1-882697291358

# 存在しないprofile名を指定するとエラーになる。
$ aws s3 ls --profile hogehoge
The config profile (hogehoge) could not be found
```

不要なリソースは削除しておこう。

```sh
% aws s3 rm s3://sagemaker-ap-northeast-1-882697291358/ --recursive
delete: s3://sagemaker-ap-northeast-1-882697291358/HogehogePipeline/code/28f35abb0416bf4bff18d70f48836d99/sourcedir.tar.gz
delete: s3://sagemaker-ap-northeast-1-882697291358/HogehogePipeline/code/9fe5616242e2133ec357b97e0c2eb7e9/runproc.sh

% aws s3 rb s3://sagemaker-ap-northeast-1-882697291358
remove_bucket: sagemaker-ap-northeast-1-882697291358
```

## AWS CLI S3コマンドメモ


### `aws s3 cp` と `aws s3 sync` の違い

- cpコマンド:
  - 指定したファイルやディレクトリ配下の全ファイルを、毎回全部コピーする。
- syncコマンド:
  - **ディレクトリ同士の差分同期コマンド**。
  - srcとdstのディレクトリを比較して、新規ファイル・更新されたファイルだけを探してコピーしてくれる。同じものは無視してくれるのがポイント。
