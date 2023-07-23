from dataclasses import dataclass

from TTRubberMeet.models.model_interface import ModelInterface


@dataclass(frozen=True)
class Rubber(ModelInterface):
    item_id: str
    name: str
    price: int
    producing_area: str

    def to_dict(self) -> dict[str, str]:
        return dict(
            item_id=self.item_id,
            name=self.name,
            price=str(self.price),
            producing_area=self.producing_area,
        )

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "Rubber":
        return Rubber(
            item_id=data["item_id"],
            name=data["name"],
            price=int(data["price"]),
            producing_area=data["producing_area"],
        )
