import torch

from machine_learning.sequential_models.paper_attention_is_all_you_need.attention_function import (
    ScaledDotProductAttention,
)


def test_query_and_key_and_value_are_inputted_to_attention_function() -> None:
    # Arrange
    n = 2
    d_k, d_v = 3, 3
    query = torch.tensor([[0.5, 0.6, 0.7], [0.8, 0.9, 1.0]])
    key = torch.tensor([[0.2, 0.3, 0.4], [0.5, 0.6, 0.7]])
    value = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    sut = ScaledDotProductAttention()

    # Act
    output, weights = sut.calc(query, key, value)

    # Assert
    expected_output = torch.tensor([[1.2000, 1.5000, 1.8000], [3.0000, 3.7500, 4.5000]])
    expected_weights = torch.tensor([[0.2582, 0.3416], [0.2582, 0.3416]])
    assert torch.allclose(output, expected_output)
    assert torch.allclose(weights, expected_weights)
