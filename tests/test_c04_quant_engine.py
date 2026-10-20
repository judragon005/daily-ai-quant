"""
單元測試：CARD-04 多因子評分矩陣與風報比計算引擎
遵循 80% 簡化技術中文規範 (STE-TW)
"""
import pandas as pd
import numpy as np
import pytest
from src.c04_quant_engine import (
    calculate_atr,
    calculate_rrr_levels,
    calculate_position_size,
    evaluate_quant_factors,
)


def create_sample_ohlcv(days: int = 60, base_price: float = 100.0) -> pd.DataFrame:
    """輔助函式：產生包含均線與震幅之完整日 K 線資料"""
    dates = pd.date_range(end="2026-10-20", periods=days, freq="B")
    np.random.seed(42)
    # 建立溫和上漲多頭排列走勢
    trend = np.linspace(0, 20, days)
    closes = base_price + trend + np.random.normal(0, 1.0, days)
    highs = closes + 2.0
    lows = closes - 2.0
    opens = closes - 0.5
    volumes = np.random.uniform(500_000, 2_000_000, days)

    df = pd.DataFrame(
        {
            "Open": opens,
            "High": highs,
            "Low": lows,
            "Close": closes,
            "Volume": volumes,
        },
        index=dates,
    )
    return df


def test_calculate_atr():
    """驗證 ATR 震幅計算合法性"""
    df = create_sample_ohlcv(days=30, base_price=100.0)
    atr = calculate_atr(df, period=14)
    assert atr > 0.0
    # 本範例高低差約 4 元，ATR 應落在 3~5 之間
    assert 2.0 <= atr <= 6.0


def test_calculate_rrr_levels():
    """驗證大摩 2 倍 ATR 風報比數值嚴格等於 2.0"""
    price = 100.0
    atr = 5.0
    levels = calculate_rrr_levels(price=price, atr14=atr)
    
    assert levels["entry_price"] == 100.0
    assert levels["stop_loss"] == 90.0   # 100 - 2*5
    assert levels["take_profit"] == 120.0 # 100 + 2*(100 - 90)
    assert levels["rrr"] == 2.0


def test_calculate_position_size():
    """驗證 1% 資本風險部位控制"""
    capital = 1_000_000 # 總資金 100 萬
    risk_pct = 0.01     # 容許最大損失 1 萬元
    price = 100.0
    stop_loss = 90.0    # 每股虧損 10 元
    
    # 預期買進股數 = 10000 / 10 = 1000 股
    shares = calculate_position_size(
        price=price,
        stop_loss=stop_loss,
        capital=capital,
        risk_pct=risk_pct,
        is_tw=False,
    )
    assert shares == 1000
    
    # 台股模式：1000 股剛好等於 1 張 (1000 股)
    tw_shares = calculate_position_size(
        price=price,
        stop_loss=stop_loss,
        capital=capital,
        risk_pct=risk_pct,
        is_tw=True,
    )
    assert tw_shares == 1000


def test_evaluate_quant_factors_score_range():
    """驗證多因子評分區間落於 0 至 100 分"""
    df = create_sample_ohlcv(days=60, base_price=150.0)
    result = evaluate_quant_factors(symbol="2330.TW", df=df, market="TW")
    
    assert "total_score" in result
    score = result["total_score"]
    assert 0 <= score <= 100
    assert "factor_breakdown" in result
    assert "rrr_levels" in result
