from enum import Enum

from pydantic import BaseModel
from type_aliases import ContentId, PreferenceScore, UserId


class InferenceType(Enum):
    DETERMINISTIC = "deterministic"
    STOCHASTIC_PLACKETT_LUCE = "stochastic_plackett_luce"
    STOCHASTIC_PLACKETT_LUCE_CACHED = "stochastic_plackett_luce_cached"
    STOCHASTIC_GUMBEL_SOFTMAX_TRICK = "stochastic_gumbel_softmax_trick"
    STOCHASTIC_EPSILON_GREEDY = "stochastic_epsilon_greedy"


class Request(BaseModel):
    user_id: UserId
    k: int
    inference_type: InferenceType = InferenceType.DETERMINISTIC
    n: int = 1000


class Response(BaseModel):
    user_id: UserId
    recommendations: list[tuple[ContentId, PreferenceScore]]
