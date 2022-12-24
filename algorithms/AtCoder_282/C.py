from collections import deque

TARGET_STR = ","
TARGET_STR_CONVERTED = "."
BRAKET_STR = '"'

"""
a,"t,"c,"o,"d,"e,"r,aaa",a,s, =>  a."t,"c."o,"d."e,"r.aaa
"""


class Hogehoge:
    def __init__(self) -> None:
        self.stack_list = deque()

    def hogehoge(self, str_length: int, string: str) -> str:
        """convertされたstringを返す"""
        string_converted = ""
        for idx in range(str_length):
            ith_str = string[idx]
            if ith_str == BRAKET_STR and len(self.stack_list) == 0:  # 開くブラケットの場合
                self.stack_list.append(idx)  # stack にデータ(開ブラケットのidx)を追加
            elif ith_str == BRAKET_STR and len(self.stack_list) != 0:  # 閉じるブラケットの場合
                self.stack_list.pop()  # stackからデータを取り除く
            elif ith_str == TARGET_STR and len(self.stack_list) == 0:
                string_converted += TARGET_STR_CONVERTED
                continue

            string_converted += ith_str

        # if len(self.stack_list) != 0:  # ブラケットが開いたまま、閉じていない場合
        #     unclosed_open_bracet_idx = self.stack_list.pop()
        #     # open_bracet_idx 以降のすべての, を.に置き換える
        #     string_converted[unclosed_open_bracet_idx:] = string_converted[unclosed_open_bracet_idx:].replace(
        #         TARGET_STR, TARGET_STR_CONVERTED
        #     )
        #     pass

        return string_converted


if __name__ == "__main__":
    n = int(input())
    string = input()  # ex) "a,b"c,d
    hogehoge_obj = Hogehoge()
    print(hogehoge_obj.hogehoge(str_length=n, string=string))
