import streamlit as st
from streamlit import selectbox
from app.pages import binary_metric_page, non_binary_metric_page

# タイトルの設定
st.title("ABテストの理想的なサンプルサイズ計算アプリ")

# メニューの設定(selectboxを使ってページ選択)
option = st.selectbox(
    "計算したいメトリクスを選択してください",
    ("二値メトリクス", "非二値メトリクス"),
)

if option == "二値メトリクス":
    binary_metric_page.display()
else:
    non_binary_metric_page.display()
