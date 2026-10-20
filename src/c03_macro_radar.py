"""
CARD-03 大盤雷達與防空警報模組
遵循 80% 簡化技術中文規範 (STE-TW)
"""
from typing import Dict, Any
import pandas as pd


def analyze_macro_trend(
    index_df: pd.DataFrame,
    market: str = "TW",
) -> Dict[str, Any]:
    """計算大盤指數現價與 60 日季線，產出多空狀態與警報"""
    index_name = "台灣加權指數 (^TWII)" if market.upper() == "TW" else "標普 500 指數 (^GSPC)"

    if index_df.empty or len(index_df) < 5:
        return {
            "index_name": index_name,
            "current_price": 0.0,
            "ma60": 0.0,
            "is_bearish": False,
            "status": "NEUTRAL_DATA_EMPTY",
            "alert_msg": "資料庫無大盤歷史資料。",
        }

    latest_close = round(float(index_df["Close"].iloc[-1]), 2)

    # 檢查是否具備足夠計算 MA60 之日數
    if len(index_df) < 60:
        return {
            "index_name": index_name,
            "current_price": latest_close,
            "ma60": round(float(index_df["Close"].mean()), 2),
            "is_bearish": False,
            "status": "NEUTRAL_DATA_INSUFFICIENT",
            "alert_msg": f"{index_name} 資料少於 60 日，以整體平均計算。",
        }

    ma60 = round(float(index_df["Close"].tail(60).mean()), 2)
    is_bearish = bool(latest_close < ma60)

    if is_bearish:
        status = "BEARISH_DEFENSIVE"
        alert_msg = f"⚠️ [空頭防守警戒] {index_name} 現價 ({latest_close}) 已跌破季線 MA60 ({ma60})，建議縮減部位防守！"
    else:
        status = "BULLISH_NORMAL"
        alert_msg = f"🟢 [正常多頭格局] {index_name} 現價 ({latest_close}) 維持在季線 MA60 ({ma60}) 之上。"

    return {
        "index_name": index_name,
        "current_price": latest_close,
        "ma60": ma60,
        "is_bearish": is_bearish,
        "status": status,
        "alert_msg": alert_msg,
    }
