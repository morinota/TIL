## title タイトル

Implementing a Stateful Architecture with Streamlit
Streamlitによるステートフル・アーキテクチャの実装

## link リンク

https://towardsdatascience.com/implementing-a-stateful-architecture-with-streamlit-58e52448efa1
https://towardsdatascience.com/implementing-a-stateful-architecture-with-streamlit-58e52448efa1

## Streamlit

Streamlit has come a long way since its inception back in October of 2019.
Streamlitは2019年10月の設立以来、長い道のりを歩んできた。
It has empowered the software development community and has effectively democratized the way we develop and deploy apps to the cloud.
ソフトウェア開発コミュニティに力を与え、クラウドへのアプリ開発とデプロイの方法を事実上民主化した。
However as with all new tools, there is still some way to go, and while the Streamlit team works tirelessly on addressing requests for new features, we developers ourselves can create ad hoc work arounds in the meantime.
Streamlitチームは、新機能のリクエストに対応するためにたゆまぬ努力を続けているが、その間に我々開発者自身がその場しのぎの回避策を作り出すこともできる。

A feature that Streamlit currently lacks, is the ability to implement programmable state for its apps.
Streamlitに現在欠けている機能は、アプリにプログラマブル・ステートを実装する能力だ。
In its current form, there is no internal state that can store volatile data such as user inputs, dataframes and values entered into widgets.
現在の形では、ユーザー入力、データフレーム、ウィジェットに入力された値のような揮発性データを保存できる内部ステートはない。
Given that Streamlit innately re-runs the entire script when the user triggers an action in the event of pressing a button or switching between pages, the app will reset all inputs and dataframes.
Streamlitは、**ユーザーがボタンを押したりページを切り替えたりといったアクションを起こすと、生来的にスクリプト全体を再実行する**ため、アプリはすべての入力とデータフレームをリセットします。
While for many applications, this is a non-issue, for others it can be a deal breaker.
多くの用途では問題ないが、他の用途では破談になることもある。
Just imagine if you are trying to build an app with sequential logic using incremental steps, the absence of a stateful architecture would render Streamlit as an unsuitable framework.
インクリメンタルなステップを使った逐次的なロジックのアプリを作ろうとした場合、ステートフルなアーキテクチャがないため、Streamlitはフレームワークとして適さないだろう.
The founders have committed to releasing a stateful version in the near future, but until then, one can use an open source database such as PostgreSQL to develop a hack as I will explain below.
創設者たちは、近い将来ステートフル・バージョンをリリースすることを約束しているが、それまでは、以下に説明するように、PostgreSQLのようなオープンソースのデータベースを使用してハックを開発することができる。

## PostgreSQL PostgreSQL

PostgreSQL or Postgres for short is a free and open source relational database system that is often the database of choice for most developers due to its ease of use and extended capabilities.
PostgreSQL（略してPostgres）は、フリーでオープンソースのリレーショナル・データベースシステムであり、その使いやすさと拡張機能により、多くの開発者が選択するデータベースとなっている。
While it is ostensibly a structured database management system, it can also store non-structured data such as arrays and binary objects, which makes it rather useful for open-ended projects.
表向きは構造化データベース管理システムだが、配列やバイナリ・オブジェクトのような非構造化データも格納できるので、オープンエンドのプロジェクトにはむしろ便利だ。
In addition, its graphical user interface is highly intuitive and straightforward ensuring that the learning curve is very shallow.
さらに、そのグラフィカル・ユーザー・インターフェースは非常に直感的でわかりやすく、学習曲線は非常に浅い。

In our implementation of a stateful architecture, we will be using a local Postgres server to store our state variables such as the user inputs and dataframes generated in our Streamlit app.
ステートフルアーキテクチャの実装では、Streamlitアプリで生成されたユーザー入力やデータフレームなどの状態変数を保存するために、ローカルのPostgresサーバーを使用します。
Before we proceed, please download and install Postgres using this link.
先に進む前に、このリンクからPostgresをダウンロードしてインストールしてください。
During the installation you will be prompted to configure a username, password and local TCP port to forward your database server to.
インストール中に、ユーザー名、パスワード、およびデータベースサーバーを転送するローカルTCPポートを設定するよう求められます。
The default port is 5432 which you may keep as is.
デフォルトのポートは5432で、そのままでもよい。
Once the installation is completed, you will be able to login to your server by running the ‘pgAdmin 4' application which will then open your server’s portal on your browser as shown below.
インストールが完了したら、'pgAdmin 4'アプリケーションを実行してサーバにログインすることができます。

By default there should also be a database called ‘Postgres’ shown in the left sidebar, if there isn’t however, you may right click on ‘Databases’ and select ‘Create’ to provision a new database.
デフォルトでは、左サイドバーに'Postgres'というデータベースが表示されているはずですが、もし表示されていない場合は、'Databases'を右クリックして'Create'を選択し、新しいデータベースをプロビジョニングしてください。

## Implementation インプリメンテーション

Now that we got the logistics out of the way, lets head over to Python for our implementation.
さて、ロジスティクスは一段落したので、次は実装のためにPythonに向かおう。
Aside from the usual suspects (Pandas and obviously Streamlit itself) you will also need to download the following packages.
通常のパッケージ（PandasとStreamlitそのもの）の他に、以下のパッケージをダウンロードする必要がある。

## Sqlalchemy Sqlalchemy

We will be using this package to create and execute our SQL queries.
このパッケージを使ってSQLクエリーを作成し、実行します。
Sqlalchemy makes it rather simple to write complex queries and if you are passing your query strings as parameters (not concatenated) it has anti-SQL-injection capabilities that ensure your queries are secure.
Sqlalchemy は、複雑なクエリを書くのを簡単にしてくれますし、クエリ文字列を（連結せずに）パラメータとして渡すのであれば、クエリの安全性を保証するアンチSQLインジェクション機能を備えています。
You can download it using the following command.
以下のコマンドでダウンロードできる。

In addition, we will need to import a method called ‘get_report_ctx’ from the Streamlit library.
さらに、Streamlitライブラリから'get_report_ctx'というメソッドをインポートする必要がある。
This function creates a unique session ID every time we run our app.
この関数は、アプリを実行するたびに一意のセッションIDを作成する。
This ID will be associated with each of our state variables to ensure that we are retrieving the correct states from our Postgres database.
このIDは各状態変数に関連付けられ、Postgresデータベースから正しい状態を確実に取得できるようにする。

Proceed by importing the following packages into your Python script.
以下のパッケージをPythonスクリプトにインポートする。

First we will create a function that extracts the session ID of our app instance.
まず、アプリ・インスタンスのセッションIDを抽出する関数を作成する。
Please note that the ID is updated each and every time the app is refreshed i.e.when you hit F5.
IDはアプリが更新されるたびに、つまりF5キーを押すたびに更新されることにご注意ください。
Since the session ID will be used as the name of the tables storing our state variables, we will need to adhere to Postgres’s table naming convention which decrees that names must start with underscores or letters (not numbers), must not contain dashes and must be less than 64 characters long.
セッションIDは状態変数を格納するテーブルの名前として使用されるため、Postgresのテーブル命名規則に従う必要があります。この規則では、名前はアンダースコアまたは文字（数字ではない）で始まり、ダッシュを含まず、64文字未満でなければなりません。

Next we will create four functions that can be used to read and to write the states of our user inputs and dataframes from Streamlit to Postgres as follows.
次に、ユーザー入力とデータフレームの状態をStreamlitからPostgresに読み書きするための関数を以下のように4つ作成する。

Now we will create the main function of our multi-page Streamlit app.
それでは、マルチページStreamlitアプリのメイン関数を作成します。
First we setup the PostgreSQL client using a connection string that contains our username, password and database name.
まず、ユーザー名、パスワード、データベース名を含む接続文字列を使用して、PostgreSQLクライアントをセットアップします。
Please note that a more secure way to store your database credentials is to save them in a configuration file and then to invoke them as parameters in your code.
データベース認証情報をより安全に保存する方法は、設定ファイルに保存し、コードの中でパラメータとして呼び出すことです。
Then we acquire our session ID which should look something along these lines:
次にセッションIDを取得する：

Subsequently, we will create a table with one column called ‘size’ with a datatype of ‘text’ using the current session ID.
続いて、現在のセッションIDを使用して、データ型が'text'の'size'という1つのカラムを持つテーブルを作成します。
We need to ensure that every time our state variable is updated, it is overwritten on the previous state.
ステート変数が更新されるたびに、前のステートに上書きされるようにする必要がある。
Therefore we will query the length of the table and if it is zero we will insert a new row with the state.
したがって、テーブルの長さを照会し、それがゼロであれば、その状態で新しい行を挿入する。
Otherwise we will just update the existing row if a previous state from the current session ID already exists.
そうでなければ、現在のセッションIDの以前の状態がすでに存在する場合、既存の行を更新するだけになります。

Finally we will create two pages that can be toggled using a ‘st.selectbox’ in the sidebar.
最後に、サイドバーの「st.selectbox」を使って切り替えられる2つのページを作ります。
The first page contains the text ‘Hello world’ and the second page contains a text input widget that is used to generate a sparse matrix with the corresponding size specified by the user.
最初のページには'Hello world'というテキストがあり、2番目のページには、ユーザが指定したサイズの疎行列を生成するためのテキスト入力ウィジェットがある。
The state of the text input and generated dataframe is saved into our Postgres database and is queried every time the script is re-run by Streamlit itself.
テキスト入力と生成されたデータフレームの状態はPostgresデータベースに保存され、Streamlit自身がスクリプトを再実行するたびに照会される。
Should the script find an existing state within the same session ID, it will update the input and dataframe accordingly.
スクリプトは、同じセッションID内の既存の状態を見つけると、それに応じて入力とデータフレームを更新します。

## Results 結果

Running the app naturally with a stateless implementation resets the text input and dataframe each time we toggle the page as shown below.
ステートレス実装でアプリを自然に実行すると、以下のようにページを切り替えるたびにテキスト入力とデータフレームがリセットされる。

However, running the app with the stateful implementation achieves a persistent state, whereby the text input and dataframe are being stored and retrieved even after we toggle the pages as shown below.
しかし、ステートフル実装でアプリを実行すると、以下のようにページを切り替えてもテキスト入力とデータフレームが保存・取得され、永続的な状態が実現される。

Concurrently, you can also see that our Postgres database is being updated in real time with our state variable and dataframe as shown below.
同時に、以下のようにPostgresデータベースが状態変数とデータフレームでリアルタイムに更新されていることもわかります。

Any other variable can have its state saved and read with the following commands:
その他の変数は、以下のコマンドで状態を保存したり読み込んだりできる：

Similarly, any dataframe can be saved and read with the following commands:
同様に、どのデータフレームも以下のコマンドで保存したり読み込んだりすることができる：

## Conclusion 結論

This method can be extended to other widgets and can also be used to store binary files that are generated or uploaded to Streamlit.
この方法は他のウィジェットにも拡張でき、Streamlitに生成またはアップロードされたバイナリファイルを保存するためにも使用できます。
In addition, if one would like to track their user’s inputs or would like to record timestamps with each action then this method can be further extended to address such features.
さらに、ユーザーの入力を追跡したり、各アクションのタイムスタンプを記録したい場合は、この方法をさらに拡張して、そのような機能に対応することができる。
The only caveat here is that not all widgets in Streamlit have values that can be stored, for instance, ‘st.button’ serves only as an event trigger and does not have a value associated with it that can be saved as a state.
例えば、'st.button' はイベントトリガーとしてのみ機能し、ステートとして保存できる値を持っていません。

If you want to learn more about data visualization, Python, and deploying a Streamlit web application to the cloud then check out the following (affiliate linked) courses:
データ可視化、Python、クラウドへのStreamlitウェブ・アプリケーションのデプロイについてもっと学びたい方は、以下のコース（アフィリエイトリンク）をチェックしてください：
