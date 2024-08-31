from enum import Enum
from typing import Literal
from pydantic import BaseModel, field_validator
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


class Response(BaseModel):
    user_id: UserId
    recommendations: list[tuple[ContentId, PreferenceScore]]

    # @field_validator("recommendations")
    # def parse_recommendations(
    #     cls,
    #     target: any,
    # ) -> dict[ContentId, PreferenceScore]:
    #     """pydanticのカスタムvalidate & parse メソッドを追加。
    #     recommendations fieldにて、tuple[ContentId, PreferenceScore]を許容してdict[ContentId, PreferenceScore]にparseする。
    #     """
    #     if isinstance(target, tuple) and len(target) == 2:
    #         content_id, preference_score = target
    #         if isinstance(content_id, str) and isinstance(
    #             preference_score, (float, int)
    #         ):
    #             return {content_id: preference_score}
    #     raise ValueError(
    #         "Invalid recommendation format. Expected a tuple of (ContentId, PreferenceScore)."
    #     )
