# 配列から目的の値を探索する二分探索法 (計算量は log N)
def binary_search(array: list[int], key: int) -> int:
    """目的の値 key の添字(index)を返す"""
    left, right = 0, len(array) - 1  # 配列の両端のidx
    while right >= left:
        mid = int((left + right) / 2)
        if key == array[mid]:
            return mid
        elif key < array[mid]:
            right = mid - 1  # 配列の左半分のみ残す
        elif key > array[mid]:
            left = mid + 1  # 配列の右半分のみ残す
    else:
        return -1


def main() -> None:
    N = 8
    sample_input = [3, 5, 8, 10, 14, 17, 21, 39]
    print(binary_search(sample_input, 10))  # 3
    print(binary_search(sample_input, 3))  # 0
    print(binary_search(sample_input, 39))  # 7

    print(binary_search(sample_input, -100))  # -1
    print(binary_search(sample_input, 9))  # -1
    print(binary_search(sample_input, 100))  # -1


if __name__ == "__main__":
    main()
