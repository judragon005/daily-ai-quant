"""
單元測試：CARD-03 大盤雷達與防空警報模組
遵循 80% 簡化技術中文規範 (STE-TW)
"""
import pandas as pd
import pytest
from src.c03_macro_radar import analyze_macro_trend


def test_macro_trend_bullish():
    """驗證大盤指數高於季線時判定為正常多頭"""
    # 建立 70 日歷史資料，價格由 100 漲至 170
    dates = pd.date_range(end="2026-10-20", periods=70, freq="B")
    prices = [100.0 + i for i in range(70)]
    df = pd.DataFrame({"Close": prices}, index=dates)
    
    result = analyze_macro_trend(df, market="TW")
    assert result["is_bearish"] is False
    assert result["status"] == "BULLISH_NORMAL"
    assert result["current_price"] == 169.0
    assert result["ma60"] < result["current_price"]


def test_macro_trend_bearish_defensive():
    """驗證大盤指數跌破季線時標註為空頭防守"""
    # 建立 70 日歷史資料，前面在高點 200，最後幾日暴跌至 120
    dates = pd.date_range(end="2026-10-20", periods=70, freq="B")
    prices = [200.0] * 65 + [120.0] * 5
    df = pd.DataFrame({"Close": prices}, index=dates)
    
    result = analyze_macro_trend(df, market="US")
    assert result["is_bearish"] is True
    assert result["status"] == "BEARISH_DEFENSIVE"
    assert "空頭防守警戒" in result["alert_msg"]
    assert result["current_price"] == 120.0


def test_macro_trend_insufficient_data():
    """驗證資料不足 60 日時之防禦處理"""
    dates = pd.date_range(end="2026-10-20", periods=20, freq="B")
    df = pd.DataFrame({"Close": [100.0] * 20}, index=dates)
    
    result = analyze_macro_trend(df, market="TW")
    # 資料不足時預設為中立/正常
    assert result["is_bearish"] is False
    assert result["status"] == "NEUTRAL_DATA_INSUFFICIENT"
