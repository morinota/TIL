"""簡単なheapを使ったクイズ
- pythonのライブラリheapq: heapを扱える
- heappush, heappopなど. 
- heapify関数:リストを渡すとheapにしてくれる
- この辺りを確認してから簡単なクイズへ
- pythonではbinary search treeの組み込みライブラリはない.
    - listやdictがあるので、不要.
- heapqに関しては、なにかのランキングからminimumなものを取ってきたりと、需要がある。->組み込みライブラリ
"""

import heapq
from collections import Counter
from typing import List

numbers = [1, 3, 5, 7, 9, 2, 4, 6, 8, 0]
heap_data = []  # ↑をheapの形にしたい

heapq.heapify(numbers)  # いちいちheap_dataを作ってpushしなくても良い
print(numbers)

# for num in numbers:
#     heapq.heappush(heap_data, num)  # heapにnumをpushしていく

# print(heap_data)

# while heap_data:
#     print(heapq.heappop(heap_data))  # heapからvalueをpopしていく

"""他の関数も確認していく"""

print(heapq.nlargest(3, numbers))  # maxからn個
print(heapq.nsmallest(3, numbers))  # minからn個

"""quiz
wordsの中で、最も多く出現するn個のランキングをheapを使って出してください.
その際、nlargestやnsmallestは使わないでください。
heapify, heappush, heappopは使ってもOK.
ヒント:tupleもheapを使える
"""


def top_n_with_heap(words: List[str], n: int) -> List[str]:
    """
    - (min)heapの場合は一番小さい数字が上に来る.
    - 今回はpopで答えを取り出してみたい.
    - -> pythonの出現回数3回を-3として、一番上に来るようにしたい.

    """
    # counter_words = {}
    # for word in words:
    #     # keyを指定してvalueが空だとエラーになるので、getで値の有無を確かめる,なければ0を返す
    #     counter_words[word] = counter_words.get(word, 0) + 1  # 出現カウントを+1してやる
    # print(counter_words)
    counter_words = Counter(words)
    # print(counter_words.most_common(n)) # こういうやり方もある。今回はheapで.

    data = [(-counter_words[word], word) for word in words]  # (-出現回数, word)のタプルを得る

    return [heapq.heappop(data)[1] for _ in range(n)]  # n回popしたvalueのstrの方をlistに格納


if __name__ == "__main__":
    words = ["python", "c", "java", "go", "python", "c", "go", "python"]
    print(top_n_with_heap(words, n=3))
