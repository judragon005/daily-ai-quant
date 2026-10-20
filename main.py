"""
每日機構級 AI 股票量化系統 - 統一執行入口 (CLI)
遵循 80% 簡化技術中文規範 (STE-TW)
"""
import argparse
import sys
from datetime import datetime

# Windows 終端 UTF-8 編碼相容防護
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

import pandas as pd

from src.c01_config import Config, KeyPoolManager
from src.c02_data_fetcher import (
    fetch_market_candles,
    filter_liquid_stocks,
    is_market_closed,
)
from src.c03_macro_radar import analyze_macro_trend
from src.c04_quant_engine import evaluate_quant_factors
from src.c05_ai_auditor import run_audit_pipeline
from src.c06_telegram_notifier import (
    build_telegram_message,
    send_telegram_broadcast,
)
from src.c07_dashboard_builder import export_dashboard_json


def run_pipeline(market: str = "TW", dry_run: bool = False) -> int:
    """執行完整量化掃描與推播工作流"""
    market = market.upper()
    print(f"[{datetime.now()}] 啟動 {market} 市場量化分析工作流...")

    # 1. 載入環境設定與金鑰池
    config = Config.from_env()
    key_pool = KeyPoolManager(config.gemini_keys or ["mock_default_key"])
    universe = config.tw_universe if market == "TW" else config.us_universe
    index_symbol = "^TWII" if market == "TW" else "^GSPC"

    # 2. 獲取大盤與個股資料 (乾跑模式下建立模擬資料以加速與防斷網)
    if dry_run:
        print("[Dry-Run] 模擬模式：生成測試資料...")
        dates = pd.date_range(end=datetime.now(), periods=65, freq="B")
        macro_df = pd.DataFrame({"Close": [23000.0] * 65}, index=dates)
        
        stock_dfs = {}
        for sym in universe[:10]:
            stock_dfs[sym] = pd.DataFrame(
                {
                    "Open": [100.0] * 65,
                    "High": [105.0] * 65,
                    "Low": [98.0] * 65,
                    "Close": [102.0] * 65,
                    "Volume": [1_000_000] * 65,
                },
                index=dates,
            )
    else:
        print(f"下載大盤指數 {index_symbol} 資料...")
        macro_raw = fetch_market_candles([index_symbol], period="6mo")
        macro_df = macro_raw[index_symbol] if index_symbol in macro_raw else macro_raw
        
        print(f"下載 {len(universe)} 檔母池標的資料...")
        candles_raw = fetch_market_candles(universe, period="6mo")
        stock_dfs = {}
        for sym in universe:
            if sym in candles_raw:
                stock_dfs[sym] = candles_raw[sym]

    # 3. 休市判定
    if not dry_run and is_market_closed(macro_df):
        print(f"[{datetime.now()}] {market} 市場本日休市或無新資料，系統正常結束。")
        return 0

    # 4. 分析大盤季線雷達
    macro_status = analyze_macro_trend(macro_df, market=market)
    print(f"大盤狀態：{macro_status.get('alert_msg')}")

    # 5. 初篩流動性
    liquid_symbols = filter_liquid_stocks(stock_dfs, market=market)
    print(f"流動性初篩通過：{len(liquid_symbols)} 檔")

    # 6. 計算多因子評分與風報比點位
    quant_candidates = []
    for sym in liquid_symbols:
        df = stock_dfs.get(sym, pd.DataFrame())
        factors = evaluate_quant_factors(sym, df, market=market)
        quant_candidates.append(factors)

    # 7. 執行機構審查與風險一票否決
    final_top20 = run_audit_pipeline(quant_candidates, key_pool, top_n=20)
    print(f"機構審查完成，最終精選：{len(final_top20)} 檔")

    # 8. 匯出儀表板 JSON
    report_date = datetime.now().strftime("%Y-%m-%d")
    out_file = f"docs/data/latest_{market.lower()}.json"
    export_dashboard_json(
        macro_data=macro_status,
        top_stocks=final_top20,
        market=market,
        output_path=out_file,
    )
    print(f"儀表板資料已儲存至 {out_file}")

    # 9. 組合 Telegram 晨報並推播
    tg_message = build_telegram_message(
        macro_data=macro_status,
        top_stocks=final_top20,
        market=market,
        report_date=report_date,
    )
    if dry_run:
        print("\n--- [Telegram 推播預覽] ---")
        print(tg_message[:300] + "\n...(長度已受保護)")
    else:
        send_telegram_broadcast(
            bot_token=config.telegram_bot_token,
            chat_id=config.telegram_chat_id,
            message=tg_message,
        )

    print(f"[{datetime.now()}] {market} 執行完成！")
    return 0


def main():
    parser = argparse.ArgumentParser(description="每日機構級 AI 股票量化系統")
    parser.add_argument(
        "--market",
        type=str,
        default="TW",
        choices=["TW", "US"],
        help="指定市場類別 (TW: 台股, US: 美股)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="模擬執行模式 (不下載即時數據與不發送真實推播)",
    )
    args = parser.parse_args()

    exit_code = run_pipeline(market=args.market, dry_run=args.dry_run)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
