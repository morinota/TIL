# input関数をint関数で囲み、整数値として変数Nに設定
N = int(input())
# input().split()で空白区切りの文字列を取得 → intに変換 → list関数で囲み、リストとしてAに設定
A = list(map(int, input().split()))

# 実際に操作をシミュレーションしないVer.
# 以下の様に考える。
