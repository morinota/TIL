import abc


class ModelInterface(abc.ABC):
    def to_dict(self) -> dict[str, str]:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "ModelInterface":
        raise NotImplementedError
