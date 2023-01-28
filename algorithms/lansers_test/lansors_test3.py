import json
from typing import Dict, Tuple

import requests
from requests.models import Response


def get_responce(url: str) -> Tuple[Dict, int]:
    responce: Response = requests.get(url)
    data = json.loads(responce.text)
    return json.loads(responce.text), responce.status_code


def main() -> None:
    url = "https://api.lancers.jp/v1/example/users/me"
    responce: Response = requests.get(url)


if __name__ == "__main__":
    main()
