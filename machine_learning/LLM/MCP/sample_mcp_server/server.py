from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

# FastMCPサーバーを初期化
mcp = FastMCP("Morita's Weather")

# 定数
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "Morita's Weather App/1.0"


async def make_nws_request(url: str) -> dict[str, Any] | None:
    """NWS APIへのリクエストを適切なエラーハンドリング付きで実行します。"""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


def format_alert(feature: dict) -> str:
    """アラート情報を読みやすい文字列にフォーマットします。"""
    props = feature["properties"]
    return f"""
イベント: {props.get('event', '不明')}
地域: {props.get('areaDesc', '不明')}
深刻度: {props.get('severity', '不明')}
説明: {props.get('description', '説明はありません。')}
指示: {props.get('instruction', '特定の指示はありません。')}
"""


@mcp.tool()
async def get_alerts(state: str) -> str:
    """指定された州の気象警報を取得します。

    引数:
        state: 米国の州コード（例: CA, NY）
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "警報を取得できないか、警報が見つかりませんでした。"

    if not data["features"]:
        return "この州には現在アクティブな警報はありません。"

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """指定された場所の天気予報を取得します。

    引数:
        latitude: 場所の緯度
        longitude: 場所の経度
    """
    # まず予報グリッドのエンドポイントを取得
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "この場所の予報データを取得できませんでした。"

    # ポイントレスポンスから予報URLを取得
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "詳細な予報を取得できませんでした。"

    # 期間をフォーマットして読みやすい予報に変換
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # 次の5期間のみ表示
        forecast = f"""
{period['name']}:
気温: {period['temperature']}°{period['temperatureUnit']}
風: {period['windSpeed']} {period['windDirection']}
予報: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)


if __name__ == "__main__":
    # サーバーを初期化して実行
    mcp.run(transport="stdio")
