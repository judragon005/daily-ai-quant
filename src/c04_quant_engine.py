"""
CARD-04 多因子評分矩陣與風報比計算引擎
遵循 80% 簡化技術中文規範 (STE-TW)
"""
from typing import Dict, Any, Optional
import numpy as np
import pandas as pd


def calculate_atr(df: pd.DataFrame, period: int = 14) -> float:
    """計算真實震幅均值 (ATR)"""
    if len(df) < period + 1:
        # 資料不足時以最高價減最低價均值估算
        spread = (df["High"] - df["Low"]).mean()
        return round(float(spread if spread > 0 else 1.0), 2)

    high = df["High"]
    low = df["Low"]
    close = df["Close"].shift(1)

    tr1 = high - low
    tr2 = (high - close).abs()
    tr3 = (low - close).abs()

    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean().iloc[-1]
    return round(float(atr if not np.isnan(atr) else 1.0), 2)


def calculate_rrr_levels(price: float, atr14: float) -> Dict[str, float]:
    """計算 2 倍 ATR 停損點位與風報比 (固定為 2.0)"""
    stop_distance = round(2.0 * atr14, 2)
    stop_loss = round(max(0.01, price - stop_distance), 2)
    take_profit = round(price + (2.0 * stop_distance), 2)

    return {
        "entry_price": round(price, 2),
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "rrr": 2.0,
    }


def calculate_position_size(
    price: float,
    stop_loss: float,
    capital: float = 1_000_000.0,
    risk_pct: float = 0.01,
    is_tw: bool = False,
) -> int:
    """依據 1% 資本風險原則計算建議部位股數"""
    risk_per_share = price - stop_loss
    if risk_per_share <= 0:
        return 0

    max_risk_capital = capital * risk_pct
    raw_shares = int(max_risk_capital / risk_per_share)

    if is_tw:
        # 台股整張交易：向下取 1000 股倍數
        tw_lots = raw_shares // 1000
        return max(1000, tw_lots * 1000) if tw_lots > 0 else raw_shares

    return max(1, raw_shares)


def evaluate_quant_factors(
    symbol: str,
    df: pd.DataFrame,
    market: str = "TW",
) -> Dict[str, Any]:
    """計算四大維度多因子權重評分 (0-100) 與風報比"""
    if df.empty or len(df) < 20:
        return {
            "symbol": symbol,
            "total_score": 50.0,
            "factor_breakdown": {},
            "rrr_levels": {"entry_price": 0.0, "stop_loss": 0.0, "take_profit": 0.0, "rrr": 2.0},
        }

    latest_close = float(df["Close"].iloc[-1])
    atr = calculate_atr(df, period=14)
    rrr_levels = calculate_rrr_levels(latest_close, atr)

    # 1. 動能因子 (20%)：均線排列與漲跌動能
    ma20 = df["Close"].rolling(20).mean().iloc[-1]
    ma50 = df["Close"].rolling(min(len(df), 50)).mean().iloc[-1]
    momentum_score = 0.0
    if latest_close > ma20:
        momentum_score += 10.0
    if ma20 > ma50:
        momentum_score += 10.0

    # 2. 價值因子 (30%)：以均線回檔幅度與價格穩健度模擬
    distance_to_ma20 = (latest_close - ma20) / ma20
    if -0.05 <= distance_to_ma20 <= 0.05:
        value_score = 30.0
    elif distance_to_ma20 > 0.05:
        value_score = 22.0
    else:
        value_score = 15.0

    # 3. 品質因子 (25%)：低波動穩定度
    returns = df["Close"].pct_change().dropna()
    volatility = returns.std()
    quality_score = 25.0 if volatility < 0.02 else (18.0 if volatility < 0.035 else 12.0)

    # 4. 市場特徵 (25%)：成交量擴增強度
    recent_vol = df["Volume"].tail(5).mean()
    base_vol = df["Volume"].tail(20).mean()
    vol_ratio = recent_vol / (base_vol + 1e-6)
    market_score = 25.0 if vol_ratio > 1.2 else (20.0 if vol_ratio >= 0.9 else 15.0)

    total_score = round(value_score + quality_score + momentum_score + market_score, 1)

    return {
        "symbol": symbol,
        "total_score": min(100.0, max(0.0, total_score)),
        "factor_breakdown": {
            "value": round(value_score, 1),
            "quality": round(quality_score, 1),
            "momentum": round(momentum_score, 1),
            "market": round(market_score, 1),
        },
        "rrr_levels": rrr_levels,
    }
