"""
單元測試：CARD-06 Telegram 晨報摘要推播模組
遵循 80% 簡化技術中文規範 (STE-TW)
"""
import pytest
from unittest.mock import patch, MagicMock
from src.c06_telegram_notifier import (
    build_telegram_message,
    send_telegram_broadcast,
)


def test_build_telegram_message_length_and_structure():
    """驗證晨報訊息結構完整且長度小於 3500 字元"""
    macro_data = {
        "index_name": "台灣加權指數 (^TWII)",
        "current_price": 23000.0,
        "ma60": 22500.0,
        "is_bearish": False,
        "alert_msg": "🟢 [正常多頭格局] 台灣加權指數 現價維持在季線之上。",
    }
    
    # 產生滿編 20 檔股票清單
    top_stocks = []
    for i in range(1, 21):
        top_stocks.append({
            "symbol": f"{2300+i}.TW",
            "total_score": round(95.0 - (i * 1.5), 1),
            "rrr_levels": {
                "entry_price": 100.0 + i,
                "stop_loss": 90.0 + i,
                "take_profit": 120.0 + i,
                "rrr": 2.0,
            },
            "audit_comment": f"第 {i} 名標的，技術動能強勁且財務指標健全。",
        })

    msg = build_telegram_message(macro_data, top_stocks, market="TW", report_date="2026-10-20")
    
    # 驗證字數門禁
    assert len(msg) < 3500
    # 驗證結構必要關鍵字
    assert "每日機構級 AI 股票量化晨報" in msg
    assert "台灣加權指數" in msg
    assert "Top 20" in msg
    assert "https://judragon005.github.io/daily-ai-quant" in msg


@patch("urllib.request.urlopen")
def test_send_telegram_broadcast_success(mock_urlopen):
    """驗證 Telegram 發送 API 正常呼叫"""
    mock_resp = MagicMock()
    mock_resp.status = 200
    mock_urlopen.return_value.__enter__.return_value = mock_resp

    result = send_telegram_broadcast(
        bot_token="mock_token",
        chat_id="mock_chat_id",
        message="測試推播訊息",
    )
    assert result is True
    mock_urlopen.assert_called_once()


def test_send_telegram_broadcast_dry_run():
    """驗證無 Token 時安全略過不拋出例外"""
    result = send_telegram_broadcast(bot_token="", chat_id="", message="測試")
    assert result is True
