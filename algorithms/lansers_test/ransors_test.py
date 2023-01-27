from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class MultiplyTable:
    elements: List[List[int]]

    @classmethod
    def create(
        cls,
        first_int: int = 1,
        last_int: int = 9,
    ) -> "MultiplyTable":
        elements = []
        for row_int in range(first_int, last_int + 1):
            elements.append([row_int * col_int for col_int in range(first_int, last_int + 1)])
        return MultiplyTable(elements)

    def print_table(self) -> None:
        """MultiplyTableの中身をコンソール出力する.
        - 各数字間が半角スペースで区切られるように表示する.
        - 桁が異なる数字でも揃えて表示されるように, 桁数が最大のものに合わせて半角スペースを左に追加する
        """
        max_element = max([element for row_elements in self.elements for element in row_elements])
        max_digit_count = len(str(max_element))
        elements_arranged = self._arrange_digit_count(max_digit_count)
        for raw_elements in elements_arranged:
            print(" ".join(raw_elements))

    def _arrange_digit_count(self, max_digit_count) -> List[List[str]]:
        return [[str(element).rjust(max_digit_count) for element in raw_elements] for raw_elements in self.elements]


def main() -> None:
    table = MultiplyTable.create(1, 9)
    table.print_table()


if __name__ == "__main__":
    main()
