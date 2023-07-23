import streamlit as st

from TTRubberMeet.const import SessionKey
from TTRubberMeet.exeptions import MyError
from TTRubberMeet.pages.page_interface import PageInterface
from TTRubberMeet.session_manager import StreamlitSessionManager


class MultiPageApp:
    """本クラス がページクラスを切り替えることで、複数ページアプリのように見せる"""

    def __init__(self, ssm: StreamlitSessionManager, pages: list[PageInterface], nav_label: str = "ページ一覧") -> None:
        self.page_by_id = {page.page_id: page for page in pages}
        self.ssm = ssm
        self.nav_label = nav_label

    def render(self) -> None:
        # ページ選択ボックスを追加
        page_id = st.sidebar.selectbox(
            self.nav_label,
            list(self.page_by_id.keys()),
            format_func=lambda page_id: self.page_by_id[page_id].title,  # page titleを表示する.
            key=SessionKey.PAGE_ID.name,
        )

        # self.ssm.show_userbox()

        # ページ描画
        try:
            self.page_by_id[page_id].render()
        except MyError as e:
            st.error(e)
