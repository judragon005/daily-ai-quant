# 📇 [CARD-03] 大盤宏觀雷達與防空警報模組

- **卡片編號**: CARD-03
- **對應模組**: `src/c03_macro_radar.py`
- **狀態**: `ready-for-agent`
- **對應規格**: [CARD-SPEC-0001 (FR-2)](../docs/spec/CARD-SPEC-0001_Daily_Stock_Quant_System.md)
- **寫作規範**: [STE-TW 規範](../docs/standards/simplified-technical-chinese.md)

---

## 1. 任務目標
計算大盤加權指數與標普 500 現價與 60 日均線。產出市場多空溫度指標。

---

## 2. 實作規範與介面定義

1. **大盤資料獲取 (`get_macro_status(market: str) -> dict`)**：
   - 台股追蹤加權指數標的：`^TWII`。
   - 美股追蹤標普 500 指數標的：`^GSPC`。
2. **多空狀態判斷**：
   - 計算指數 60 日簡單移動平均線 (MA60)。
   - 若現價 >= MA60：標註狀態為 `BULLISH_NORMAL`。
   - 若現價 < MA60：標註狀態為 `BEARISH_DEFENSIVE`（空頭防守）。
3. **回傳字典結構**：
   - `index_name`: 指數名稱。
   - `current_price`: 當前點位。
   - `ma60`: 60 日均線點位。
   - `is_bearish`: 布林值（是否跌破季線）。
   - `alert_msg`: 警示字串。

---

## 3. 驗收標準 (Acceptance Criteria)

- [ ] **AC-1 (均線計算)**：傳入 60 日歷史數據。系統正確計算 MA60 數值。
- [ ] **AC-2 (多空狀態判定)**：模擬指數低於 MA60 情境。回傳值 `is_bearish` 必須為 True。
- [ ] **AC-3 (警示格式)**：空頭狀態下。系統產出包含「空頭防守警戒」字樣之字串。
- [ ] **AC-4 (單元測試覆蓋)**：撰寫單元測試 `tests/test_c03_macro_radar.py`。測試全部通過。
