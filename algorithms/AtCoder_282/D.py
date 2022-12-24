import copy
import itertools
from collections import deque
from dataclasses import dataclass
from typing import Dict, List

TARGET_STR = ","
TARGET_STR_CONVERTED = "."
BRAKET_STR = '"'


@dataclass
class Edge:
    value: int
    connected_edge_values: List[int]


class Solver:
    def __init__(self) -> None:
        self.edge_value_edge_mapping: Dict[int, Edge] = {}

    def solve(
        self,
        edge_num: int,
        bar_num: int,
        edge_connectiosn_u: List[int],
        edge_connectiosn_v: List[int],
    ) -> int:
        nice_edge_pair_num = 0

        for bar_idx in range(bar_num):
            u_value = edge_connectiosn_u[bar_idx]
            v_value = edge_connectiosn_v[bar_idx]

            self._register_edge(edge_value=u_value, connected_edge_value=v_value)
            self._register_edge(edge_value=v_value, connected_edge_value=u_value)

        all_pairs = itertools.combinations(self.edge_value_edge_mapping.keys(), 2)
        for edge_val_1, edge_val_2 in all_pairs:
            edge_1 = self.edge_value_edge_mapping[edge_val_1]
            edge_2 = self.edge_value_edge_mapping[edge_val_2]
            if edge_val_2 in edge_1.connected_edge_values:  # 条件1 :繋がっていない事
                continue
            if not self._judge_2_part_graph(edge_1, edge_2):  # 条件2: 繋げると2部グラフになる.
                continue
            nice_edge_pair_num += 1

        return nice_edge_pair_num

    def _register_edge(self, edge_value: int, connected_edge_value: int) -> None:
        if edge_value not in self.edge_value_edge_mapping:  # 初登場のedgeだったら...
            self.edge_value_edge_mapping[edge_value] = Edge(
                value=edge_value,
                connected_edge_values=[connected_edge_value],
            )
            return None

        # 既に登録されているedgeであるケース
        self.edge_value_edge_mapping[edge_value].connected_edge_values.append(connected_edge_value)
        return None

    def _judge_2_part_graph(self, edge_1: Edge, edge_2: Edge) -> bool:
        """
        条件2: もしedge_1とedge_2を繋げると、2部グラフになる.
        """
        # tempのグラフを作り、仮のconnectionを追加
        temp_edge_value_edge_mapping = copy.deepcopy(self.edge_value_edge_mapping)  # shallowではなくdeep copy
        temp_edge_value_edge_mapping[edge_1.value].connected_edge_values.append(edge_2.value)
        temp_edge_value_edge_mapping[edge_2.value].connected_edge_values.append(edge_1.value)
        # ２部グラフになっているか判定する
        return self._is_bipartite_ver2(edges=list(temp_edge_value_edge_mapping.values()))

    def print_edges(self) -> None:
        for value, edge in self.edge_value_edge_mapping.items():
            print(f"edge value {edge.value}")
            print(f"connected_edge_values {edge.connected_edge_values}")
            print("=========================================")

    def _is_bipartite(self, edges: List[Edge]) -> bool:
        """与えられたグラフ(edges)が２部グラフか否かを判定して返す
        - 判定方法
            - 全てのedgeを黒と白の二色で塗り分ける.
            - 隣り合うedgeの色がそれぞれ異なっていれば、2部グラフとみなす.
        """
        white_set = set()
        black_set = set()
        for edge in edges:
            # まだ塗っていないEdgeのケース
            if edge.value not in white_set and edge.value not in black_set:
                white_set.add(edge.value)  # 白に塗りつぶす
                # edgeと繋がっているedgeを探索して、全てblack_setへ入れる
                black_set.update(edge.connected_edge_values)
            # edgeがwhiteで塗りつぶされてるケース
            elif edge.value in white_set:
                for connected_edge in edge.connected_edge_values:
                    if connected_edge in white_set:
                        return False
                    # そうでなければ、connected_edgeをblackで塗る
                    black_set.add(connected_edge)
            # edgeがblackで塗りつぶされてるケース
            elif edge.value in black_set:
                for connected_edge in edge.connected_edge_values:
                    if connected_edge in black_set:
                        return False
                    # そうでなければ、connected_edgeをwhiteで塗る
                    white_set.add(connected_edge)

    def _is_bipartite_ver2(self, edges: List[Edge]) -> bool:
        """与えられたグラフ(edges)が２部グラフか否かを判定して返す
        - 判定方法
            - 全てのedgeを黒と白の二色で塗り分ける.
            - 隣り合うedgeの色がそれぞれ異なっていれば、2部グラフとみなす.
        """
        white_set = set()
        black_set = set()
        for edge in edges:
            # まだ塗っていないEdgeのケース
            if edge.value not in white_set and edge.value not in black_set:
                white_set.add(edge.value)  # 白に塗りつぶす
                # edgeと繋がっているedgeを探索して、全てblack_setへ入れる
                black_set.update(edge.connected_edge_values)
            # edgeがwhiteで塗りつぶされてるケース
            elif edge.value in white_set:
                black_set.update(edge.connected_edge_values)
            # edgeがblackで塗りつぶされてるケース
            elif edge.value in black_set:
                white_set.update(edge.connected_edge_values)

        return not bool(white_set & black_set)  # 一つでも同じ要素があればFalse


if __name__ == "__main__":
    n, m = map(int, input().split())
    u_v_list = [map(int, input().split()) for _ in range(m)]
    u_list, v_list = [list(i) for i in zip(*u_v_list)]

    hogehoge_obj = Solver()
    print(
        hogehoge_obj.solve(
            edge_num=n,
            bar_num=m,
            edge_connectiosn_u=u_list,
            edge_connectiosn_v=v_list,
        )
    )
