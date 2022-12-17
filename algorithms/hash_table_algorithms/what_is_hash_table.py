"""ハッシュテーブルとは何か
- 
"""
import hashlib
from typing import Any


class HashTable(object):
    def __init__(
        self,
        idx_size: int = 10,
    ) -> None:
        """
        - keyの数によって、indexの数も変化させていく事が必要
        -
        """
        self.idx_size = idx_size
        self.tables = [[] for _ in range(self.idx_size)]  # 今回はListで管理する

    def hash_function(self, key: str) -> int:
        """keyを受け取って、index番号を返す
        今回はhashlibのmd5を使う
        """
        hash_object = hashlib.md5(key.encode())  # keyをbinaryにしてmd5に渡してやる.
        hash_str = hash_object.hexdigest()  # =>hexdigestでhash objectをhashの文字列へ(これは"car"に対して一意に定まった値, 16進数)
        hash_int = int(hash_str, base=16)  # 16進数 -> 10進数のintへ
        return hash_int % self.idx_size  # hash_intを10個のグループに分類する=割る10の余りを使う

    def add_to_table(self, key: str, value: Any) -> None:
        """tableに値を追加する"""
        key_idx = self.hash_function(key)
        # データの重複を避ける仕組み
        for data in self.tables[key_idx]:
            if data[0] == key:
                data[1] = value  # valueを上書き
                break
        else:  # 途中でbreakせずに終了したら新規登録
            self.tables[key_idx].append([key, value])

    def print(self) -> None:
        """各テーブルのコンソール出力を見やすくする"""
        for idx in range(self.idx_size):
            print(idx, end=" ")  # end=" "にする事で改行しないようにする.じゃあdefaultは"\n"?
            for data in self.tables[idx]:
                print("-->", end=" ")
                print(data, end=" ")

            print()

    def get(self, key: str) -> Any:
        """keyを受け取りvalueを返す"""
        key_idx = self.hash_function(key)  # 索引をたどる
        for data in self.tables[key_idx]:  # 第key_idx章でページを1枚ずつめくっていく
            if data[0] == key:
                return data[1]

    """以下で、実際のpythonのdictと呼び出し方を揃える
    """

    def __setitem__(self, key: str, value: Any) -> None:
        """HashTable[key] = valueの呼び出し方をされた時に実行される"""
        self.add_to_table(key, value)

    def __getitem__(self, key: str) -> Any:
        """同様にgetも. HashTable[key] の呼び出し方をされた時に実行される。"""
        return self.get(key)


if __name__ == "__main__":
    hash_table = HashTable()
    hash_table.add_to_table(key="car", value="Tesla")
    hash_table.add_to_table(key="car", value="Toyota")
    hash_table.add_to_table(key="pc", value="Mac")
    hash_table.add_to_table(key="sns", value="Youtube")
    hash_table["hoge"] = "hogehoge"

    hash_table.print()
