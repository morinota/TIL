<!-- javascriptを生まれて初めて触ったので、とりあえずimplicit ALSを実装してみた(推薦システム) -->

# はじめに

就職活動の一貫で、ペアプロ的な面接の機会があり、その際に「javascript or typescriptを使用します」との事だったので、面接前に生まれて始めてjavascriptを触ってみようと思いました. (私はpythonを結構ガッツリめに、golangを少々かじっている者です.)
じゃあどう触ろうかという事で、私はRecommender SystemやPersonalizeが技術的にも理念的にも好きなので、有名な推薦アルゴリズムの一つである implicit ALSを実装してみる事にしました...!

# implicit ALSってなんぞや?

implicit ALSは、推薦システムにおける協調フィルタリングベースの手法で、**ユーザuのアイテムiに対する評価値**(ex. rating, feedback, reaction, etc.)が各要素に格納されたような**評価行列(rating matrix, ユーザ=行, アイテム=列)**を分解する"**行列分解(Matrix Factorization)**"と呼ばれる手法の一つです.

ALS(Alternating Least Square)の場合は、各ユーザの各アイテムに対する評価値を格納した評価行列$R$を、各ユーザのベクトルからなる**ユーザ行列**Xと、各アイテムのベクトルからなる**アイテム行列**Yの積に分解します.

$$
R \approx X \cdot Y^T = \hat{R}
$$

ALSでは、潜在変数の個数(=グルーピングの数)k を与えた時、評価行列 R を X と Y の積に分解します.
正確には、Xにできる限り近い(近似した)$\hat{R} = X \cdot Y^T$を推定します.
得られた$\hat{R}$によって、ユーザがまだ評価していないアイテムの評価値を予測したり、ユーザの好みを定量化する事ができます.

implicit ALSに関する理論の詳細に関して興味と時間がある場合は、[私の過去の記事](https://qiita.com/morinota/items/9bd9f6ebff13d962d75b)や元論文[Collaborative Filtering for Implicit Feedback Datasets](http://yifanhu.net/PUB/cf.pdf)等を参照してください.

# javascriptの作法を学ぶ

では続いて、公式ドキュメントを見ながらjavascriptのお作法を学んでいきます.

## 変数宣言

なるほど、変数宣言は`let`を使うと.

```javascript
let myVariable;
myVariable = "Bob";

// 宣言と代入を一行で行うver. let myVariable = 'Bob';
```

なんとなく変数宣言は`var`だと思っていましたが、どう違うんだろう.

[この記事](https://techplay.jp/column/1619)を参考に調べました！

- javascriptには`let`, `var`, `const`の3つの宣言方法がある.
- `const`は定数. 再代入も再宣言もできない.
- `let`と`var`は変数.
  - `let`: 再宣言が不可. スコープがブロックスコープ(pythonにはブロックという概念が無い気がする...? `{}`で囲まれた、for文の中とかif文の中とかの印象)
  - `var`: 再宣言が可能. スコープが関数スコープ(pythonにおける変数の扱いと同一?)

なるほどなるほど...ふむふむふむ.

javascriptは動的型付け言語なので、データタイプは指定しないとは思うんですが、pythonでいうタイプヒントみたいな作法はあるのかなー...

変数名は"小文字始まりのキャメルケース"

## データタイプ

### 数値型(numbers)
intもfloatも"number"タイプになる.

```
let myAge = 17;
```



### 文字列型(strings)

```
let dolphinGoodbye = 'So long and thanks for all the fish';
```

### 真偽値(booleans)

```
let iAmAlive = true;
let test = 6 < 3;
```

### 配列(arrays)

```javascript
let myNameArray = ['Chris', 'Bob', 'Jim'];
let myNumberArray = [10, 15, 40];

myNameArray[0]; // should return 'Chris'
myNumberArray[2]; // should return 40
```

object??

pythonでいうdictみたいな?もしくはデータクラス的な??

```javascript
let dog = { name : 'ポチ', breed : 'ダルメシアン' };
dog.name; // should return "ポチ"
```

## 演算子

[公式document](https://developer.mozilla.org/ja/docs/Learn/Getting_started_with_the_web/JavaScript_basics#%E6%BC%94%E7%AE%97%E5%AD%90)を読んでいきます.

加減乗除の演算子はpythonと同じ.
等号、不等号は`===`と`!==`という事で、pythonよりも一つ`=`を多く後ろにつけるんですね...!

## 条件文(conditionals)

なるほど...以下のような感じで、条件を`()`で対応する処理を`{}`で囲むんですね.
`{}`で囲まれた箇所をブロックというのかな.

```javascript
let iceCream = "チョコレート";
if (iceCream === "チョコレート") {
  alert("やった、チョコレートアイス大好き！");
} else {
  alert("あれれ、でもチョコレートは私のお気に入り......");
}
```

## 関数の定義

以下のような感じで定義する、と.

```javascript
function function_name(argument_1, argument_2) {
  let result = argument_1 * argument_2;
  return result;
}
```

個人的には、引数と返り値がどんなデータタイプなのか、宣言するなりタイプヒントを追加するなりして読み手に伝えたいですね...!(pythonのタイプヒント好きなんだよなー...)

## イベント

今回のimplicit ALSではウェブサイトを作って機能を追加する訳では無いので使いませんが一応.
ウェブサイトをInteractive(対話的)にする際に、この"イベント"という概念が必要らしい.
例えば`click`イベントが発生したら、`alert`functionを呼び出す、みたいな.

```javascript
document.querySelector("html").addEventListener("click", function () {
  alert("痛っ! つつかないで!");
});
```

↑の例は、`html`elementにて`click`eventが発生した際に、`alert`functionが実行される.

なお上の記述は、以下と同等.

```javascript
let myHTML = document.querySelector("html");
myHTML.addEventListener("click", function () {
  hogehoge("argument_value");
});
```

## 無名関数

なお上のコードで`addEventListener`には無名関数を渡している.(無名関数の中でalertが呼ばれる.)

無名関数の書き方は二通り?
`function ()`を使う方法とアロー関数`() =>`を使う方法.

```javascript
document.querySelector("html").addEventListener("click", () => {
  alert("痛っ! つつかないで!");
});
```

```javascript
document.querySelector("html").addEventListener("click", () => {
  alert("痛っ! つつかないで!");
});
```




# いざjavascriptでimplicit ALSを実装する.
