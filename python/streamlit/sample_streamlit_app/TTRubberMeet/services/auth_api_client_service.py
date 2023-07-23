import abc

import dataset

from TTRubberMeet.exeptions import MyError
from TTRubberMeet.models.cart import Cart
from TTRubberMeet.models.session import Session
from TTRubberMeet.services.mock_db_repository import DBRepositoryInterface


class AuthenticationError(MyError):
    pass


class AuthAPIClientServiceInterface(abc.ABC):
    """AuthAPI にアクセスする client クラス"""

    @abc.abstractmethod
    def login(self, user_id: str, password: str) -> str:
        raise NotImplementedError


class MockAuthAPIClientService(AuthAPIClientServiceInterface):
    def __init__(self, mockdb: DBRepositoryInterface, session_db: DBRepositoryInterface) -> None:
        self.mockdb = mockdb
        self.session_db = session_db

    def login(self, user_id: str, password: str) -> str:
        """
        # ログインに成功した場合、MockSessionDBにセッションを追加し、セッションIDを返す
        # ログインに失敗した場合、AuthenticationErrorを発生させる
        """
        if not self._verify_user(user_id, password):
            raise AuthenticationError

        session = Session(user_id=user_id, cart=Cart(user_id))
        with self.session_db.connect() as db:
            db.insert(session.to_dict())

        return session.session_id

    def _verify_user(self, user_id: str, password: str) -> bool:
        """
        # 指定されたユーザIDを持つユーザがMockDBのユーザテーブルに入ればTrueを返す
        # ※パスワードの検証は行わない
        """
        with self.mockdb.connect() as db:
            table: dataset.Table = db["users"]
            user_data = table.find_one(user_id=user_id)

        return user_data is not None
