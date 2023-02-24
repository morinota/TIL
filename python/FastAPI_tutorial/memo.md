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

### 1.1.3. Step 3：path operationを作成(宣言)

- ここでの"path"とは、最初の`/`から始まるURLの最後の部分.
  - ex) `https://example.com/items/foo`の場合、pathは`/items/foo`.
  - pathは一般に、**"endpoint"または"root"**とも呼ばれる.
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

ここで、operation=`get`, path=`/`, `root()`はpath operation function.
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

### 4.4. request body parameterの各要素に対して、`pydantic.Field`で設定をdeclareする.

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

### request body parameterのnested化

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

### `List[submodel]`をrequest body parameterのfieldとして期待するケース

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

# 特殊なdata typeとvalidationについて

str、int、float などの通常の単数型とは別に str を継承した、より複雑な**singular data types**を使用できる.

どのようなsingular data typesがあるかは、Pydanticの**exotic types**に関するドキュメントを参照してください. いくつかの例をあげる.

## `pydantic.HttpUrl`

```python
class Image(BaseModel):
    url: HttpUrl
    name: str
```
