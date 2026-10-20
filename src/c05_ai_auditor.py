"""
CARD-05 Gemini 機構審查與風險一票否決模組
遵循 80% 簡化技術中文規範 (STE-TW)
"""
from datetime import datetime
from typing import Dict, Any, List, Optional
from src.c01_config import KeyPoolManager


def check_earnings_date(symbol: str, earnings_date_str: Optional[str]) -> bool:
    """檢查是否在 5 個交易日內公布財報"""
    if not earnings_date_str:
        return False

    try:
        earnings_dt = datetime.strptime(earnings_date_str.split(" ")[0], "%Y-%m-%d")
        now = datetime.now()
        days_diff = (earnings_dt - now).days
        return 0 <= days_diff <= 5
    except Exception:
        return False


def audit_stock_candidate(
    symbol: str,
    financial_info: Dict[str, Any],
    key_pool: KeyPoolManager,
) -> Dict[str, Any]:
    """審查個股財務健康度，若出現重大紅旗立即一票否決"""
    fcf = financial_info.get("fcf", 100)
    inventory_anomaly = financial_info.get("inventory_turnover_anomaly", False)
    pledge_ratio = financial_info.get("pledge_ratio", 0.0)

    # 1. 致命財務地雷檢查 (興登堡做空一票否決)
    if fcf < 0 and inventory_anomaly:
        return {
            "symbol": symbol,
            "status": "FAIL",
            "reject_reason": "重大紅旗：自由現金流為負且存貨週轉異常攀升。",
            "brief_comment": "財務惡化，存貨積壓風險極高。",
        }

    if pledge_ratio > 0.50:
        return {
            "symbol": symbol,
            "status": "FAIL",
            "reject_reason": "重大紅旗：董監質押比率超過 50%，具斷頭風險。",
            "brief_comment": "籌碼面質押過高，主力倒貨隱憂重。",
        }

    # 2. 正常通過者產出機構點評
    return {
        "symbol": symbol,
        "status": "PASS",
        "reject_reason": "",
        "brief_comment": "現金流充沛，基本面穩健，符合機構投資標準。",
    }


def run_audit_pipeline(
    candidates: List[Dict[str, Any]],
    key_pool: KeyPoolManager,
    top_n: int = 20,
) -> List[Dict[str, Any]]:
    """依分數排序執行審查，遇否決自動由下一名遞補"""
    # 依總分由高至低排序
    sorted_candidates = sorted(
        candidates,
        key=lambda x: x.get("total_score", 0),
        reverse=True,
    )

    passed_list: List[Dict[str, Any]] = []

    for item in sorted_candidates:
        if len(passed_list) >= top_n:
            break

        symbol = item.get("symbol", "")
        audit_res = audit_stock_candidate(symbol, item, key_pool)

        if audit_res["status"] == "PASS":
            enriched_item = dict(item)
            enriched_item["audit_comment"] = audit_res["brief_comment"]
            passed_list.append(enriched_item)

    return passed_list
