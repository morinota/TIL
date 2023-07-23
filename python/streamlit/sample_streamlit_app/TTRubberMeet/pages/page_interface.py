import abc

from TTRubberMeet.const import PageId
from TTRubberMeet.session_manager import StreamlitSessionManager

"""
ページを追加したい時は、以下の手順で行います。

1. PageId の属性を増やす
2. BasePage を継承したページクラスを作る
3. MultiPageApp のpagesにページ ID とページクラスのペアを追加する
"""


class PageInterface(abc.ABC):
    def __init__(self, page_id: PageId, title: str, ssm: StreamlitSessionManager) -> None:
        self.page_id = page_id.name
        self.title = title
        self.ssm = ssm

    @abc.abstractmethod
    def render(self) -> None:
        raise NotImplementedError
