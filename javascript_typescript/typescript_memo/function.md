## 関数の宣言方法

[](https://typescriptbook.jp/reference/functions)を参考.

```typescript
function add_nums(num_1: number, num_2: number): number {
  return num_1 + num_2;
}
```

TypeScriptで戻り値がない関数において、戻り値を明示的にタイプヒントするには`void`型を用いる

```typescript
function print(message: string): void {
  console.log(message);
}
```

`undifined`型もある.
戻り値型が`undefined`型の場合は、`return undefined`が必要.

## 値渡しと参照渡し

プログラミング言語によっては、引数の渡し方に**値渡し(pass-by-value)**と**参照渡し(pass-by-reference)**の2種類が存在する.

### 値渡し

変数が関数に渡るタイミングで、変数が別の変数にコピーされる.
**元々同じ変数でも、関数の呼び出し元と関数の内部処理では、独立した値**になる.
そのため、関数の処理で引数に値を代入しても、関数呼び出し元の変数に影響しない.

### 参照渡し(pass-by-reference)

**関数呼び出し元の変数が関数内の処理でも共有**される.
もし、関数の処理で引数に値を代入すると、関数呼び出し元の変数も変化する.

### JavaScriptは値渡し

javascriptは全て値渡しらしく、参照渡しの機能がない.

しかし、オブジェクト型については少し特殊で、どこでも参照渡しになる.

どういうことかというと、**オブジェクトに別の変数名をつけても**、オブジェクトが複製されて新たなオブジェクトができるのではなく、**異なる変数名同士でひとつのオブジェクトを指す**ということ.
たとえば、次の例のようにオブジェクト{ n: 1 }を変数xに代入し、さらにxを変数yに代入すると、xとyは同じオブジェクトを参照する.
もし、**yのプロパティnを変更すると、xのnも変化**する.

```typescript
const x = { n: 1 };
const y = x;
y.n = 2;
console.log(x);
// -> { n: 2 }
```

ただし、yに別の値を代入した場合は、xとyは共通のオブジェクトを参照しなくなり、yへの変更はxには影響しなくなる.
(当然といえば当然！)

```typescript
const x = { n: 1 };
let y = x;
y = { n: 2 }; // yに別オブジェクトを再代入
y.n = 3;
console.log(x);
// -> { n: 1 }
```

以上のようにJavaScriptでは、あるオブジェクトに別の変数をつけたとき、そのオブジェクトを共有するようになっている.
共有されたオブジェクトはプロパティを変更した場合、他の変数にもその変更が影響する.
**この仕様は引数にも同じことが言える**.

たとえば、次の例. オブジェクト{ n: 1 }を変数xに代入し、さらにxを関数changeの引数yに代入すると、xとyは同じオブジェクトを参照する.
**関数内でyのプロパティを変更すると、その影響は関数呼び出し元のxのプロパティにも影響する**.

```typescript
function change(y) {
  y.n = 2;
}
const x = { n: 1 };
change(x);
console.log(x);
// -> { n: 2 }
```

## オプション引数

オプション引数(optional parameter)は、渡す引数を省略できるようにするTypeScript固有の機能.
疑問符?を引数名の後ろに書くことで表現.

```typescript
// function 関数名(引数名?: 型) {}
function hello(person?: string) {}

hello(); // 引数を省略して呼び出せる
hello("alice"); // 省略しない呼び出しももちろんOK
```

オプション引数の型は、指定した型とundefinedのUnion型になる. 上の例で言えば、`(parameter) person: string | undefined`.

オプション引数は、引数の型がundefinedとのユニオン型になるため、そのままでは使えずコンパイルエラーになる.
以下の二種の方法がある.

### デフォルト値を代入する

引数がundefinedの場合分けをif文で書き、そこでデフォルト値を代入する方法.

```typescript
function hello(person?: string) {
  if (typeof person === "undefined") {
    person = "anonymous";
  }
  return "Hello " + person.toUpperCase();
}
```

**Null合体代入演算子**`??=`でデフォルト値を代入する方法もある.

```typescript
function hello(person?: string) {
  person ??= "anonymous";
  return "Hello " + person.toUpperCase();
}
```

さらに、デフォルト引数を指定することでも同じことができる. 多くのケースでは、デフォルト引数を使うほうがよい.(デフォルト引数の機能合ってよかったー...)

```typescript
function hello(person: string = "anonymous") {
  //                          ^^^^^^^^^^^^^デフォルト引数
  return "Hello " + person.toUpperCase();
}
```

### 処理を分ける

オプション引数を取り回すもうひとつの方法は、処理を分けること.(まあやってる事は、undifindの場合にearly returnしてるって感じ！)

```typescript
function hello(person?: string) {
  if (typeof person === "undefined") {
    return "Hello ANONYMOUS";
  }
  return "Hello " + person.toUpperCase();
}
```

### `データ型 | undifined`との違い

オプション引数はユニオン型`T | undefined`として解釈される.であれば、引数の型を`T | undefined`と書けば同じなはず.なぜTypeScriptは、疑問符`?`という別の記法を用意したのか??
これには呼び出す側で、**引数を省略できるかどうかという違い**...!

### オプション引数の後に、普通の引数は書けない.

## デフォルト引数

引数にundefinedを渡す場合、デフォルト引数が適用される.
JavaScriptの引数は省略するとundefinedになる.よって引数が省略された場合もデフォルト引数が入る.

引数にnullが渡されたときは、デフォルト引数は適用されない.

JavaScriptのデフォルト引数は、デフォルト値を持たない引数の前に書くことができる.

### 初期化処理が書ける

JavaScriptのデフォルト値には式が書ける.`function foo(x = 2 * 2) {}`
式が書けるので、関数呼び出しも書ける.`function foo(x = parseInt("1.5")) {}`

### 型推論が効く.

TypeScriptでは、デフォルト引数があると、引数の型推論が効く.
そのため、デフォルト引数が型ヒントを省略することもできる.
