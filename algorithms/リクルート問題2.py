import itertools


def main():
    # 標準入力から 1 行読み込む
    s= input()
    N = len(s)
    all_patterns = set(itertools.permutations(s)) # 重複なし順列を取得W
    all_patterns = [''.join(each_pattern) for each_pattern in all_patterns] # List[Tupple] =>List[str]

    all_patterns.sort(reverse=False)
    
    ans = 0
    for i, each_patten in enumerate(all_patterns):
        if each_patten == s:
            ans = i+1
            break
    # 標準出力に答えを 1 行で出力
    print(ans)

if __name__ == '__main__':
    main()