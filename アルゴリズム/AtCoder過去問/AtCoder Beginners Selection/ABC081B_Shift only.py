# 問題文

# input関数をint関数で囲み、整数値として変数Nに設定
N = int(input())
# input().split()で空白区切りの文字列を取得 → intに変換 → list関数で囲み、リストとしてAに設定
A = list(map(int, input().split()))

# 終了判定用のフラグ
flag = 0
# 2で割れた回数をカウントする変数※以下ではカウンタと呼びます
count = 0

while True:
    # 0~N-1までのN回forループ処理を行う
    for i in range(N):
        # Aのi番目A[i]が2で割れない場合
        if A[i] % 2 !=0:
            # 終了フラグに1を設定する
            flag = 1

    # 終了フラグが立つ(1)の場合
    if flag ==1:
        # break文で処理を終了する
        break

    # 0~N-1までのN回forループ処理を行う
    for i in range(N):
        # Aのi番目であるA[i]を2で割ったものをA[i]に再設定
        A[i] = A[i]//2
    
    # 全て割れたのでカウンタに1プラスする
    count += 1
# 操作総数を表示する
print(count)