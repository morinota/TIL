import json
from datetime import date, datetime
from typing import Dict

import requests
from pydantic.dataclasses import dataclass
from requests.models import Response


@dataclass
class UserInfo:
    DATETIME_FORMAT = r"%Y-%m-%d"
    SHOW_FORMAT = """
    氏名：{}
    性別：{}
    年齢：{}
    """
    GENDER_ENG_JP_MAP = {
        "male": "男性",
        "female": "女性",
    }

    user_id: int
    nickname: str
    name: str
    birthday: date
    gender: str
    email: str
    phone_number: int

    @classmethod
    def from_dict(cls, responce_text: Dict) -> "UserInfo":
        return UserInfo(
            user_id=responce_text["user_id"],
            nickname=responce_text["nickname"],
            name=responce_text["name"],
            birthday=datetime.strptime(responce_text["birthday"], UserInfo.DATETIME_FORMAT),
            gender=responce_text["gender"],
            email=responce_text["email"],
            phone_number=responce_text["phone_number"],
        )

    @property
    def age(self) -> int:
        execution_date = datetime.now().date()
        return execution_date.year - self.birthday.year

    def show(self) -> None:
        print(
            UserInfo.SHOW_FORMAT.format(
                self.name,
                UserInfo.GENDER_ENG_JP_MAP[self.gender],
                self.age,
            )
        )


def get_user_info_responce(url: str) -> UserInfo:
    responce: Response = requests.get(url)
    if responce.status_code != 200:
        return None
    data = json.loads(responce.text)
    return UserInfo.from_dict(data)


def main() -> None:
    url = "https://api.lancers.jp/v1/example/users/me"
    user_info = get_user_info_responce(url)
    user_info.show()


if __name__ == "__main__":
    main()
