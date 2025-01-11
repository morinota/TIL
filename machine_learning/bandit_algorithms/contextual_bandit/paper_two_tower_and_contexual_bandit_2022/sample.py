from typing import Callable

import numpy as np


def two_stage_exploration_framework(
    users: list[int],  # ユーザーのリスト
    topics: list[int],  # トピックのリスト
    topic_to_news: dict[int, list[int]],  # 各トピックに関連付けられたニュースの辞書
    alpha_1: Callable[[int, int], float],  # トピックのUCBスコア取得関数
    alpha_2: Callable[[int, int], float],  # ニュースのUCBスコア取得関数
    m: int,  # 一回のiterationで推薦するアイテムの数
    N: int,  # シミュレーションの繰り返し数
):
    # 初期化
    for t in range(N):
        user = np.random.choice(users)  # ランダムにユーザーを選択
        S_rec = []  # 推薦セットを初期化

        # --- Stage One: トピック推薦 ---
        topic_scores = [(v, alpha_1(user, v)) for v in topics]  # 各トピックのUCBスコアを計算
        topic_scores.sort(key=lambda x: x[1], reverse=True)  # スコアで降順にソート

        # 上位 m 個のトピックを選択
        selected_topics = [v for v, _ in topic_scores[:m]]

        # 動的トピックセット再構築（必要に応じて推薦候補トピックを拡張）
        # ex. 世間的に話題になってるトピックとか?? :thinking:
        dynamic_topics = {v: topic_to_news[v] for v in selected_topics}

        # --- Stage Two: ニュース推薦 ---
        for topic, news_list in dynamic_topics.items():
            news_scores = [
                (news, alpha_2(user, news)) for news in news_list
            ]  # 選ばれたトピックについて、各ニュースのUCB取得スコアを計算
            news_scores.sort(key=lambda x: x[1], reverse=True)  # UCB取得スコアの降順にソート

            # 最も高スコアのニュース1つを選択して、推薦ニュースセットに追加
            if news_scores:
                best_news = news_scores[0][0]
                S_rec.append(best_news)

        # 推薦ニュースセットをユーザーに提示し、フィードバックを取得
        feedback = oracle(user, S_rec)  # oracle関数はクリック（1）または非クリック（0）を返す関数

        # モデルを更新(たぶん実務上は、time stepごとに毎回更新するのではなく、定時バッチで更新する感じになりそう??)
        update_models(user, S_rec, feedback)


# oracle: ユーザーと推薦セットに基づきフィードバックを返す関数（クリック/非クリック）
def oracle(user: int, S_rec: list[int]) -> dict[int, int]:
    # サンプル実装: ランダムにクリックを返す（実際にはデータセットが必要）
    return {item: np.random.choice([0, 1]) for item in S_rec}


# モデル更新の関数（サンプル）
def update_models(user: int, S_rec: list[int], feedback: dict[int, int]):
    # フィードバックに基づいてモデルを更新（具体的な実装はアプリケーション依存）
    for item, reward in feedback.items():
        print(f"User {user}: News {item} -> Feedback: {reward}")


# テスト用のパラメータ
users = list(range(100))  # ユーザーID（例: 0〜99）
topics = list(range(20))  # トピックID（例: 0〜19）
topic_to_news = {v: list(range(v * 10, (v + 1) * 10)) for v in topics}  # 各トピックに関連付けるニュース


# サンプルの取得関数（ランダムスコアを返す）
def sample_alpha_1(user: int, topic: int) -> float:
    return np.random.random()


def sample_alpha_2(user: int, news: int) -> float:
    return np.random.random()


# 実行
two_stage_exploration_framework(
    users=users,
    topics=topics,
    topic_to_news=topic_to_news,
    alpha_1=sample_alpha_1,
    alpha_2=sample_alpha_2,
    m=5,  # 推薦数
    N=10,  # シミュレーション回数
)
