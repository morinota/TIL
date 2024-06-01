from datetime import datetime
import patito as pt
from typing import Literal


class AppLaunchLogSchema(pt.Model):
    # user_idは1~4の4人のみ
    user_id: int = pt.Field(ge=1, le=4)
    timestamp: datetime
    os: Literal["iOS", "Android"]


class UserVariantMappingSchema(pt.Model):
    # user_idは1~4の4人のみ
    user_id: int = pt.Field(ge=1, le=4)
    # abtest_idは1000, 1001の2つのみ
    abtest_id: int = pt.Field(ge=1001, le=1002)
    variant: Literal["controll", "treatment"]


class UserMetadataSchema(pt.Model):
    # user_idは1~4の4人のみ
    user_id: int = pt.Field(ge=1, le=4, unique=True)
    is_paid_user: bool
    age: int = pt.Field(ge=0, le=150)
    sex: Literal["male", "female"]
