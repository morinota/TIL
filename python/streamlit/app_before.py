import streamlit as st
import csv

from enum import Enum


class AtBat(Enum):
    READY = 0
    HOME_RUN = 4
    OUTS = -1


abbat = AtBat.READY

throws = {"右": "R", "左": "L"}

# 球種を読み込む
pitch_types = {}
with open("dataset/pitch_type.csv") as f:
    reader = csv.DictReader(f)
    for r in reader:
        if r["pitch_name"] == "Curveball":
            pass
        elif r["pitch_name"] == "Fastball":
            pass
        else:
            pitch_types[r["pitch_name_jp"]] = r["pitch_name_jp"]

st.write(" # オオタニサン本塁打予測 :baseball:")
st.write("オオタニサンがホームランを打てるボールか占ってみよう")

# サイドバーを使ってみる
st.sidebar.markdown(
    """
    # ボールを決める
    """
)

p_throw = st.sidebar.selectbox(
    "利き腕",
    throws.keys(),
)
pitch_speed = st.sidebar.slider(
    "球速(km/h)",
    70,
    170,
    150,
    5,
)
pitch_type = st.sidebar.selectbox(
    "球種",
    pitch_types.keys(),
    index=4,
)

# 球種の検索用にkm/h -> mp/h 変換
pitch_speed_mph = round(pitch_speed / 1.609, 1)

# 入力値を一旦書き出す
st.write("## 投球・球種・球速")
st.write(
    f"""
    - {p_throw}
    - {pitch_speed} km/h ({pitch_speed_mph} mph)
    - {pitch_type}(code: {pitch_types.get(pitch_type, "Unknown")})
    """
)

# 結果を予測する
import joblib

# sk-learnで学習済みのモデルがあるのでそれをloadする
model = joblib.load("model/ohtani_hr_model_app.joblib")


from dataclasses import dataclass
import pandas as pd


@dataclass
class Form:
    throws: str
    pitch_speed_kmh: float
    pitch_speed_mph: float
    pitch_type: str


def predict(form: Form) -> AtBat:
    # 過去の投打履歴を取ってくる?
    df = pd.read_csv("dataset/predict_shohei_ohtani_features03_app_dataset.csv")
    # 欲しいデータのみに絞る
    df = df[df["game_date"].between("2021-08-01", "2021-11-30")]
    # 利き腕
    df = df[df["p_throws"] == form.throws]
    # カーブの時は2つの種別で見る
    if pitch_type == "CU":
        pitch_types = ("CU", "CS")
    else:
        pitch_types = (form.pitch_type,)
    df = df[df["pitch_type"].isin(pitch_types)]

    if len(df) == 0:
        # 0件だったら(=過去の履歴にない球種だったら)アウト
        return AtBat.OUTS

    # 球速で絞る
    df = df[df["release_speed"].between(form.pitch_speed_mph - 5, form.pitch_speed_mph + 5)]
    if len(df) == 0:
        # 0件だったら(=過去の履歴にない球速だったら)アウト
        return AtBat.OUTS

    # 予測する
    data = df[["a", "b"]]
    pre = model.predict_proba(data.to_numpy())[:, 1]
    # スコア結果を見て判定
    for r in pre:
        if float(r) >= 0.042 and float(r) < 0.043:
            return AtBat.HOME_RUN
        elif float(r) >= 0.0414 and float(r) < 0.0416:
            return AtBat.HOME_RUN
        elif float(r) >= 0.038 and float(r) < 0.0386:
            return AtBat.HOME_RUN
        elif float(r) >= 0.029 and float(r) < 0.029:
            return AtBat.HOME_RUN
    return AtBat.OUTS


st.write("## 結果")


from PIL import Image

# TODO 確率を出す
if st.sidebar.button("投げる"):
    form = Form(
        pitch_type=pitch_types[pitch_type],
        throws=throws[p_throw],
        pitch_speed_kmh=pitch_speed,
        pitch_speed_mph=pitch_speed_mph,
    )
    atbat = predict(form)

    if atbat == AtBat.READY:
        st.image(Image.open("assets/img/baseball_homerun_yokoku.png"), caption="勝負")
    elif atbat == AtBat.HOME_RUN:
        st.image(Image.open("assets/img/baseball_homerun_man.png"), caption="オオタニサン！")
    else:
        st.image(Image.open("assets/img/baseball_strike_man.png"), caption="残念")
else:
    # リセット
    atbat = AtBat.READY
    st.image(Image.open("assets/img/baseball_homerun_yokoku.png"), caption="勝負")
