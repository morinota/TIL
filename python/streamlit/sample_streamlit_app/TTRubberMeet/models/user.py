from dataclasses import dataclass
from datetime import date, datetime

from TTRubberMeet.const import UserRole
from TTRubberMeet.models.model_interface import ModelInterface


@dataclass(frozen=True)
class User(ModelInterface):
    """ユーザ種別はページの閲覧権限の切り替えに使用."""

    user_id: str
    name: str
    birthday: date
    email: str
    role: UserRole  # roleはEnum型で定義

    def to_dict(self) -> dict[str, str]:
        return dict(
            user_id=self.user_id,
            name=self.name,
            birthday=self.birthday.isoformat(),
            email=self.email,
            role=self.role.name,
        )

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "User":
        birthday = datetime.fromisoformat(data["birthday"])
        return User(
            user_id=data["user_id"],
            name=data["name"],
            birthday=birthday.date(),
            email=data["email"],
            role=UserRole[data["role"]],
        )
