# from script.realtime_inference_endpoint.code.recommender import Recommender
# from script.realtime_inference_endpoint.code.models import InferenceType
from recommender import Recommender
from models import InferenceType


def test_deterministic_recommend():
    # Arrange
    user_vectors = {
        "U:1": [1.0, 2.0, 3.0],
    }
    movie_vectors = {
        "M:1": [1.0, 2.0, 3.0],
        "M:2": [2.0, 3.0, 4.0],
        "M:3": [3.0, 4.0, 5.0],
    }
    sut = Recommender(user_vectors, movie_vectors)

    # Act
    actual = sut.predict("U:1", 2, InferenceType.DETERMINISTIC)

    # Assert
    assert actual == [("M:3", 26.0), ("M:2", 20.0)]


def test_stochastic_plackett_luce_recommend():
    # Arrange
    user_vectors = {
        "U:1": [1.0, 2.0, 3.0],
    }
    movie_vectors = {
        "M:1": [1.0, 2.0, 3.0],
        "M:2": [2.0, 3.0, 4.0],
        "M:3": [3.0, 4.0, 5.0],
    }
    sut = Recommender(user_vectors, movie_vectors)

    # Act
    actual = sut.predict("U:1", 2, InferenceType.STOCHASTIC_PLACKETT_LUCE)

    # Assert
    assert len(actual) == 2


def test_stochastic_plackett_luce_cached_recommend():
    # Arrange
    user_vectors = {
        "U:1": [1.0, 2.0, 3.0],
    }
    movie_vectors = {
        "M:1": [1.0, 2.0, 3.0],
        "M:2": [2.0, 3.0, 4.0],
        "M:3": [3.0, 4.0, 5.0],
    }
    sut = Recommender(user_vectors, movie_vectors)

    # Act
    actual = sut.predict("U:1", 2, InferenceType.STOCHASTIC_PLACKETT_LUCE_CACHED)

    # Assert
    assert len(actual) == 2


def test_stochastic_gumbel_softmax_trick_recommend():
    # Arrange
    user_vectors = {
        "U:1": [1.0, 2.0, 3.0],
    }
    movie_vectors = {
        "M:1": [1.0, 2.0, 3.0],
        "M:2": [2.0, 3.0, 4.0],
        "M:3": [3.0, 4.0, 5.0],
    }
    sut = Recommender(user_vectors, movie_vectors)

    # Act
    actual = sut.predict("U:1", 2, InferenceType.STOCHASTIC_GUMBEL_SOFTMAX_TRICK)

    # Assert
    assert len(actual) == 2


def test_stochastic_predict_with_epsilon_greedy():
    # Arrange
    user_vectors = {
        "U:1": [1.0, 2.0, 3.0],
    }
    movie_vectors = {
        "M:1": [1.0, 2.0, 3.0],
        "M:2": [2.0, 3.0, 4.0],
        "M:3": [3.0, 4.0, 5.0],
    }
    sut = Recommender(user_vectors, movie_vectors)

    # Act
    actual = sut.predict("U:1", 2, InferenceType.STOCHASTIC_EPSILON_GREEDY)

    # Assert
    print(actual)
    assert len(actual) == 2
