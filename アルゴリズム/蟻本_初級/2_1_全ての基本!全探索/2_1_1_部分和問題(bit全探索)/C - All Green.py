# https://atcoder.jp/contests/abc104/tasks/abc104_c

D, G = map(int, input().split())
p, c = [0] * D, [0] * D
for i in range(D):
    p[i], c[i] = map(int, input().split())


# 各難易度i(i=1~D)に対して、p_i個の問題(各問題の配点は100*i点)
# 難易度iの問題を全問正解だと、さらにボーナスc_i点追加
# 総合スコアがG点以上になるには、少なくとも何問、正解する必要があるか。
# 各問題に関して、「正解or不正解の２択」＝＞2^nの探索＝＞bit全探索

# ただ実際には、各難易度に対して「全問正解するか否か」を２進数で表し、bit全探索
# =>点数がG未満ならば、全問正解してない難易度の中で、一番点数の高い問題を解き、G以上になるかを確かめる。
# つまり、bit全探索とgreedyの合せ技。
# 確かに、各問題に対するbit全探索だと、計算量が爆発しちゃうか...

# 選択肢の数(難易度の数)
option_count = D


count_min = 1e9  # 解答の初期値(とりあえずめちゃ大きい数に)

for i in range(2**option_count):  # 2^n通りのoptionがある。bit全探索
    total_score_i = 0
    count_i = 0

    # i番目のoptionの初期値を設定(全問正解=1 or not=0)
    option_i = [""] * option_count
    # i番目のoptionに関して、各難易度の0 or 1を取得
    for j in range(option_count):
        if (i >> j) & 1:  # もし左からj桁目が1だったら...
            # トータルスコアと解答数を記録
            total_score_i += (p[j] * 100 * (j + 1)) + c[j]
            count_i += p[j]

    # total_scoreがGを超えていれば...
    if total_score_i >= G:
        # その時の回答数(1の数)を比較してcontinue
        count_min = min(count_min, count_i)
        continue

    # Gを超えてない場合は...
    else:
        # コンプリートしていない問題の中で一番点数の高い問題を解き、G以上になるかを確かめる。
        # Gを超えない状態でcount >= count_minとなればその時点でbreak
        j = D - 1  # 一番点数の高い問題から確認
        while (total_score_i < G) and (count_i < count_min):
            if (i >> j) & 1:  # すでに全完の難易度ならcontinue
                pass
            else:
                # まだ未完の難易度であれば...
                for _ in range(p[j] - 1):  # 難易度jの問題数-1だけループ
                    total_score_i += 100 * (j + 1)
                    count_i += 1
                    if total_score_i >= G:
                        # その時の回答数(1の数)を比較してbreak
                        count_min = min(count_min, count_i)
                        break
                    elif count_i >= count_min:
                        break

            # １段低い難易度へ
            j -= 1
            # 最低難易度まで解いてもダメだったら、このOptionではクリアできない。
            if j == -1:
                break

print(count_min)
