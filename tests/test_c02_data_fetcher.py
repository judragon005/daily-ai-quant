"""
單元測試：CARD-02 雙市場資料下載與除權息還原
遵循 80% 簡化技術中文規範 (STE-TW)
"""
import pandas as pd
import numpy as np
import pytest
from unittest.mock import patch, MagicMock
from src.c02_data_fetcher import (
    filter_liquid_stocks,
    is_market_closed,
    fetch_market_candles,
)


def create_mock_stock_df(close_price: float, avg_volume: float, days: int = 30) -> pd.DataFrame:
    """輔助函式：產生模擬個股日 K 線資料"""
    dates = pd.date_range(end="2026-10-20", periods=days, freq="B")
    data = {
        "Open": [close_price * 0.99] * days,
        "High": [close_price * 1.02] * days,
        "Low": [close_price * 0.98] * days,
        "Close": [close_price] * days,
        "Volume": [avg_volume] * days,
    }
    return pd.DataFrame(data, index=dates)


def test_filter_liquid_stocks_tw():
    """驗證台股流動性篩選：收盤價 > 10 元，20 日均成交額 > 5000 萬元"""
    # 合格股票：現價 100 元，日均量 1000 張 (1,000,000 股)，成交額 1 億元 > 5000 萬
    df_qualified = create_mock_stock_df(close_price=100.0, avg_volume=1_000_000)
    
    # 不合格 1：雞蛋水餃股（現價 8 元 <= 10 元）
    df_penny = create_mock_stock_df(close_price=8.0, avg_volume=10_000_000)
    
    # 不合格 2：流動性不足（現價 100 元，但日均量僅 100 張，成交額 1000 萬元 < 5000 萬）
    df_illiquid = create_mock_stock_df(close_price=100.0, avg_volume=100_000)
    
    stock_dict = {
        "2330.TW": df_qualified,
        "PENNY.TW": df_penny,
        "LOWVOL.TW": df_illiquid,
    }
    
    result = filter_liquid_stocks(stock_dict, market="TW")
    assert result == ["2330.TW"]


def test_filter_liquid_stocks_us():
    """驗證美股流動性篩選：收盤價 > 5 美元，20 日均成交額 > 1500 萬美元"""
    # 合格：現價 150 美元，日均量 200,000 股，成交額 3000 萬美元 > 1500 萬
    df_qualified = create_mock_stock_df(close_price=150.0, avg_volume=200_000)
    
    # 不合格 1：仙股（現價 3 美元 <= 5 美元）
    df_penny = create_mock_stock_df(close_price=3.0, avg_volume=10_000_000)
    
    # 不合格 2：成交額不足（現價 10 美元，日均量 500,000 股，成交額 500 萬美元 < 1500 萬）
    df_illiquid = create_mock_stock_df(close_price=10.0, avg_volume=500_000)
    
    stock_dict = {
        "NVDA": df_qualified,
        "PENNY_US": df_penny,
        "LOWVOL_US": df_illiquid,
    }
    
    result = filter_liquid_stocks(stock_dict, market="US")
    assert result == ["NVDA"]


def test_is_market_closed():
    """驗證休市判斷邏輯"""
    dates = pd.date_range(end="2026-10-16", periods=5, freq="B")
    df = pd.DataFrame({"Close": [100] * 5}, index=dates)
    
    # 傳入相同或更早日期：判定為休市（無新資料）
    assert is_market_closed(df, last_processed_date="2026-10-16") is True
    
    # 傳入較新日期：判定為非休市（有新交易日）
    assert is_market_closed(df, last_processed_date="2026-10-15") is False


@patch("yfinance.download")
def test_fetch_market_candles_params(mock_download):
    """驗證呼叫 yfinance 時強制啟用 auto_adjust=True"""
    mock_df = pd.DataFrame({"Close": [100.0]})
    mock_download.return_value = mock_df
    
    symbols = ["2330.TW", "2317.TW"]
    fetch_market_candles(symbols, period="1y")
    
    # 驗證參數傳入 auto_adjust=True
    mock_download.assert_called_once()
    _, kwargs = mock_download.call_args
    assert kwargs.get("auto_adjust") is True
