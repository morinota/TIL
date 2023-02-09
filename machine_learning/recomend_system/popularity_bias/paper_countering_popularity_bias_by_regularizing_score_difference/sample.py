import numpy as np


def generate_sysnthetic_data(
    n_user: int = 200,
    n_item: int = 200,
) -> np.ndarray:
    user_item_matrix = np.zeros(shape=(n_user, n_item))
    for user_idx in range(n_user):
        for item_idx in range(n_item):
            user_item_matrix[user_idx, item_idx] = _formula_for_sysnthetic_data(
                user_idx,
                item_idx,
            )
    return user_item_matrix


def _formula_for_sysnthetic_data(user_idx: int, item_idx: int, boundary_num: int = 200) -> int:
    if user_idx + item_idx <= boundary_num:
        return 1
    return 0


def main():
    generate_sysnthetic_data()


if __name__ == "__main__":
    main()
