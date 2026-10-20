"""
單元測試：CARD-05 Gemini 機構審查與風險一票否決模組
遵循 80% 簡化技術中文規範 (STE-TW)
"""
from datetime import datetime, timedelta
import pytest
from src.c01_config import KeyPoolManager
from src.c05_ai_auditor import (
    audit_stock_candidate,
    check_earnings_date,
    run_audit_pipeline,
)


def test_audit_stock_candidate_pass():
    """驗證財務正常之標的通過審查"""
    key_pool = KeyPoolManager(["mock_key_1"])
    good_stock = {
        "symbol": "2330.TW",
        "fcf": 500_000_000,
        "inventory_turnover_anomaly": False,
        "pledge_ratio": 0.05,
    }
    result = audit_stock_candidate("2330.TW", good_stock, key_pool)
    assert result["status"] == "PASS"
    assert result["reject_reason"] == ""
    assert len(result["brief_comment"]) > 0


def test_audit_stock_candidate_fail():
    """驗證觸發紅旗地雷之標的遭到一票否決"""
    key_pool = KeyPoolManager(["mock_key_1"])
    bad_stock = {
        "symbol": "TRAP.TW",
        "fcf": -100_000_000,
        "inventory_turnover_anomaly": True,
        "pledge_ratio": 0.60, # 質押高達 60%
    }
    result = audit_stock_candidate("TRAP.TW", bad_stock, key_pool)
    assert result["status"] == "FAIL"
    assert "重大紅旗" in result["reject_reason"] or "高風險" in result["reject_reason"]


def test_check_earnings_date_warning():
    """驗證財報公布日小於等於 5 日觸發預警標籤"""
    today = datetime.now()
    near_earnings = (today + timedelta(days=3)).strftime("%Y-%m-%d")
    far_earnings = (today + timedelta(days=30)).strftime("%Y-%m-%d")

    assert check_earnings_date("TEST", near_earnings) is True
    assert check_earnings_date("TEST", far_earnings) is False
    assert check_earnings_date("TEST", None) is False


def test_run_audit_pipeline_replenishment():
    """驗證否決時下一名標的自動遞補以補足名額"""
    key_pool = KeyPoolManager(["mock_key"])
    # 建立 4 檔標的，第 2 檔為地雷股
    candidates = [
        {"symbol": "S1", "total_score": 95, "fcf": 100, "inventory_turnover_anomaly": False, "pledge_ratio": 0.1},
        {"symbol": "S2_BAD", "total_score": 90, "fcf": -100, "inventory_turnover_anomaly": True, "pledge_ratio": 0.8},
        {"symbol": "S3", "total_score": 85, "fcf": 100, "inventory_turnover_anomaly": False, "pledge_ratio": 0.1},
        {"symbol": "S4", "total_score": 80, "fcf": 100, "inventory_turnover_anomaly": False, "pledge_ratio": 0.1},
    ]

    # 目標選取 2 檔
    passed_list = run_audit_pipeline(candidates, key_pool, top_n=2)
    assert len(passed_list) == 2
    symbols = [item["symbol"] for item in passed_list]
    # S2_BAD 被否決，由 S3 遞補
    assert symbols == ["S1", "S3"]
