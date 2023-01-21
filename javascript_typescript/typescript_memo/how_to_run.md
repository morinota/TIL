## 参考

- (有志の方々がまとめてくれているらしく良さそう.)[https://typescriptbook.jp/tutorials/make-a-simple-function-via-cli]

## 実行手順

まずprojectのディレクトリ(`main.ts`があるディレクトリというイメージ?)にて、以下のコマンドで`tsconfig.json`(TypeScriptファイルをJavaScriptファイルに変換する際の設定が書かれたconfigファイル)を生成する.
実行すると、project_dir内に`tsconfig.json`という設定ファイルが作成される.

```
cd project_dir/
tsc –-init
```

`main.ts`の中身を記述した後は、以下のコマンドでコンパイルを実行し、TypeScriptファイルからJavaScriptファイルに変換する. (恐らくproject_dir内の全てのtsファイルをjsファイルにコンパイルする...?)

```
cd project_dir/
tsc
```

最後に、コンパイルで生成された`main.js`ファイルを実行する.

```
node main.js
```


