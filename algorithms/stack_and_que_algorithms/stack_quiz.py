"""
Input {'key1': 'value1', 'key2': [1, 2, 3], 'key3': (1, 2, 3)}  Output True
Input [{'key1': 'value1', 'key2': [1, 2, 3], 'key3': (1, 2, 3)} Output False
- Inputされるjsonの中で、全ての鍵かっこが正しく開いて閉じているか確認せよ。
- カギカッコはカーリーブラケット{}もスクエアブラケット[]もラウンドブラケット()も対象。

- 開くブラケットが出てきたら、閉じる方}をスタックに積んでいく。
- 今度は閉じるブラケットが出てきたら、スタックの中に入っているかどうかを判定する. pop で取り出して消してやる。
- 最後、きれいにスタックが空になったらTrueと判定していく。

- Stackなら以下のような場合のFalseも、データ構造に落とし込んで対応できる
- ([)]のような対の形があってもFalse
- いきなり]が来た場合もFalse

- コード自体は簡単。
- 質問内容をどのようにアプローチするか。どういったケースでFalseになるのか。
↑を頭の中で整理できるかどうかがkeyになる。
- アイデアの話。こういった問題が出た時に思い出してもらえたら。
"""


def validate_format(chars: str) -> bool:
    lookup = {"{": "}", "[": "]", "(": ")"}  # dictでブラケットのセットを管理していく
    stack = []  # python のライブラリでquuというものがあるが、今回は簡単にListで
    for char in chars:
        if char in lookup:
            stack.append(lookup[char])
        if char in lookup.values():
            if not stack:
                return False  # stackが空なのに、閉ブラケットが出現したケース
            if char != stack.pop():
                return False  # stackの上から取り出した値が、対象の閉ブラケットと異なっているケース

    if stack:
        return False  # 最後、stackに中身が残っていたら...

    return True  # 最後、stackがきれいに空になったら


if __name__ == "__main__":
    json = "{'key1': 'value1', 'key2': [1, 2, 3], 'key3': (1, 2, 3)}"
    json = "]{'key1': 'value1', 'key2': [1, 2, 3], 'key3': (1, 2, 3)}"
    json = "{'key1': ['value1', 'key2': [1, 2, 3], 'key3': (1, 2, 3)}"
    json = "{'key1': 'value1', 'key2': [1, 2, 3], 'key3': (1, 2, 3)}["
    print(validate_format(json))
