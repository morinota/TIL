import abc
from collections.abc import Generator
from contextlib import contextmanager
from datetime import date
from pathlib import Path
from random import randint
from typing import Any

import dataset
from mimesis import Field, Schema
from mimesis.locales import Locale
from tinydb import TinyDB

from TTRubberMeet.const import UserRole
from TTRubberMeet.models.user import User


class DBRepositoryInterface(abc.ABC):
    @contextmanager
    def connect(self) -> Generator[Any, None, None]:
        raise NotImplementedError


class MockDbRepsitory(DBRepositoryInterface):
    """疑似データベースのWrapper(=コアロジックに必要な処理だけを抽出したRepositoryクラス?)"""

    def __init__(self, dbpath: Path) -> None:
        s_dbpath = str(dbpath)
        self._dbname = f"sqlite:///{s_dbpath}"
        self._init_mock_db()  # 今後の章で実装

    def _init_mock_db(self):
        self._create_mock_user_table()

    @contextmanager
    def connect(self) -> Generator[dataset.Database, None, None]:
        """context manager = with句と組み合わせて使うやつ"""
        db = dataset.connect(self._dbname)
        db.begin()
        try:
            yield db
            db.commit()
        except Exception as e:
            db.rollback()
            raise e

    def _create_mock_user_table(self) -> None:
        sample_users = [
            User(
                user_id="member",
                name="会員",
                birthday=date(2000, 1, 1),
                email="guest@example.com",
                role=UserRole.MEMBER,
            ),
            User(
                user_id="admin",
                name="管理者",
                birthday=date(2000, 1, 1),
                email="admin@example.com",
                role=UserRole.ADMIN,
            ),
        ]
        with self.connect() as db:
            table: dataset.Table = db["users"]
            for user in sample_users:
                table.insert(user.to_dict())


class MockSessionDBRepository(DBRepositoryInterface):
    def __init__(self, dbpath: Path) -> None:
        self._db = TinyDB(dbpath)

    @contextmanager
    def connect(self) -> Generator[TinyDB, None, None]:
        try:
            yield self._db
        except Exception as e:
            raise e
