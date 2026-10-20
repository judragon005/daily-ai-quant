"""
CARD-07 儀表板資料產生器
遵循 80% 簡化技術中文規範 (STE-TW)
"""
import json
import os
from datetime import datetime
from typing import Dict, Any, List


def export_dashboard_json(
    macro_data: Dict[str, Any],
    top_stocks: List[Dict[str, Any]],
    market: str = "TW",
    output_path: str = "docs/data/latest_tw.json",
) -> None:
    """將量化篩選與審查成果匯出至 JSON 檔案"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    payload = {
        "market": market.upper(),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "macro": macro_data,
        "stocks": top_stocks,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
