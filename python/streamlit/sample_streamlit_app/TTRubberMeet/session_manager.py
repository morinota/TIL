from typing import Optional

import streamlit as st

from TTRubberMeet.const import SessionKey
from TTRubberMeet.models.user import User


class StreamlitSessionManager:
    """st.session_state のWrapperクラス.
    SessionManager では明示的に(Session state API で)保持するデータのみをkey-valueで管理する.
    """

    def __init__(self) -> None:
        self._session_state = st.session_state  # key-value型

    def get_user(self) -> User:
        return self._session_state[SessionKey.USER.name]

    def set_user(self, user: User) -> None:
        self._session_state[SessionKey.USER.name] = user
