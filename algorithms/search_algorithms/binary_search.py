"""
- 今度は既にソートされたものから、特定の数字を探し出す(サーチ)の部分
- 先頭から見ていく: LInear Search
    - 後ろにあったら時間がかかる
- binary searchを使うと、速くサーチできる。
    - L(left)のR(right)のindexを足し合わせて、2で割ったものをM(middle)
    - いきなり、まずは真ん中Mを見る
    - Mのnumが探し出したい数字(target_num)よりも小さい場合、target_numはMよりも右側にある
        =>L=M+1に移動させて、今度は右側のMを更に見る。
    - どんどん真ん中にジャンプしていく。検索が速くなる。＝＞Binary Search
"""

from typing import List


def linear_search(numbers: List[int], target_num: int) -> int:
    for i in range(0, len(numbers)):
        if numbers[i] == target_num:
            return i

    return -1  # もし見つからなかったら-1を返す


class BinarySearch:
    def __init__(self) -> None:
        pass

    def search_with_while(self, numbers: List[int], target_num: int) -> int:
        """binary_search(while文ver). numbersは昇順でソートされている前提"""
        left_idx, right_idx = 0, len(numbers) - 1

        while left_idx <= right_idx:
            print("###############")
            # LとRの間がどんどん狭くなっていく
            # target_numが見つからなかったら、最終的にLとRの前後関係が入れ替わる
            mid_idx = (left_idx + right_idx) // 2
            if numbers[mid_idx] == target_num:
                return mid_idx
            elif numbers[mid_idx] < target_num:
                left_idx = mid_idx + 1  # LをMの右隣に移動させる
            else:
                right_idx = mid_idx - 1  # RをMの左隣に移動させる

        return -1

    def search_with_inner(self, numbers: List[int], target_num: int) -> int:
        """binary_search(inner関数というかprivateメソッドを使って再起的に実行するver). numbersは昇順でソートされている前提"""
        return self._search_with_inner(
            numbers,
            target_num,
            left_idx=0,
            right_idx=len(numbers) - 1,
        )  # 再起関数のエントリーポイント

    def _search_with_inner(
        self,
        numbers: List[int],
        target_num: int,
        left_idx: int,
        right_idx: int,
    ) -> int:
        print("###############")

        if left_idx > right_idx:
            return -1

        mid_idx = (left_idx + right_idx) // 2
        if numbers[mid_idx] == target_num:
            return mid_idx
        elif numbers[mid_idx] < target_num:
            return self._search_with_inner(
                numbers,
                target_num,
                left_idx=mid_idx + 1,  # LをMの右隣に移動させる
                right_idx=right_idx,
            )
        else:
            return self._search_with_inner(
                numbers,
                target_num,
                left_idx=left_idx,
                right_idx=mid_idx - 1,  # LをMの右隣に移動させる
            )


if __name__ == "__main__":
    nums = [0, 1, 5, 7, 9, 11, 15, 20, 24]
    print(linear_search(nums, target_num=15))
    print(BinarySearch().search_with_while(nums, target_num=15))
    print(BinarySearch().search_with_inner(nums, target_num=15))
