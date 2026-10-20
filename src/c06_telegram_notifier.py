"""
CARD-06 Telegram 晨報摘要推播模組
遵循 80% 簡化技術中文規範 (STE-TW)
"""
import json
import urllib.parse
import urllib.request
from typing import Dict, Any, List


def build_telegram_message(
    macro_data: Dict[str, Any],
    top_stocks: List[Dict[str, Any]],
    market: str = "TW",
    report_date: str = "",
) -> str:
    """建構 Telegram 晨報 Markdown 卡片，長度限制小於 3500 字元"""
    market_title = "台股市場 (TW)" if market.upper() == "TW" else "美股市場 (US)"
    lines = [
        f"🏛️ *【每日機構級 AI 股票量化晨報 - {market_title}】*",
        f"📅 日期：`{report_date}`",
        "────────────────────",
        f"📊 *大盤宏觀溫度計*：",
        f"• 指數：{macro_data.get('index_name', '')}",
        f"• 現價：`{macro_data.get('current_price', 0.0)}` | 季線 (MA60)：`{macro_data.get('ma60', 0.0)}`",
        f"• 狀態：{macro_data.get('alert_msg', '')}",
        "────────────────────",
        f"🏆 *黃金 Top 20 推薦清單 (風報比 RRR ≥ 2.0)*：",
        "`序  標的     評分  進場   停損   目標`",
    ]

    for idx, item in enumerate(top_stocks[:20], 1):
        sym = item.get("symbol", "").replace(".TW", "")
        score = item.get("total_score", 0.0)
        rrr = item.get("rrr_levels", {})
        entry = rrr.get("entry_price", 0.0)
        sl = rrr.get("stop_loss", 0.0)
        tp = rrr.get("take_profit", 0.0)
        lines.append(f"`{idx:02d}  {sym:<8} {score:<5.1f} {entry:<6.1f} {sl:<6.1f} {tp:<6.1f}`")

    lines.append("────────────────────")
    lines.append("🔍 *Top 3 機構審查點評*：")
    for idx, item in enumerate(top_stocks[:3], 1):
        sym = item.get("symbol", "")
        comment = item.get("audit_comment", "基本面穩健。")
        lines.append(f"*{idx}. {sym}*：{comment}")

    lines.append("────────────────────")
    lines.append("🌐 *完整儀表板*：[點此查看詳細數據與圖表](https://judragon005.github.io/daily-ai-quant)")
    lines.append("⚠️ *免責聲明*：本報告由量化模型產出，僅供研究參考，非投資建議。")

    full_text = "\n".join(lines)
    # 嚴格截斷防護，防範 Telegram 400 錯誤
    if len(full_text) > 3500:
        full_text = full_text[:3490] + "\n...(略)"

    return full_text


def send_telegram_broadcast(
    bot_token: str,
    chat_id: str,
    message: str,
) -> bool:
    """呼叫 Telegram API 發送廣播推播"""
    if not bot_token or not chat_id:
        print("[Telegram] 未配置 Token 或 Chat ID，略過推播發送。")
        return True

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return bool(resp.status == 200)
    except Exception as e:
        print(f"[Telegram] 發送失敗：{e}")
        return False
