import itertools
import re
from collections import deque
from dataclasses import dataclass
from typing import Deque, Dict, Generator, List, Tuple


@dataclass
class EncodedData:
    IS_HAVING_BRAKET_PATTERN = re.compile(r".*\(.*\).*")
    BRAKET_EXPANDING_PATTERN = re.compile(r"(\d+)\(([^()]+)\)")  # 1個以上の数字 + (1個以上の何かしら)
    COEF_CHAR_SEPARATE_PATTAEN = re.compile(r"(\d*)(\D)")  # 0個以上の数字 + 1個の文字列
    text: str

    def is_having_brakets(self) -> bool:
        if EncodedData.IS_HAVING_BRAKET_PATTERN.match(self.text):
            return True

        return False


class Decoder:
    """
    - データは文字列で表され、文字数は最大で 2^60 と非常に長い文字列の可能性がある.
    - データに含まれる文字は英小文字('a' - 'z') の26種類のみからなる.
    - 本クラスは圧縮後のデータを圧縮前のデータにDecodeする.
    - ex)
        - 圧縮後: "2(2u2lt4d)3(rb)pa"
        - 圧縮前: "uulltdddduulltddddrbrbrbpa"
    - また、圧縮されたデータは必ずしも最適に圧縮されているとは限らない.
        - ex) 圧縮前: uuuuuuのケース
        - 圧縮後のパターン: 6u, 2(3u)、3(2u)、3u3u、4uuu、uuuuuu
    """

    def __init__(self) -> None:
        pass

    def solve(self, encoded_str: str) -> Dict[str, int]:
        """圧縮後のデータ(str)を受け取り、
        圧縮前のデータ(str)における英小文字('a' - 'z') の出現回数をカウントする.
        返り値はkey=英小文字, value=出現回数, 要素数26のDict[str, int]
        """
        encoded_data = EncodedData(encoded_str)

        while encoded_data.is_having_brakets():
            encoded_data.text = self._expand_minimize_brakets(encoded_data.text)

        coef_char_pairs = self._get_coef_char_pairs(encoded_data.text)

        return self._count_chars(coef_char_pairs)

    def _expand_minimize_brakets(self, decoded_text: str) -> str:
        """最も小さいブラケットを展開する
        ex) (())のケースでは内側の()のみを展開する.
        """
        match_objects = re.findall(EncodedData.BRAKET_EXPANDING_PATTERN, decoded_text)

        for coef, text_in_braket in match_objects:

            coef_char_pairs_in_braket = self._get_coef_char_pairs(text_in_braket)
            coef_char_pairs_multiplied = self._multiply_to_coef(
                coef_char_pairs_in_braket,
                int(coef),
            )
            decoded_text = decoded_text.replace(
                f"{coef}({text_in_braket})",
                self._recompose_text(coef_char_pairs_multiplied),
            )  # ()の箇所を置き換え.
        return decoded_text

    def _get_coef_char_pairs(self, decoded_text: str) -> List[Tuple[int, str]]:
        """textに"()"は入っていない想定."""

        coef_char_pairs = []
        for coef, char in re.findall(
            EncodedData.COEF_CHAR_SEPARATE_PATTAEN,
            decoded_text,
        ):
            if coef == "":
                coef = 1
            coef_char_pairs.append((int(coef), char))
        return coef_char_pairs

    def _recompose_text(self, coef_char_pairs: List[Tuple[int, str]]) -> str:
        """ペアのタプルからstrを再構築する
        ex) [(4,u), (4,l)] -> "4u4l"
        """
        recomposed_text = ""
        for coef, char in coef_char_pairs:
            recomposed_text += str(coef) + char
        return recomposed_text

    def _multiply_to_coef(
        self,
        coef_char_pairs: List[Tuple[int, str]],
        multiplier: int,
    ) -> List[Tuple[int, str]]:
        return [(coef * multiplier, char) for coef, char in coef_char_pairs]

    def _count_chars(self, coef_char_pairs: List[Tuple[int, str]]) -> Dict[str, int]:
        """coef_char_pairsを受け取り, 各 英小文字の総出現回数を計算する"""
        char_count_map = {chr(i): 0 for i in range(ord("a"), ord("z") + 1)}  # a~zのmapを初期化(初期値0)
        for coef, char in coef_char_pairs:
            char_count_map[char] += coef
        return char_count_map


def main():
    s = input()  # 圧縮後のデータを表す文字列s

    char_count_map = Decoder().solve(s)

    for char, count in char_count_map.items():
        print(f"{char} {count}")


if __name__ == "__main__":
    main()
