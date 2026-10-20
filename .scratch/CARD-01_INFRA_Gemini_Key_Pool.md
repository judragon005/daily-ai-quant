# 📇 [CARD-01] 系統環境配置與 Gemini API 金鑰池管理

- **卡片編號**: CARD-01
- **對應模組**: `src/c01_config.py`
- **狀態**: `ready-for-agent`
- **對應規格**: [CARD-SPEC-0001 (FR-4.1)](../docs/spec/CARD-SPEC-0001_Daily_Stock_Quant_System.md)
- **寫作規範**: [STE-TW 規範](../docs/standards/simplified-technical-chinese.md)

---

## 1. 任務目標
實作環境變數讀取與 API 金鑰輪詢機制。金鑰遇到限流時自動切換。

---

## 2. 實作規範與介面定義

1. **環境變數載入**：
   - 讀取 `GEMINI_API_KEYS`（以逗號分隔多組金鑰）。
   - 讀取 `TELEGRAM_BOT_TOKEN` 與 `TELEGRAM_CHAT_ID`。
2. **金鑰輪詢類別 (`KeyPoolManager`)**：
   - 提供 `get_next_key() -> str` 輪流回傳金鑰。
   - 提供 `mark_key_rate_limited(key: str)` 標記金鑰進入冷卻。
3. **股票母池配置**：
   - 台股初選名單：臺灣 50 與中型 100 代碼陣列。
   - 美股初選名單：標普 500 與那斯達克 100 代碼陣列。

---

## 3. 驗收標準 (Acceptance Criteria)

- [ ] **AC-1 (多金鑰解析)**：輸入包含 3 組金鑰之字串。系統正確解析為包含 3 個項目的清單。
- [ ] **AC-2 (輪詢機制驗證)**：連續呼叫 `get_next_key()` 4 次。系統依序產出金鑰，並在第 4 次回到第 1 組。
- [ ] **AC-3 (限流自動切換)**：當標記目前金鑰 429 限流時。系統自動跳過該金鑰並取用下一組有效金鑰。
- [ ] **AC-4 (單元測試覆蓋)**：撰寫單元測試 `tests/test_c01_config.py`。測試全部通過。
