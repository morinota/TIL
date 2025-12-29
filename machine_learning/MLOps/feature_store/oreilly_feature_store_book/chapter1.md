# Chapter 1: Building Machine Learning Systems
# 第1章：機械学習システムの構築

Imagine you have been tasked with producing a financial forecast for the upcoming financial year.
来年度の財務予測を作成するタスクを任されたと想像してください。

You decide to use machine learning (ML), as there is a lot of available data, but, not unexpectedly, the data is spread across many different places—in spreadsheets and many different tables in the data warehouse.
多くのデータが利用可能であるため、機械学習（ML）を使用することにしましたが、案の定、データはスプレッドシートやデータウェアハウス内の多数の異なるテーブルなど、多くの異なる場所に分散しています。

This example shows the difference between training a model to make a one-off prediction on a static dataset and building a batch ML system—a system that automates reading from data sources, transforming data into features, training models, performing inference on new data with the model, and updating a dashboard with the model’s predictions.
この例は、静的なデータセットで一度限りの予測を行うためにモデルをトレーニングすることと、データソースからの読み込み、データを特徴量へ変換すること、モデルのトレーニング、モデルを使用した新しいデータに対する推論の実行、そしてモデルの予測によるダッシュボードの更新を自動化するシステムである「バッチMLシステム」を構築することの違いを示しています。

## The Anatomy of a Machine Learning System
## 機械学習システムの解剖学

We can categorize ML systems by how they process the new data that is used to make predictions.
予測を行うために使用される新しいデータをどのように処理するかに基づいて、MLシステムを分類することができます。

Does the ML system make predictions on a schedule (for example, once per day), or does it run 24/7, making predictions in response to user requests?
MLシステムはスケジュール（例えば1日1回）に基づいて予測を行うか、それとも24時間365日稼働し、ユーザーのリクエストに応じて予測を行うでしょうか？

### Batch ML Systems
### バッチMLシステム

Spotify’s Discovery Weekly is an example of a batch ML system, which is a recommendation engine that, once per week, predicts which songs you might want to listen to and adds them to your playlist.
SpotifyのDiscovery WeeklyはバッチMLシステムの一例であり、週に1回、あなたが聴きたいと思われる曲を予測し、プレイリストに追加するレコメンデーションエンジンです。

### Real-time ML Systems
### リアルタイムMLシステム

TikTok’s recommendation engine, on the other hand, is famous for adapting its recommendations in near real time as you click and watch its short-form videos.
一方、TikTokのレコメンデーションエンジンは、ショート動画をクリックして視聴するたびに、ほぼリアルタイムで推奨内容を適応させることで有名です。

TikTok’s recommendation service is a real-time ML system. It predicts which videos to show you as you scroll and watch videos.
TikTokのレコメンデーションサービスは、リアルタイムMLシステムです。スクロールして動画を視聴する際に、どの動画を表示すべきかを予測します。

### Agentic AI Systems
### エージェンティック（自律型）AIシステム

Lovable is an agentic AI system that takes your instructions and uses an LLM to create and run your web application as TypeScript code along with CSS styling and an optional integrated database.
Lovableは、あなたの指示を受け取り、LLMを使用してWebアプリケーションをTypeScriptコード、CSSスタイリング、およびオプションの統合データベースとして作成・実行するエージェンティックAIシステムです。

Agentic systems have natural language interfaces. You give them a high-level goal or task to execute, and they work with a high degree of autonomy to achieve your goal or task.
エージェンティックシステムは自然言語インターフェースを持っています。高レベルの目標や実行すべきタスクを与えると、それらは高度な自律性を持って目標やタスクを達成しようとします。

## A Brief History of Machine Learning Systems
## 機械学習システムの簡潔な歴史

### Feature Stores
### フィーチャーストア

The general problem of building stateful online ML systems was first addressed by feature stores, which were introduced as a new category of platform by Uber in 2017, with their article on their internal Michelangelo platform.
ステートフルなオンラインMLシステムを構築するという一般的な課題は、2017年にUberが社内のMichelangeloプラットフォームに関する記事で新しいカテゴリのプラットフォームとして紹介した「フィーチャーストア」によって最初に対処されました。

Feature stores manage the transformation and storage of context and history as features that can be easily used by online models.
フィーチャーストアは、オンラインモデルが容易に使用できるように、コンテキストや履歴の変換と保存を「特徴量」として管理します。

### From LLMs to Agents
### LLMからエージェントへ

The first RAG-powered LLM applications took the user input as a string and queried a vector database with the input string, returning chunks of text similar to the input using approximate nearest neighbor (ANN) search.
最初のRAG（検索拡張生成）を活用したLLMアプリケーションは、ユーザー入力を文字列として受け取り、その入力文字列を使ってベクトルデータベースにクエリを投げ、近似最近傍（ANN）探索を用いて入力に類似したテキストのチャンクを返していました。

As LLM applications took on increasingly complex tasks, they required more autonomy in what data to query and what tasks to execute.
LLMアプリケーションがますます複雑なタスクを担うようになるにつれ、どのデータを照会し、どのタスクを実行するかについて、より高い自律性が求められるようになりました。

Agents are a class of LLM application that have a level of autonomy in how to query diverse data sources (vector indexes, search engines, feature stores, etc.) to retrieve relevant context data and how to plan and execute tasks to achieve goals.
エージェントは、関連するコンテキストデータを取得するために多様なデータソース（ベクトルインデックス、検索エンジン、フィーチャーストアなど）をどのように照会するか、そして目標を達成するためにどのようにタスクを計画・実行するかについて、ある程度の自律性を持つLLMアプリケーションの一種です。

## A Unified Architecture for AI Systems: Feature, Training, and Inference Pipelines
## AIシステムのための統一アーキテクチャ：特徴量、トレーニング、および推論パイプライン

Luckily, we can do better. There is a unified architecture for developing all AI systems that follows a natural decomposition of any AI system into feature creation, model training, and inference pipelines.
幸いなことに、もっと良い方法があります。あらゆるAIシステムを、特徴量作成、モデルトレーニング、および推論パイプラインへと自然に分解することに従った、すべてのAIシステムを開発するための統一アーキテクチャが存在します。

The three different ML pipelines have clear inputs and outputs and can be developed, tested, and operated independently:
3つの異なるMLパイプラインは明確な入力と出力を持ち、独立して開発、テスト、運用することができます：

*   **Feature pipelines**: These take data as input and produce reusable feature data as output.
    **特徴量パイプライン**: データを入力として受け取り、再利用可能な特徴量データを出力として生成します。

*   **Training pipelines**: These take feature data as input, train a model, and output the trained model.
    **トレーニングパイプライン**: 特徴量データを入力として受け取り、モデルをトレーニングし、トレーニング済みモデルを出力します。

*   **Inference pipelines**: These take feature data and a model as inputs, and they output predictions and prediction logs.
    **推論パイプライン**: 特徴量データとモデルを入力として受け取り、予測と予測ログを出力します。

We can now define an AI system as a set of independent feature pipelines, training pipelines, and inference pipelines that are connected via a feature store and model registry.
これで、AIシステムを、フィーチャーストアとモデルレジストリを介して接続された独立した特徴量パイプライン、トレーニングパイプライン、推論パイプラインのセットとして定義できます。
