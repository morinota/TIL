# Chapter 4. Our First Use Case: Flask API and Service Layer 第4章 私たちの最初のユースケース。 Flask APIとサービスレイヤー

図4-1は、Repositoryパターンを扱った第2章の終わりで到達した地点.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0401.png)

この章では、**orchestration logic**, **business logic**, **interfacing code** の違いについて説明し、ワークフローの orchestration とシステムのユースケース(??)を定義するための **Service Layer**パターンを紹介する.

**Service Layer Patternと Repository Pattern (データベースを抽象化したリポジトリ) を組み合わせる**ことで、ドメインモデルだけでなく、ユースケースのワークフロー全体のテストを高速に記述することができる.

図4-2は、私たちが目指しているものを示す.
Service Layer と対話するFlask APIを追加し、ドメインモデルへの**エントリポイント**として機能させるつもり.
サービスレイヤーは `AbstractRepository` に依存しているので、 `FakeRepository` を使ってユニットテストを行い、 `SqlAlchemyRepository` を使ってプロダクションコードを実行することができる.

(domain Model -> databaseの依存関係を無くす為に使用したのが Repository Pattern. なので恐らく、**domain model -> Flask(ひいてはクライアント側?)の依存関係を無くす為に使用**するのが Service Layer Pattern ?)

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0402.png)

## Connecting Our Application to the Real World 私たちのアプリケーションを実世界につなげるために

chapter 1 ~ 2で、Domain model のコアと、注文を割り当てるために必要なdomain service 、そして永久保存のための repository interface を手に入れた.

すべての可動部をできるだけ早く接続し、よりクリーンなアーキテクチャに向けてリファクタリングしていく.

1. Flaskを使って、APIエンドポイントを `allocate` ドメインサービスの前に配置する. データベースセッションとリポジトリの配線。 エンドツーエンドテストと、テストデータを準備するためのクイックアンドダーティなSQLでテスト.
2. ユースケースを抽象化し、Flaskとドメインモデルの間に位置するサービスレイヤーをリファクタリングする. サービスレイヤーのテストをいくつか作って、それらがどのように `FakeRepository` を使うことができるかを示す.
3. プリミティブな(=build-inの)データ型を使うことで、サービス層のクライアント（テストとFlask API）をモデル層から切り離すことができることを示す.

## A First End-to-End Test 最初のエンド・ツー・エンド・テスト


