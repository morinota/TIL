# 年齢当てゲーム_二分探索法ver
# 初対面のAさんの年齢を当てたい。Aさんの年齢は20歳以上３６歳未満である事はわかっている。
# Aさんに4回までYes/Noで答えられる質問ができる。


def is_more_than(age: int) -> bool:
    correct_age = 30
    return correct_age >= age
    # 年齢が渡したage以上ならTrueを返す。


def main() -> None:
    # Aさんの年齢候補を表す区間を [left, right)と表す。
    left, right = 20, 36

    # Aさんの数を1つに絞れないうちは繰り返す。
    while right - left > 1:
        mid = int((left + right) / 2)

        # mid以上かを聴いて、回答をTrue/Falseで受け取る。
        is_Yes = is_more_than(mid)
        if is_Yes:
            left = mid  # 配列の右半分のみ残す
        else:
            right = mid  # 配列の左半分のみ残す

    print(left)  # CORRECT_AGE


if __name__ == "__main__":
    main()
