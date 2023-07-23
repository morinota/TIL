from __future__ import annotations

import json
from dataclasses import dataclass
from uuid import uuid4

from TTRubberMeet.models.cart import Cart
from TTRubberMeet.models.model_interface import ModelInterface


@dataclass(frozen=True)
class Session(ModelInterface):
    user_id: str
    cart: Cart
    session_id: str = str(uuid4())

    def to_dict(self) -> dict[str, str]:
        cart_dict = self.cart.to_dict()
        return dict(
            session_id=self.session_id,
            user_id=self.user_id,
            cart=json.dumps(cart_dict),
        )

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Session:
        cart_dict = json.loads(data["cart"])
        return Session(
            session_id=data["session_id"],
            user_id=data["user_id"],
            cart=Cart.from_dict(cart_dict),
        )
