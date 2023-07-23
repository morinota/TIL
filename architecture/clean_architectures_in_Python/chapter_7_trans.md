## link 

https://www.thedigitalcatbooks.com/pycabook-chapter-07/
https://www.thedigitalcatbooks.com/pycabook-chapter-07/

# Chapter 7 - Integration with a real external system - MongoDB 第7章 実際の外部システムとの統合 - MongoDB

There's, uh, another example.
もう1つ例を挙げよう。

Jurassic Park, 1993
[empty]

The previous chapter showed how to integrate a real external system with the core of the clean architecture.
前章では、実際の外部システムをクリーン・アーキテクチャのコアに統合する方法を示した。
Unfortunately I also had to introduce a lot of code to manage the integration tests and to globally move forward to a proper setup.
残念なことに、私は統合テストを管理し、グローバルに適切なセットアップを進めるために多くのコードを導入しなければならなかった。
In this chapter I will leverage the work we just did to show only the part strictly connected with the external system.
[empty]
Swapping the database from PostgreSQL to MongoDB is the perfect way to show how flexible the clean architecture is, and how easy it is to introduce different approaches like a non-relational database instead of a relational one.
データベースをPostgreSQLからMongoDBに入れ替えることは、クリーンなアーキテクチャがいかに柔軟で、リレーショナルデータベースの代わりに非リレーショナルデータベースのような異なるアプローチをいかに簡単に導入できるかを示す完璧な方法だ。

## Fixtures 

Thanks to the flexibility of clean architecture, providing support for multiple storage systems is a breeze.
クリーン・アーキテクチャの柔軟性のおかげで、複数のストレージ・システムのサポートは簡単だ。
In this section, I will implement the class MongoRepo that provides an interface towards MongoDB, a well-known NoSQL database.
[empty]
We will follow the same testing strategy we used for PostgreSQL, with a Docker container that runs the database and docker-compose that orchestrates the whole system.
[empty]

You will appreciate the benefits of the complex testing structure that I created in the previous chapter.
前章で作成した複雑なテスト構造の利点をご理解いただけるだろう。
That structure allows me to reuse some of the fixtures now that I want to implement tests for a new storage system.
[empty]

Let's start defining the file tests/repository/mongodb/conftest.py, which will contains pytest fixtures for MongoDB, mirroring the file we created for PostgreSQL
tests/repository/mongodb/conftest.pyファイルを定義して、PostgreSQL用に作成したファイルをミラーして、MongoDB用のpytestフィクスチャを格納します。

As you can see these functions are very similar to the ones that we defined for Postgres.
見ての通り、これらの関数はPostgres用に定義したものと非常によく似ている。
The function mg_database_empty is tasked to create the MongoDB client and the empty database, and to dispose them after the yield.
mg_database_empty関数は、MongoDBクライアントと空のデータベースを作成し、終了後にそれらを破棄します。
The fixture mg_test_data provides the same data provided by pg_test_data and mg_database fills the empty database with it.
フィクスチャmg_test_dataはpg_test_dataによって提供されるのと同じデータを提供し、mg_databaseは空のデータベースをそれで満たします。
While the SQLAlchemy package works through a session, PyMongo library creates a client and uses it directly, but the overall structure is the same.
SQLAlchemyパッケージがセッションを通して動作するのに対して、PyMongoライブラリはクライアントを作って直接それを使いますが、全体的な構造は同じです。

Since we are importing the PyMongo library we need to change the production requirements
PyMongoライブラリをインポートするので、production requirementsを変更する必要があります。

and run pip install -r requirements/dev.txt.
を実行し、pip install -r requirements/dev.txtを実行する。

## Docker Compose configuration Docker Composeの設定

We need to add an ephemeral MongoDB container to the testing Docker Compose configuration.
テスト用のDocker Compose構成に、エフェメラルなMongoDBコンテナを追加する必要がある。
The MongoDB image needs only the variables MONGO_INITDB_ROOT_USERNAME and MONGO_INITDB_ROOT_PASSWORD as it doesn't create any initial database.
MongoDB イメージは初期データベースを作成しないので、 MONGO_INITDB_ROOT_USERNAME と MONGO_INITDB_ROOT_PASSWORD 変数だけが必要です。
As we did for the PostgreSQL container we assign a specific port that will be different from the standard one, to allow tests to be executed while other containers are running.
PostgreSQLコンテナで行ったように、他のコンテナの実行中にテストを実行できるように、標準とは異なる特定のポートを割り当てる。

## Application configuration アプリケーションの設定

Docker Compose, the testing framework, and the application itself are configured through a single JSON file, that we need to update with the actual values we want to use for MongoDB
Docker Compose、テストフレームワーク、アプリケーション自体は、1つのJSONファイルで設定されます。

Since the standard port from MongoDB is 27017 I chose 27018 for the tests.
MongoDBの標準ポートは27017なので、テストには27018を選んだ。
Remember that this is just an example, however.
ただし、これはあくまでも一例であることをお忘れなく。
In a real scenario we might have multiple environments and also multiple setups for our testing, and in that case we might want to assign a random port to the container and use Python to extract the value and pass it to the application.
実際のシナリオでは、テスト用に複数の環境と複数のセットアップがあるかもしれない。そのような場合、コンテナにランダムなポートを割り当て、Pythonを使って値を抽出してアプリケーションに渡したいかもしれない。

Please also note that I chose to use the same variable APPLICATION_DB for the name of the PostgreSQL and MongoDB databases.
また、PostgreSQLとMongoDBのデータベース名には、同じ変数APPLICATION_DBを使うことにしました。
Again, this is a simple example, and your mileage my vary in more complex scenarios.
繰り返しになるが、これは単純な例であり、もっと複雑なシナリオの場合は、走行距離も変わってくる。

## Integration tests 統合テスト

The integration tests are a mirror of the ones we wrote for Postgres, as we are covering the same use case.
統合テストは、同じユースケースをカバーしているため、Postgres用に書いたものをミラーしている。
If you use multiple databases in the same system you probably want to serve different use cases, so in a real case this might probably be a more complicated step.
同じシステムで複数のデータベースを使用する場合、おそらく異なるユースケースに対応したいだろうから、実際のケースではもっと複雑なステップになるかもしれない。
It is completely reasonable, however, that you might want to simply provide support for multiple databases that your client can choose to plug into the system, and in that case you will do exactly what I did here, copying and adjusting the same test battery.
しかし、クライアントがシステムに接続するために選択できる複数のデータベースのサポートを単純に提供したい場合もあり、その場合は、私がここで行ったのとまったく同じように、同じテスト・バッテリーをコピーして調整することになる。

I added a test called test_repository_list_with_price_as_string that checks what happens when the price in the filter is expressed as a string.
test_repository_list_with_price_as_stringというテストを追加し、フィルター内の価格が文字列として表現された場合にどうなるかをチェックするようにした。
Experimenting with the MongoDB shell I found that in this case the query wasn't working, so I included the test to be sure the implementation didn't forget to manage this condition.
MongoDBシェルで実験してみると、この場合はクエリが機能していないことがわかったので、実装がこの条件を管理するのを忘れていないことを確認するためにテストを入れた。

## The MongoDB repository MongoDBリポジトリ

The MongoRepo class is obviously not the same as the Postgres interface, as the PyMongo library is different from SQLAlchemy, and the structure of a NoSQL database differs from the one of a relational one.
PyMongoライブラリはSQLAlchemyとは異なりますし、NoSQLデータベースの構造はリレーショナルデータベースとは異なります。
The file rentomatic/repository/mongorepo.py is
rentomatic/repository/mongorepo.pyファイルは次のとおりです。

which makes use of the similarity between the filters of the Rent-o-matic project and the ones of the MongoDB systemfootnote:[The similitude between the two systems is not accidental, as I was studying MongoDB at the time I wrote the first article about clean architectures, so I was obviously influenced by it.].
Rent-o-maticプロジェクトのフィルターとMongoDBシステムのフィルターの類似性を利用したものである。

I think this very brief chapter clearly showed the merits of a layered approach and of a proper testing setup.
この非常に短い章は、レイヤーアプローチと適切なテストセットアップのメリットを明確に示したと思う。
So far we implemented and tested an interface towards two very different databases like PostgreSQL and MongoDB, but both interfaces are usable by the same use case, which ultimately means the same API endpoint.
これまでのところ、私たちはPostgreSQLとMongoDBのような全く異なる2つのデータベースに対するインターフェースを実装し、テストしてきたが、どちらのインターフェースも同じユースケースで使用可能であり、最終的には同じAPIエンドポイントを意味する。

While we properly tested the integration with these external systems, we still don't have a way to run the whole system in what we call a production-ready environment, that is in a way that can be exposed to external users.
これらの外部システムとの統合をきちんとテストしたとはいえ、私たちがプロダクション・レディ環境と呼ぶ、外部ユーザーに公開できる形でシステム全体を稼働させる方法はまだない。
In the next chapter I will show you how we can leverage the same setup we used for the tests to run Flask, PostgreSQL, and the use case we created in a way that can be used in production.
次の章では、テストに使ったのと同じセットアップを活用して、Flask、PostgreSQL、そして作成したユースケースを本番で使えるように実行する方法を紹介する。