"""
CARD-02 雙市場資料下載與除權息還原模組
遵循 80% 簡化技術中文規範 (STE-TW)
"""
from typing import Dict, List, Optional
import pandas as pd
import yfinance as yf


def fetch_market_candles(
    symbols: List[str],
    period: str = "1y",
    interval: str = "1d",
) -> pd.DataFrame:
    """批次下載日 K 線資料，強制啟用 auto_adjust=True 還原除權息"""
    if not symbols:
        return pd.DataFrame()

    df = yf.download(
        tickers=symbols,
        period=period,
        interval=interval,
        group_by="ticker",
        auto_adjust=True,
        threads=True,
        progress=False,
    )
    return df


def filter_liquid_stocks(
    stock_dict: Dict[str, pd.DataFrame],
    market: str = "TW",
) -> List[str]:
    """依流動性與股價門檻篩選合格標的"""
    qualified_symbols: List[str] = []

    for symbol, df in stock_dict.items():
        if df.empty or len(df) < 20:
            continue

        # 取得最新收盤價與近 20 日資料
        recent_20 = df.tail(20)
        latest_close = float(recent_20["Close"].iloc[-1])
        
        # 計算近 20 日平均成交金額 (收盤價 * 成交量)
        avg_turnover = float((recent_20["Close"] * recent_20["Volume"]).mean())

        if market.upper() == "TW":
            # 台股門檻：收盤價 > 10 元，20 日均成交額 > 5000 萬元新台幣
            if latest_close > 10.0 and avg_turnover > 50_000_000:
                qualified_symbols.append(symbol)
        elif market.upper() == "US":
            # 美股門檻：收盤價 > 5 美元，20 日均成交額 > 1500 萬美元
            if latest_close > 5.0 and avg_turnover > 15_000_000:
                qualified_symbols.append(symbol)

    return qualified_symbols


def is_market_closed(
    df: pd.DataFrame,
    last_processed_date: Optional[str] = None,
) -> bool:
    """判斷最新交易日是否已處理或當日無新資料"""
    if df.empty:
        return True

    latest_date = df.index[-1].strftime("%Y-%m-%d")
    if last_processed_date and latest_date <= last_processed_date:
        return True

    return False
