from typing import List

import numpy as np


def bag_of_words(embedded_texts: List[List[np.ndarray]]) -> List[np.ndarray]:
    """text内の各tokenのembedding vector を '足し合わせる'(恐らくココがbag of wordsの本質?)."""

    bag_of_words_texts = []
    return [np.sum(embedded_tokens, axis=0) for embedded_tokens in embedded_texts]


def main():
    corpas = ["私 は ラーメン が 好き です 。", "私 は 餃子 が 好き です 。", "私 は ラーメン が 嫌い です 。"]


if __name__ == "__main__":
    main()


def test_bag_of_words() -> None:
    embedded_text = [
        np.array([1, 0, 0, 0, 0, 0, 0, 0, 0]),
        np.array([0, 1, 0, 0, 0, 0, 0, 0, 0]),
        np.array([0, 0, 1, 0, 0, 0, 0, 0, 0]),
    ]

    bag_of_words_texts_actual = bag_of_words(embedded_texts=[embedded_text])

    bag_of_words_text_expected = np.array([1, 1, 1, 0, 0, 0, 0, 0, 0])

    np.testing.assert_array_equal(bag_of_words_texts_actual[0], bag_of_words_text_expected)
