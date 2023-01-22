# import、export、require

実務でアプリケーションを作る場合、複数のJavaScriptファイルを組み合わせて、ひとつのアプリケーションを成すことが多い.
いわゆるモジュール指向の開発.
ここではJavaScriptとTypeScriptでのモジュールと、モジュール同士を組み合わせるためのimport、export、requireについて.

## スクリプトとモジュール

## 値の公開と非公開

## モジュールは常にstrict mode

## モジュールはimport時に一度だけ評価される

## モジュールの歴史的経緯

## CommonJS

### requnre()

Node.jsでは現在でも主流の他の.jsファイル(TypeScriptでは.tsも)を読み込む機能. 基本は次の構文.

```javascript
const package1 = require("package1");
```

## ES Module

## Node.jsでES Moduleを使う

# TypeScriptでは

TypeScriptでは一般的に**ES Module**方式(**import文を使う方式**)に則った記法で書く.
これは**CommonJS**方式(**require()を使う方式**)を使用しないというわけではなく、コンパイル時の設定でCommonJS, ES Moduleのどちらにも対応した形式で出力できるのであまり問題はない.

## require? import?

TypeScript -> JavaScriptへのコンパイル時にどの方式に変換するかの指定.

## default export? named export?

`module.exports`と`export default`はdefault exportと呼ばれ、`exports`と`export`はnamed exportと呼ばれる.
どちらも長所と短所があり、たびたび議論になる話題.
どちらか一方を使うように統一するコーディングガイドを持っている企業もあるようだが、好みの範疇.

### default export

- Pros:
  - importする時に名前を変えることができる
  - そのファイルが他のexportに比べ何をもっとも提供したいのかがわかる
- Cons:
  - エディター、IDEによっては入力補完が効きづらい
  - 再エクスポートの際に名前をつける必要がある

### named export

- Pros:
  - エディター、IDEによる入力補完が効く
  - ひとつのファイルから複数exportできる
- Cons:
  - (名前の変更はできるものの)基本的に決まった名前でimportして使う必要がある
  - exportしているファイルが名前を変更すると動作しなくなる

### ファイルが提供したいもの

### 今回の問題点

### named exportだとF
