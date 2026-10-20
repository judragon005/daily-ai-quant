# 📇 [CARD-06] Telegram 晨報摘要推播模組

- **卡片編號**: CARD-06
- **對應模組**: `src/c06_telegram_notifier.py`
- **狀態**: `ready-for-agent`
- **對應規格**: [CARD-SPEC-0001 (FR-5.1)](../docs/spec/CARD-SPEC-0001_Daily_Stock_Quant_System.md)
- **寫作規範**: [STE-TW 規範](../docs/standards/simplified-technical-chinese.md)

---

## 1. 任務目標
組合晨報 Markdown 訊息卡片。呼叫 Telegram Bot API 完成推播。字串長度小於 3500 字元。

---

## 2. 實作規範與介面定義

1. **訊息排版函式 (`build_telegram_message(macro_data, stocks_data, report_date) -> str`)**：
   - 頂部：大盤點位與多空防守警示。
   - 中段：精選前 20 檔代碼、多因子分數、進場價與停損目標點位簡表。
   - 深度點評：挑選前 3 名機構審查評語（每檔 50 字以內）。
   - 底部：附帶 GitHub Pages 儀表板連結。
   - 限制：總長度小於 3500 字元，避免觸發 Telegram 400 錯誤。
2. **發布函式 (`send_telegram_broadcast(message_text: str) -> bool`)**：
   - 讀取環境變數 `TELEGRAM_BOT_TOKEN` 與 `TELEGRAM_CHAT_ID`。
   - 使用 HTTPS POST 發送請求。傳入 `parse_mode="Markdown"`。
   - 若發送失敗，提供重試機制（重試 3 次）。

---

## 3. 驗收標準 (Acceptance Criteria)

- [ ] **AC-1 (字數門禁)**：產生完整 20 檔股票之推播字串。長度驗證小於 3500 字元。
- [ ] **AC-2 (格式解析)**：模擬推播發布。Markdown 特殊符號（如 `_`, `*`, `[`）經過正確轉義。
- [ ] **AC-3 (重試容錯)**：模擬網路連線異常。系統自動重試並記錄日誌。
- [ ] **AC-4 (單元測試覆蓋)**：撰寫單元測試 `tests/test_c06_telegram_notifier.py`。測試全部通過。
