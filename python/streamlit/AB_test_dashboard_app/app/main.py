import streamlit as st
from app.pages import dashboard

# タイトルの設定()
st.title("ABテストダッシュボード")

# ABtest idを入力するためのテキストボックスをメインページに配置。
abtest_id = st.text_input("ABテストIDを入力してください")

# ダッシュボードの表示
if abtest_id:
    dashboard.display(abtest_id)
