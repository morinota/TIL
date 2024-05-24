# sourcedir.tar.gzの中に格納したinference.py
import os
from urllib import response


def model_fn(model_dir: str):
    with open(os.path.join(model_dir, "my_model.txt"), "r") as f:
        model = f.read()[:-1]
    return model


def predict_fn(input_data, model):
    response = f"{model} for the {input_data}st time"
    return response


def input_fn(input_data, content_type):
    if content_type == "text/csv":
        transformed_data = input_data.split(",")
    else:
        raise ValueError("Illegal content type")
    return transformed_data


def predict_fn(transformed_data, model):
    prediction_list = []
    for data in transformed_data:
        if data[-1] == "1":
            ordinal = f"{data}st"
        elif data[-1] == "2":
            ordinal = f"{data}nd"
        elif data[-1] == "3":
            ordinal = f"{data}rd"
        else:
            ordinal = f"{data}th"
        prediction = f"{model} for the {ordinal} time"
        prediction_list.append(prediction)
    return prediction_list


# 後処理
def output_fn(prediction_list, accept):
    if accept == "text/csv":
        response = ""
        for prediction in prediction_list:
            response += prediction + "¥n"
    else:
        raise ValueError("Illegal accept type")
    return response, accept
