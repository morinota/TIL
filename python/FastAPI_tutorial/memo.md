# 1. 起動コマンド関連

```
uvicorn main:app --reload
```

- `main`: `main.py`ファイル。
- `app`: `main.py`内部で作られるobject(`app = FastAPI()`の様に記述される).
- `--reload`:コードの変更時にサーバーを再起動させる.開発用.

### 1.0.1. 対話型API documentを開く..

http://127.0.0.1:8000/docs にアクセスする.
自動生成された対話的APIドキュメントが表示される(Swagger UIで提供)

### 1.0.2. 他のAPI Documentを開く.

次に、http://127.0.0.1:8000/redoc にアクセスする。
先ほどとは異なる、自動生成された対話的APIドキュメントが表示される (ReDocによって提供):

### 1.0.3. openAPI スキーマを確認したい場合.

次の場所で直接確認できる：http://127.0.0.1:8000/openapi.json

## 1.1. 簡単なmain.pyのステップ

### 1.1.1. Step 1: `FastAPI`をImport

- FastAPIは、APIの全ての機能を提供するPythonクラス

### 1.1.2. Step 2:`FastAPI`のインスタンスを生成.

- 一般的には, `app`変数が`FastAPI`クラスのインスタンスとする.
- これが、全てのAPIを作成する為のmain pointになる.
- **この`app`は、コマンドで`uvicorn`が参照するものと同じ**

### 1.1.3. Step 3： path operation を作成(宣言)

- ここでの"path"とは、最初の`/`から始まるURLの最後の部分.
  - ex) `https://example.com/items/foo`の場合、pathは`/items/foo`.
  - pathは一般に、**"endpoint"** または **"root"** とも呼ばれる.
- ここでの"operation"とは、HTTPのメソッドの1つを指す.
  - ex)
    - POST, GET, PUT, DELETE
- APIを構築する時は、通常、これらの特定のHTTPメソッド(=operation)を使用して、特定のアクションを実行する.
  - 通常は以下を使用する：
    - POST(データの作成), GET(データの読み取り), PUT(データの更新), DELETE(データの削除)
- 従って、OpenAPIでは、各HTTPメソッドは"**operation**"と呼ばれる.

Path Operation デコレータを定義する.

```python
# ...略

@app.get("/") # ここ！！
async def root():
    return {"message": "Hello World"}
```

`@app.get('/')`は、直下の関数が、下記のリクエストの処理を担当する事をFastAPIに伝える.

他のoperationも使用できる： `@app.post()`, `@app.put()`, `@app.delete()`

ここで、operation=`get`, path=`/`, `root()`は **path operation function**.
path operation function `root`は、`GET` operationを使った path `/`へのリクエストを受け取る度に、FastAPIによって呼び出される.

async function `async def hogehoge()`の代わりに、通常の関数`def hogehoge()`として定義する事もできる.
違いは、**非同期処理**にするか否か？？
https://fastapi.tiangolo.com/ja/async/#in-a-hurry 参照

path operation function は 何らかのコンテンツをreturnする.
dict, list, str, int等のprimitive型の他に、Pydanticモデル(=クラス?)を返す事もできる.

# 2. path parameter とpath variable

format string と同様のシンタックス(形式)で"path parameter"や "path variable"を宣言(declare)できる.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

パスパラメータ の値は、引数 item_id としてpath operator function に渡される.

path operator functionにtype hintを指定する事で、data translation と data validationが適用される.

FastAPIにおける全ての **data validation は、Pydanticによって**内部で実行される.

## 2.1. path parameterの値を細かく定義する.

**有効な path parameter の値を細かく定義したい場合**は、build-inの `Enum`クラスを利用できる.

上の章では、intであれば何でも path parameter を受け取る事ができていた. 今度はそれを更に細かく指定したい！って話

- `Enum` をインポートし、 `str` と `Enum` を継承したサブクラスを作成する.
  - `str` を継承することで、APIドキュメントは値が `文字列` でなければいけないことを知り、正確にレンダリングできるようになる.
  - そして、固定値の class property を作る. その値がpath parameter として 使用可能な値となる.

```python
class ModelName(str, Enum): # ここ！
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    return {"model_name": model_name, "message": "Deep Learning FTW!"}
```

## 2.2. `fastapi.Path`を用いてpath parameterにより細かい設定をdeclareする.

`Query` でquery parameter に対するvalidationやメタデータをdeclareできるのと同じように、 `Path` でもpath parameter に対するvalidation やメタデータをdeclareできる.

```python
@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(title="The ID of the item to get"), # ここ！
    q: Union[str, None] = Query(default=None, alias="item-query"),
):
    # 略
```

path parameter はpathの一部でなければならないので、常に**必須**である.

数値型のvalidation:

- gt: より大きい
- ge: 等しいかそれ以上
- lt: より小さい
- le: 以下または等しい

- Technical Details:
  - fastapiから`Query`や`Path`などをインポートするとき、それらは実際にはfunctionである.
    - 呼び出されると、同じ名前のクラスのインスタンスを返す.
  - これらの関数は（クラスを直接使用する代わりに）、エディタが型に関するエラーをマークしないように用意されている.(??)

# 3. Query parameter

path parameterではないfunction parameterを宣言すると、それらは自動的に **query parameter** として解釈される.
クエリはURL内で`?`の後に続くkeyとvalueの組で、`&`で区切られている.

- ex) 下の様なURL内で`http://127.0.0.1:8000/items/?skip=0&limit=10`の場合、
  - query parameterは以下.
  - `skip`: 値は `0`
  - `limit`: 値は `10`

query parameter はURLの一部なので、"自然に"string扱いになる.
しかしtype hintを用いると (上記の例では int として)、data typeのtranslate & validation が行われる.
(path parameter に適用される処理と完全に同様な処理が query parameterにも適用される)

## 3.1. query parameterのdefault value や Optional

Query parameterはpathの固定部分ではないので、Optionalとしたり、デフォルト値をもつことができる.
(逆に言えば、**path parameterはdefalut値を持てない**...?)
(`Optional[str]` はFastAPIでは認識されない. strと判断するらしい.)

```python
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
```

path parameter と同様に、query parameterに対しても`Enum`を使用して、取り得るparameterの値を制限できる.

## 3.2. `fastapi.Query`を用いて、query paremeterをより細かくdeclareする

### 3.2.1. query parameterで受け取る文字列のvalidationを追加

`fastapi.Query`を用いて、query parameterのvalidationを追加できる.

```python
app = FastAPI()


@app.get("/items/")
async def read_items(q: Union[str, None] = Query(default=None, max_length=50)): # ここ！
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```

これにより、データをvalidation し、データが有効(valid)でない場合は明確なエラーを表示する.

query parameter が一致するべき正規表現も定義できる.

```python
q: Union[str, None] = Query(
        default=None, min_length=3, max_length=50, regex="^fixedquery$"
    )
```

### 3.2.2. query paremeterで list(複数の値)を受け取る方法

query paremeter を明示的に`Query`で宣言した場合、list型等の複数の値を受け取るように宣言可能になる.
(=fastAPIは単数系typeのみをquery parameterとみなす. **明示的にqueryと示さない場合、list型はrequest bodyとして解釈される**.)

```python
@app.get("/items/")
async def read_items(q: Union[List[str], None] = Query(default=None)):
    query_items = {"q": q}
    return query_items
```

URLは以下:

```
http://localhost:8000/items/?q=foo&q=bar
```

この場合のresponce bodyは以下.

```json
{
  "q": ["foo", "bar"]
}
```

### 3.2.3. query parameterに関わるより多くのメタデータをdeclareする.

`Query`を用いる事で、validationの他にもquery parameterに関わるより多くのメタデータをdeclareできる.
その情報は、生成されたOpenAPIに含まれ、documentのUIや外部のツールで参照される.

```python
q: Union[str, None] = Query(
        default=None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
    )
```

### 3.2.4. alias parameter

Pythonで有効でないquery parameter名を指定したい.

- ex.) `http://127.0.0.1:8000/items/?item-query=foobaritems`における`item-query`
- 代替として、最も近いのはitem_queryだろう.
- しかし、どうしても`item-query`と正確に一致している必要があるとする.(client側の都合で...!)

その場合、aliasをdeclareすることができる.
aliasは、parameter の値を見つけるのに使用される.

```python
async def read_items(q: Union[str, None] = Query(default=None, alias="item-query")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```

### 3.2.5. 非推奨パラメータ

さて、あるquery paraemeterが気に入らなくなったとする.
それを使っているクライアントがいるので、しばらくは残しておく必要がありますが、ドキュメントには"非推奨"と明示的に示しておきたい.

その場合、`Query`にパラメータ`deprecated=True`を渡せばよい. Documentで見た際に"非推奨"ということがわかる.

```python
    q: Union[str, None] = Query(
        default=None,
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
        regex="^fixedquery$",
        deprecated=True,
    )
```

# 4. Request Body

client (ブラウザなど) からAPIにデータを送信する必要があるとき、データを **request body** として送る.
(request bodyはclientからAPIへ送られる. **responce body**はAPIからclientに送るデータ.)

APIはほとんどの場合 何らかのresponce bodyを送るが、client は必ずしもrequest bodyを送る訳では無い.

request bodyをdeclareする為に、**Pydantic.BaseModel**を使用する.

request bodyを送るには、`POST`(最もよく使われる)、`PUT` , `DELETE`, または`PATCH`がpath operator(HTTP method)として使われる.

## 4.1. pydantic.BaseModelを用いて data model(request bodyの雛形?)を定義する.

```python
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
```

上記のdata modelは、下記の様なJSONオブジェクト(もしくはPythonの `dict` )をdeclareしている.

```json
{
  "name": "Foo",
  "description": "An optional description",
  "price": 45.2,
  "tax": 3.5
}
```

path operation function に加えるためには、path parameter やquery parameterと同じ様にdata modelを宣言すればよい.

```python
app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    return item
```

### 4.1.1. request body + path parameter + query parameterの例.

FastAPI はそれぞれを認識し、適切な場所からデータを取得する.

```python
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
```

それぞれのfunction parameters は以下の様に判定される:

- parameter名がpath内で宣言されている場合は、優先的にpath parameterとして扱われる.
- paramterが**単数型**(`int`、`float`、`str`、`bool` など)(=List等の複数形のdata typeはpath operator functionでは定義できない...??確かに不要な気はする.)の場合は、query parameterとして解釈される.
- parameter が `pydantic.BaseModel`クラスでdeclareされた場合、request bodyとして解釈される.

## 4.2. Multiple body parameters 複数のrequest body parameterを受け取る.

```python
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


class User(BaseModel):
    username: str
    full_name: Union[str, None] = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results
```

FastAPIはpath operator function内に複数の body parameter があることに気づく(`pydantic.BaseModel`である2つのパラメータ）.

上のケースでは、parameter名をbodyのkey(field名)として使用した、以下のようなrequest bodyを期待する.
(body parameterが２つある状況は、**一つのrequest bodyを複数に分割する**、みたいなイメージ??)

```json
{
  "item": {
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
  },
  "user": {
    "username": "dave",
    "full_name": "Dave Grohl"
  }
}
```

## 4.3. request body parameterのvalidation

query parameterやpath parameterに追加データをdeclareするために`Query`や`Path`があるのと同じように、FastAPI は同等の`Body`を提供する.

```python
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


class User(BaseModel):
    username: str
    full_name: Union[str, None] = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User, importance: int = Body()):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results
```

上の例で、`importance`引数はint型であるため、そのままdeclareすると、FastAPI はquery parameter であると見なす. しかし, `Body`をdeclareする事で、単数系のdata typeでもrequest body parameterと判断できる.

In this case, FastAPI will expect a body like:

```json
{
  "item": {
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
  },
  "user": {
    "username": "dave",
    "full_name": "Dave Grohl"
  },
  "importance": 5
}
```

### 4.3.1. 単一の request body parameter

body parameter が`Item`モデルクラス1つだけのケースを想定する.

デフォルトでは、FastAPIはそのbody(=Itemのfieldの中身)を直接期待する.
しかし以下のように、key=`Item`とその中にあるcontent(fieldの中身)を含むJSONを期待したい場合は、特別なrequest body parameterの埋め込みを使うことができる.

```json
{
  "item": {
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
  }
}

// ↓ではないケース. `Body(embed=False)`の場合は下のrequest bodyを期待してる.
// {
//     "name": "Foo",
//     "description": "The pretender",
//     "price": 42.0,
//     "tax": 3.2
// }
```

上のrequest bodyを期待したいケースでは、以下のように`Body(embed=True)`としてdeclareすれば良い.

```python
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(embed=True)): # ここ
    results = {"item_id": item_id, "item": item}
    return results
```

### 4.3.2. request body parameterの各要素に対して、`pydantic.Field`で設定をdeclareする.

`pydantic.Field`では、`pydantic.BaseModel`の各field(=**request body parameterの各要素!**)に対して追加のvalidationやmetadataをdeclareできる.
そして、それは生成されたJSONスキーマ(=API document?)に含まれることになる.

```python
class Item(BaseModel):
    name: str
    description: Union[str, None] = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: Union[float, None] = None
```

### 4.3.3. request body parameterのnested化

FastAPI を使用すると、任意に深くネストされたモデル(=request body parameter)をdeclare、validation、documentation、使用できる.

BaseModelのfieldに、別のBaseModel(=**submodel**)を格納するケースを考える.

```python
class Image(BaseModel):
    url: str
    name: str


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()
    image: Union[Image, None] = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
```

上のケースでは、FastAPIが次のようなrequest bodyを期待している.

```json
{
  "name": "Foo",
  "description": "The pretender",
  "price": 42.0,
  "tax": 3.2,
  "tags": ["rock", "metal", "bar"],
  "image": {
    "url": "http://example.com/baz.jpg",
    "name": "The Foo live"
  }
}
```

### 4.3.4. `List[submodel]`をrequest body parameterのfieldとして期待するケース

Pydanticモデルをリストやセットなどのサブタイプとして使用することもできる.

```python
class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()
    images: Union[List[Image], None] = None
```

このケースで、fastapiが期待するrequest bodyは以下.

```json
{
  "name": "Foo",
  "description": "The pretender",
  "price": 42.0,
  "tax": 3.2,
  "tags": ["rock", "metal", "bar"],
  "images": [
    {
      "url": "http://example.com/baz.jpg",
      "name": "The Foo live"
    },
    {
      "url": "http://example.com/dave.jpg",
      "name": "The Baz"
    }
  ]
}
```

## 4.4. Request BodyのExample data をdeclareする

アプリが受け取ることができるデータ(request body)の例をdeclareできる.

ここではいくつかの方法を紹介する.

### 4.4.1. pydanticの`schema_extra`を用いる方法

request body parameterのBaseModelクラスの中に、`schema_extra`fieldを持つ`Config`を定義する事でExample dataをdeclareできる.
そのモデルの出力JSON Schemaにそのまま追加され、APIドキュメントで使用される.
`schema_extra` fieldに`example`以外のメタデータを追加する事もできる.

```python
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }
```

### 4.4.2. `pydantic.Field`のaddtional arguments(=\*argの引数?)を用いる方法

Pydanticモデルで`Field()`を使用する場合、他の任意の引数を渡すことで、JSON Schemaのための特別な情報をdeclareできる.
これを利用して、request body parameterの各fieldのexampleを追加できる.
(additional argumentsは何のvalidationも行わず、API ducumentation のための追加情報としての利用される.)

```python
class Item(BaseModel):
    name: str = Field(example="Foo")
    description: Union[str, None] = Field(default=None, example="A very nice Item")
    price: float = Field(example=35.4)
    tax: Union[float, None] = Field(default=None, example=3.2)
```

### 4.4.3. OpenAPI(=FastAPI?)の`example`や`examples`を用いる方法

Path, Query, Body等のFastAPIのdeclare用クラスを使っている場合、OpenAPI(=API doc??)に追加されるdata `example` や `examples` をdeclareすることもできる.
以下では`Body()`で期待されるdata `example`をdeclareしている.

```python
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item = Body(
        example={
            "name": "Foo",
            "description": "A very nice Item",
            "price": 35.4,
            "tax": 3.2,
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results
```

### 4.4.4. Example in the docs UI

上記のいずれの方法でも、docs UI(`/docs`)には以下のように表示される.

![](https://fastapi.tiangolo.com/img/tutorial/body-fields/image01.png)

### 4.4.5. 単一の`example`ではなく、複数の`examples`をdeclareする.

単一のexampleではなく、複数のexampleを持つdictを使用して`examples`をdeclareする事もできる.
dict のkeyがそれぞれのexampleを特定し、それぞれのvalueが別の dict となる.

`examples` の中のそれぞれの具体的な`example`の dict には、以下のものを含めることができる.

- `summary`: 例に対する短い説明.
- `description`: Markdownテキストを含むことができる長い説明.
- `value`: これは示された実際のexample. 例えば、dict.
- `externalValue`: valueの代わりとなるもので、例を指すURL. これはvalueとは異なり、多くのツールでサポートされていないかもしれない.

```python
@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item = Body(
        examples={ # 複数のexamplesをdeclare
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** item works correctly.",
                "value": {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
            "converted": {
                "summary": "An example with converted data",
                "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                "value": {
                    "name": "Bar",
                    "price": "35.4",
                },
            },
            "invalid": { # 良くないexampleも含める事ができる.
                "summary": "Invalid data is rejected with an error",
                "value": {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            },
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results
```

# 5. Extra Data Types

## 5.1. 特殊なdata typeとvalidationについて

str、int、float などの通常の単数型とは別に str を継承した、より複雑な**singular data types**を使用できる.

どのようなsingular data typesがあるかは、Pydanticの**exotic types**に関するドキュメントを参照してください. いくつかの例をあげる.

## 5.2. `pydantic.HttpUrl`

```python
class Image(BaseModel):
    url: HttpUrl
    name: str
```

## 5.3. Other data types

- `UUID`:
- `datetime.datetime`
- `datetime.date`
- `datetime.time`
- `datetime.timedelta`
- `frozenset`:
  - In requests and responses, treated the same as a `set`:
    - request時にはlistを読み込みsetに変換する.
    - response時には、setをlistにconvertする.
    - 生成されたschema(=API doc?)には、set扱いになる.
- `bytes`:
  - Pythonの標準的なバイト.
  - リクエストとレスポンスではstrとして扱われる.
  - リクエストとレスポンスではstrとして扱われる.
- `Decimal`:
  - Pythonの標準的な10進数。
  - リクエストやレスポンスにおいて、floatと同じように扱われる.

以下に、上記のextra data typeのいくつかを使ったparameter群によるpath operation functionの例を示す.

```python
@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Union[datetime, None] = Body(default=None),
    end_datetime: Union[datetime, None] = Body(default=None),
    repeat_at: Union[time, None] = Body(default=None),
    process_after: Union[timedelta, None] = Body(default=None),
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }
```

# 6. Cookie parameter

cookie parameter は、query paremter やpath parameterと同じ方法でdeclareできる.
`fastapi.Cookie`を用いて、cookie parameterの設定をdeclare & validation できる.
(cookie parameterをdeclareするには、`Cookie`を使う必要がある. なぜなら、**そうしないと定義したparameterがquery parameterとして解釈されてしまう**...!)

```python
@app.get("/items/")
async def read_items(ads_id: Union[str, None] = Cookie(default=None)):
    return {"ads_id": ads_id}
```

# 7. Header parameter

header parameterは, query parameterやpath parameterと同じ方法でdeclareできる.
`fastapi.Header`を用いて、 header parameterの設定をdeclare & validation できる.
(header parameterをdeclareするには、`Header`を使う必要がある. なぜなら、**そうしないと定義したparameterがquery parameterとして解釈されてしまう**...!)

```python
@app.get("/items/")
async def read_items(user_agent: Union[str, None] = Header(default=None)):
    return {"User-Agent": user_agent}
```

## 7.1. auto translate

`Header`は`Path`や`Query`、`Cookie`が提供する機能に加え、少しだけ追加の機能を持っている.

ほとんどの標準ヘッダーは、「マイナス記号」（-）としても知られる「ハイフン」で区切られている.
しかし`user-agent`のような変数名はPythonでは無効.
そのため、defaultでは`Header`は header parameterの文字をアンダースコア`_`からハイフン`-`に変換して、headerを探索してparameterを抽出する.

またHTTP headerは大文字小文字を区別しない為、header parameter名はスネークケースでdeclareできる.

## 7.2. headerの重複

受信したヘッダーが重複することがあります。つまり、同じヘッダーで複数の値を持つということ.
これらの場合、リストの型宣言を使用してdeclareできる.

重複したheaderのすべての値を、header parameterではPythonのlistとして受け取れる.

```python
@app.get("/items/")
async def read_items(x_token: Union[List[str], None] = Header(default=None)):
    return {"X-Token values": x_token}
```

上のpath operation functionは、以下のように2つのHTTP headerを期待している.

```
X-Token: foo
X-Token: bar
```

# 8. Responsce Modelの設定をdeclareする.

## 8.1. path operation functionの返り値のtype hintを用いる方法

path operation functionの返り値のtype hintをつける事で、responseのdata typeをdeclareできる.

FastAPIでは、返り値のtype hintを用いて以下の事ができる.

- responseのvalidation
  - データがinvalidな場合、app codeが壊れている事を意味し、**invalidなデータではなくserver errorを返す**.(type hintではなく、きちんとtype annotationとして機能するのか...!)
- responceの為のjson schemaを OpenAPI path operation(=automaticで生成されるdocumentの事)に追加してくれる.

最も重要なのは、responce dataを返り値のtypeで定義されているものにlimit & filter処理をする. = security的に特に重要...!

## 8.2. response model parameter

また、path operation functionのに付与している**decorator**の`response_model`引数に指定する事ができる...!
(notice that... `response_model`引数はdecoratorメソッドのparameter! path operator functionのparameterではない!)
(`response_model`引数でresponce modelの設定をdeclareする場合は、path operator functionの返り値のtype hintを`Any`としておくと良い.=曖昧にしとく?)

```python
@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Any:
    return item

@app.get("/items/", response_model=List[Item])
async def read_items() -> Any:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]
```

### 8.2.1. response model の priority

"path operation funcitonの返り値のtype hint"と"decoratorの`response_model`引数"の両方でdeclareしたケースでは、FastAPIは後者のdeclareを優先する.

`response_model=None`を指定して、そのpath operation の response modelの作成を無効にすることも可能.

## 8.3. input dataをそのままresponseとして(ただ秘匿情報のみ隠して)返したい場合

ここでは `UserIn` モデルをdeclareしている. これにはプレーンテキストのパスワードが含まれる.

```python
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Union[str, None] = None


# Don't do this in production!
@app.post("/user/")
async def create_user(user: UserIn) -> UserIn:
    return user
```

password が response modelとして返されてしまうのがかなり危険.

この場合、秘匿性の高い情報(field)を取り除いたoutput modelを別途、declareすれば良い.

```python
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user
```

ここでは path operation functionが、passwordを含む入力値と同じ`user`を返しているが、`response_model`にdeclareしている`UserOut`modelには`password`fieldが含まれていない為、pydanticは`user`を`UserOut`に変換してresponseを返してくれる...!
(**FastAPI はpydanticによって、response model でdeclare されていないすべてのデータを除外してくれる**...!!)

### 8.3.1. どちらを使うべき?: `response_model` or 返り値のtype hint

上のケースでは、"返り値のtype hint"を用いた場合、editorやtoolはinvalidだと怒ってしまう.
＝＞このようなdata filtering が必要なケースでは、`response_model`がbetter.

### 8.3.2. "返り値のtype hint"でも、data filteringを行いたい.

Abstract Base Class 等のクラスのinheritance(継承)を適用する事で、type hintを用いる方法でも data filteringが可能.

```python
class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserIn(BaseUser):
    password: str


@app.post("/user/")
async def create_user(user: UserIn) -> BaseUser:
    return user
```

## 8.4. 他の "path operation functionの返り値のtype annotation"

### 8.4.1. `faspapi.Response`クラスを直接用いる.

最も単純なケース.

```python
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, RedirectResponse

app = FastAPI()


@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return JSONResponse(content={"message": "Here's your interdimensional portal."})
```

### 8.4.2. `faspapi.Response`のサブクラス(子クラス)を用いる.

```python
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/teleport")
async def get_teleport() -> RedirectResponse:
    return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
```

## 8.5. Invalid Return Type Annotations

ただし、有効な Pydantic 型ではない他の任意のオブジェクト (database オブジェクトなど)を返し、関数でそのようにannotationを付けると、FastAPI はその type annotation から Pydantic response model を作成しようとし、失敗する.

1 つ以上の型が有効な Pydantic 型ではない異なる型間の結合のようなものがある場合、同じことが起こる. たとえば、これは失敗する.
-> type annotationが Responseと dictのUnion(2つのうちのどちらか)の為...(??)
-> FastAPIによって自動生成されるOpenAPI docが壊れるから??

```python
@app.get("/portal")
async def get_portal(teleport: bool = False) -> Union[Response, dict]:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return {"message": "Here's your interdimensional portal."}
```

この場合、`response_model=None`をdeclareする事で、response modelの生成をskipできる. これにより FastAPI アプリケーションに影響を与えることなく、必要な返り値のtype annotationを付与できる.

## 8.6. `response_model_exclude_unset`parameterの使用

`response_model_exclude_unset=True`をdeclareすると、response modelの生成時に適用されたdefalut値が、respose modelから除外される.
(response model生成時にsetされてないfieldが、responseから除外される.)

他にも、`app.decorator()`method には以下のようなparameterがある.

- `response_model_exclude_defaults=True`
- `response_model_exclude_none=True`

## 8.7. `response_model_include`引数 と `response_model_exclude`引数

```python
@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"}, # equal to set(["name", "description"])
)
async def read_item_name(item_id: str):
    return items[item_id]
```

# 9. Extra Models(ケーススタディ)

appの作成では、複数の関連したmodel(request model や response model...)があるのが一般的.

これは特に User モデルの場合に当てはまる.

- input model は plaintext password を持つことができる必要がある.
- output model にはパスワードを設定してはいけない.
- database model には、おそらく**password hash** が必要.
  - ユーザのplaintext passwordを保存してはいけない.
  - 後で検証できる"secure hash"を常に保存すべき.

```python
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: Union[str, None] = None


def fake_password_hasher(raw_password: str) -> str:
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn) -> UserInDB:
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn) -> Any:
    user_saved = fake_save_user(user_in)
    return user_saved
```

## 9.1. Unwrapping a dict(単にpythonのSyntaxの話ですが...)

dictを functionやclassの引数として`**dict`で渡す場合、Pythonは**unwrap**する.
i.e. dictの各itemが、functionのkey-value argumentとして渡される.

```python
user_in = UserIn(username="john", password="secret", email="john.doe@example.com")
user_dict = user_in.dict()
UserInDB(**user_dict)
```

unwapしたdictに加えて、extra keywordsもargumentとして渡す事ができる.

```python
UserInDB(**user_in.dict(), hashed_password=hashed_password)
```

## 9.2. duplication(重複)を減らす

コードのduplicationを減らすことは、FastAPI の中心的なアイデアの 1つ.

コードのduplicationにより、**バグ、セキュリティの問題、コードのdesynchronization(非同期化)の問題(ある場所ではコードを更新しても他の場所では更新し忘れる, なるほど...!)**などの可能性が高くなる.

これらのモデル(UserHogehoge)はすべて多くのデータを共有し、field の名前と型を複製している.
もっとうまくできるはずだ...!

他のモデルのベースとして機能する `UserBase` モデルをdeclareする.
そして、そのfield(type annotation、validationなど) を継承するそのモデルのサブクラスを作成するようにしてみよう.
(すべての data translation、validation、documentationなどはリファクタ前と同じように機能する.)

そうすれば子クラスでは、モデル間の違いだけをdeclareできる (plaintext passwordあり、hashed_password あり、パスワードなし):

```python
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str
```

## 9.3. `Union`を使う例(OpenAPIでは`anyOf`としてdocumentationされる.)

```python
class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type = "car"


class PlaneItem(BaseItem):
    type = "plane"
    size: int


items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}


@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]
```

## 9.4. Response として BaseModelのListを採用する例

responseを何らかのObjectのListとしてdeclareするケースを考える.

```python
class Item(BaseModel):
    name: str
    description: str


items = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]


@app.get("/items/", response_model=List[Item])
async def read_items():
    return items
```

## 9.5. Response として Dictを採用する例

```python
@app.get("/keyword-weights/", response_model=Dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}
```

# 10. Response Status Code

Response model を declareできるのと同じ方法で、decoratorの`status_code` parameterを使用して、path operation の response に使用される **HTTP status code**をdeclareできる.

```python
@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": name}
```

## 10.1. HTTP status codeに関して

HTTP では、responseの一部として 3 digit の数値 status codeを送信する.

これらのstatus code には、それらを認識するための名前が関連付けられていますが、重要な部分は番号である.

要するに：

- 100 and above are for "**Information**":
  - それらを直接使用する事はめったにない.
  - これらのstatus codeを含むresponseにbody(本文)を含める事はできない.
- 200 and above are for "**Successful**" responses:
  - これらは、最もよく使用するもの.
  - 200 is the default status code, which means everything was "OK".
  - Another example would be 201, "Created(作成済み)". databaseに新しいrecordを作成した後によく使用される.
  - A special case is 204, "No Content". このresponseは、clientに返すcontentがない場合に使用されるため、responseにbodyを含める事はできない.
- 300 and above are for "**Redirection(リダイレクト)**".
  - bodyがある場合とない場合がある.
  - 304(Not Modified)は必ずbodyを持たない.
- 400 and above are for "**Client error**" responses.
  - これらは、おそらく最もよく使用する2番目のstatus code.
  - 404: for a "Not Found" response.
  - clientからの一般的なエラーの場合は、400 を使用できる.
- 500 and above are for **server errors**.
  - それらを直接使用することはほとんどない.
  - application code または server のどこかで問題が発生すると、これらの status code のいずれかが**自動的に(!)**返される.

## 10.2. Shortcut to remember the names(& status code)

`fastapi.status.`を使うと良い.

```python
@app.post("/items/", status_code=fastapi.status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}
```

# 11. Form data(request bodyに関して、jsonではなくform fieldを受け取る??)

JSON(=request body?)の代わりにform field(?)を受け取る場合は、`fastapi.Form`を使用する.

```python
from fastapi import FastAPI, Form

app = FastAPI()


@app.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}
```

## 11.1. Form Fieldとは??

**HTML Form（`<form></form>`）がサーバにデータを送信する方法(=Form field?)**は、通常、そのデータに「特別な」エンコーディングを使用しているが、これはjsonとは異なる.

# 12. request file parameter を受け取る.

clientがuploadするファイルは、`fastapi.File`と`fastapi.UploadFile`を使ってdeclareできる.
`Body`や`Form`と同じように、file parameterを作成する.
(`File`は`Form`をそのまま継承したクラス...!へぇー！)
(file parameterを`File`を使用してdeclareしないと、query parameter や request body parameter(=JSON)として解釈されてしまう.)

- default値に`File`を使うケース
  - request fileは "form data" としてuploadされる.
  - `bytes` typeのデフォルト値に`File`でdeclareすると、content全体がメモリに保存される...!(小さなファイルには有効)
- type hintに`UploadFile`を使うケース
  - `bytes`に比べていくつかの利点がある.
    - パラメータのデフォルト値で`File()`を使用する必要がない.
    - "spool"されたファイルを使用する.
      - **spooled file** = 最大サイズの制限まではメモリに保存され、この制限を超えた後はディスクに保存されるファイル.
      - -> つまり、画像、ビデオ、大きなバイナリなどの大きなファイルに対して、メモリを消費することなく、うまく動作する.
    - アップロードされたファイルからメタデータを取得できる.
    -

```python
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
```

## 12.1. `UploadFile`について

`UploadFile` has the following attributes:

https://fastapi.tiangolo.com/ja/tutorial/request-files/#uploadfile

## 12.2. file parameterをオプショナルにするケース

```python
@app.post("/files/")
async def create_file(file: Union[bytes, None] = File(default=None)):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: Union[UploadFile, None] = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}
```

## 12.3. Fileと UploadFileを一緒に使うケース

`UploadFile`タイプヒントの初期値に`File()` を使用すると、追加のmetadataを設定することができる.

```python
@app.post("/uploadfile/")
async def create_upload_file(
    file: UploadFile = File(description="A file read as UploadFile"),
):
    return {"filename": file.filename}
```

## Multiple File Uploads

同時に複数のファイルをアップロードすることが可能.

その場合、`bytes`か`UploadFile`のListをfile parameterのtype hintとしてdeclareする.

```python
@app.post("/files/")
async def create_files(files: List[bytes] = File()): # これ
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile]): # これ
    return {"filenames": [file.filename for file in files]}
```

# 13. SQL Databases(RDB)をapplicationに組み込む.

FastAPIのapplicationは、必ずしもSQL database(=RDB)を使う必要はない.(ex. PostgreSQL, MySQL, SQListe, Oracle, Microsoft SQL Server, etc.)

必要があれば、FastAPIとSQLAlchemyを組み合わせて適用できる.
(tips: サンプルコードのほとんどは標準的なSQLAlchemyのcode. FastAPI固有のcodeはほんのすこし)

## 13.1. 最もcommon: ORM(Object-Relational Mapping)を使用するパターン

SQL Databases(RDB)をapplicationに組み込む上で、一般的なパターンはORM(Object-Relational Mapping)ライブラリを使用する事.

- ORMとは:
  - code内のオブジェクト(ex. Domain Model) と Database table(=relation)間の変換(=map).
- ORMでは通常、RDBのテーブルを表すクラスを作成し、classの各fieldがDBのcolumnに対応する.
  - ex) `Pet` class -> RDBのpetsテーブル
- そのclass のインスタンスは、RDBテーブルの各recordを表す.

一般的なORM ライブラリ:

- Django-ORM (Django フレームワークの一部),
- SQLAlchemy ORM (SQLAlchemy の一部、フレームワークとは無関係),
- Peewee (フレームワークとは無関係), etc.

## 13.2. DBモデルクラスにmagic attribute `relationship`をdeclareする.

`my_user.items`にアクセスすると、users テーブルの このレコードを指す外部キーを持つ、`Item`モデル(items テーブルから)のリストを取得できる. (my_user.items にアクセスすると、SQLAlchemy は、実際にデータベースから items テーブルにあるアイテムを取得してくる...!)

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
```

## 13.3. SQLAlchemy models と Pydantic models のconfuseを避ける.

SQLAlchemy models(=ORMの為のDBモデル)とPydantic models(=request body やresponse bodyの設定をdeclareする為のBaseModel)のconfuseを避ける為に、前者を`models.py`に、後者を`schemas.py`(<=多かれ少なかれ**"schema"="validなデータの形を定義する"**ので...!)に記述するといい.

## 13.4. SQLAlchemy models と Pydantic models の declare styleの違い

SQLAlchemy modelsのケース

```python
name = Column(String)
```

Pydantic models

```python
name: str
```

## 13.5. pydanticの`orm_mode`を使用する.

pydantic BaseModelの internal `Config` classに `orm_mode = True`を追加する.
Pydanticの`orm_mode`は、Pydanticのモデルが`dict`ではなく、ORM model(または属性を持つ他の任意のオブジェクト)であってもデータを読み込むようにdeclareする.
(i.e. **dict以外からでも、pydantic modelのauto translationが効くようになる**って事...??)
これによって、Squalchemy ORM model -> response body modelの自動変換が可能になる.

```python

class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True
```

`orm_mode`を指定しなければ、もしあなたが path operation から SQLAlchemy model を返したとしても、**それはrelationshipのデータを含んでいない**だろう.

`orm_mode`を使用する事で, Pydantic 自身が必要なデータを(dict を想定するのではなく)fieldからアクセスしようとするので、返したい特定のデータをdeclareすれば、ORM modelからであってもそれを取りに行くことができるようになる.

## 13.6. CRUD(Create, Read, Update, Delete)用のutilsを用意すると良い...!

/crud.pyを定義する. このファイルでは、Databaseのデータを操作するための再利用可能な関数が用意されている.

### 13.6.1. Read data 用 の utility funcitonを作る.

`sqlalchemy.orm` から `Session` をimportする.
`Session`クラスをtype hintに用いる事で、`db` parameterのtypeをdeclareし、function内でより良いtype check と completion(補完) ができるようになる.

`models` (the SQLAlchemy models) と `schemas` (the Pydantic models / schemas)をimportして、以下のようなutility functionを作成できる.

tips: path operation function とは別に、Databaseとのやり取り(ユーザーやアイテムの取得)だけに特化した関数を作ることで、**より簡単に複数のパーツで再利用でき、unit testも追加しやすい**.(SRP= single responsibility principleだー!!)

```python
from sqlalchemy.orm import Session

from . import models, schemas

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()
```

### 13.6.2. Create date用の utility function を作る.

```python
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(
        **item.dict(), # pydantic modelを一旦dictに変換して、dictをuppackingしてkey-valueをargumentsとして渡している.
        owner_id=user_id,
        )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
```
