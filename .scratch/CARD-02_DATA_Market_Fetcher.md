# 📇 [CARD-02] 雙市場股價資料下載與除權息還原

- **卡片編號**: CARD-02
- **對應模組**: `src/c02_data_fetcher.py`
- **狀態**: `ready-for-agent`
- **對應規格**: [CARD-SPEC-0001 (FR-1)](../docs/spec/CARD-SPEC-0001_Daily_Stock_Quant_System.md)
- **寫作規範**: [STE-TW 規範](../docs/standards/simplified-technical-chinese.md)

---

## 1. 任務目標
批次下載台股與美股母池日 K 線資料。執行除權息價格還原。自動判定市場休市日。

---

## 2. 實作規範與介面定義

1. **批次下載函式 (`fetch_market_candles(symbols, period="1y") -> pd.DataFrame`)**：
   - 呼叫 `yfinance.download()` 批次抓取。
   - 強制帶入 `auto_adjust=True` 參數。消除除權息假跳空。
2. **市場流動性初篩 (`filter_liquid_stocks(df, market) -> list[str]`)**：
   - 台股條件：收盤價 > 10 元，近 20 日均成交額 > 5000 萬元。
   - 美股條件：收盤價 > 5 美元，近 20 日均成交額 > 1500 萬美元。
3. **休市阻斷函式 (`is_market_closed(df) -> bool`)**：
   - 檢查最新 K 線日期是否小於等於已處理日期。
   - 若為休市日，系統印出休市訊息並回傳 True。

---

## 3. 驗收標準 (Acceptance Criteria)

- [ ] **AC-1 (除權息還原)**：下載包含除權息股票歷史資料。檢查收盤價序列無人為斷崖。
- [ ] **AC-2 (流動性篩選)**：傳入測試股票清單。系統正確剔除低成交量與雞蛋水餃股。
- [ ] **AC-3 (休市退出)**：傳入歷史資料模擬非交易日。程式偵測休市並回傳 True。
- [ ] **AC-4 (單元測試覆蓋)**：撰寫單元測試 `tests/test_c02_data_fetcher.py`。測試全部通過。
