"""
單元測試：CARD-08 統一執行入口與整合工作流
遵循 80% 簡化技術中文規範 (STE-TW)
"""
import pytest
from main import run_pipeline


def test_main_pipeline_dry_run_tw():
    """驗證台股工作流在 Dry-Run 模式下完整走通"""
    exit_code = run_pipeline(market="TW", dry_run=True)
    assert exit_code == 0


def test_main_pipeline_dry_run_us():
    """驗證美股工作流在 Dry-Run 模式下完整走通"""
    exit_code = run_pipeline(market="US", dry_run=True)
    assert exit_code == 0
