"""
單元測試：CARD-07 儀表板資料產生器與展示頁面
遵循 80% 簡化技術中文規範 (STE-TW)
"""
import os
import json
import pytest
from src.c07_dashboard_builder import export_dashboard_json


def test_export_dashboard_json(tmp_path):
    """驗證匯出儀表板 JSON 格式結構與檔案寫入"""
    output_file = str(tmp_path / "latest_tw.json")
    
    macro_data = {
        "index_name": "台灣加權指數 (^TWII)",
        "current_price": 23000.0,
        "ma60": 22500.0,
        "is_bearish": False,
        "status": "BULLISH_NORMAL",
        "alert_msg": "正常多頭格局",
    }
    top_stocks = [
        {
            "symbol": "2330.TW",
            "total_score": 92.5,
            "rrr_levels": {"entry_price": 1050.0, "stop_loss": 980.0, "take_profit": 1190.0, "rrr": 2.0},
            "audit_comment": "基本面與技術面雙強。",
        }
    ]

    export_dashboard_json(
        macro_data=macro_data,
        top_stocks=top_stocks,
        market="TW",
        output_path=output_file,
    )

    assert os.path.exists(output_file)
    with open(output_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["market"] == "TW"
    assert "updated_at" in data
    assert data["macro"]["current_price"] == 23000.0
    assert len(data["stocks"]) == 1
    assert data["stocks"][0]["symbol"] == "2330.TW"
