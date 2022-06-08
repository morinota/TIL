def main():
    # 標準入力から 1 行読み込む
    s_ori = input().lower()
    # s_ori = "book"
    N = len(s_ori)
    s = " " + s_ori  # indexと文字の順番が一致するように' 'を足す
    # i = 1 ~ len(s)の動的計画法でいけるのでは??

    # DPテーブル
    dp = [{} for _ in range(N + 1)]  # dp[1], dp[2], ... には、それぞれに空のディクショナリーが入っている
    # 「1~nまでの文字列のパターン」をキー, 順位をvalueとするディクショナリー

    # i=1の場合
    dp[1][s[1]] = 1

    # i=2の場合 (パターンは2通り, dp[1].key()の前に入れるか後に入れるか)
    for n in range(2, N + 1):
        dp_n_keys = set()  # ここに「i = nまでの順列の組み合わせ」を格納する
        for dp_n_1_key in dp[n - 1].keys():  # 「i = n-1までの順列の組み合わせ」を一つずつ取り出す.
            # どこにs[n-1:n]を挟みこむか！ len(dp_n_1_key)+1通り?
            for j in range(0, n):
                dp_n_key = dp_n_1_key[:j] + s[n] + dp_n_1_key[j:]
                dp_n_keys.add(dp_n_key)

        # 辞書順にソート
        dp_n_keys = sorted(dp_n_keys, reverse=False)

        # dp[n]にkeyとvalueを格納していく
        rank = 1
        for dp_n_key in dp_n_keys:
            dp[n][dp_n_key] = rank
            rank += 1

    print(dp[N][s_ori])


if __name__ == "__main__":
    main()
