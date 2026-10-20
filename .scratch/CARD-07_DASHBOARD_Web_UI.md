# 📇 [CARD-07] 儀表板資料產生器與前端展示頁面

- **卡片編號**: CARD-07
- **對應模組**: `src/c07_dashboard_builder.py` 與 `docs/index.html`
- **狀態**: `ready-for-agent`
- **對應規格**: [CARD-SPEC-0001 (FR-5.2)](../docs/spec/CARD-SPEC-0001_Daily_Stock_Quant_System.md)
- **寫作規範**: [STE-TW 規範](../docs/standards/simplified-technical-chinese.md)

---

## 1. 任務目標
將量化與審查成果匯出至 JSON 資料檔。實作極簡深色主題之響應式前端儀表板。

---

## 2. 實作規範與介面定義

1. **資料產出模組 (`src/c07_dashboard_builder.py`)**：
   - 函式 `export_dashboard_json(results_data, market: str, output_path: str)`。
   - 台股產出：`docs/data/latest_tw.json`。
   - 美股產出：`docs/data/latest_us.json`。
   - 欄位包含：大盤現價、更新時間、20 檔標的多因子分數、ATR 點位、機構點評。
2. **前端頁面 (`docs/index.html`)**：
   - 採用原生 HTML5、CSS 與 JavaScript。無外部重量級框架相依。
   - 深色主題配色，手機與桌機版面自動切換。
   - 支援「台股 (TW)」與「美股 (US)」雙分頁切換。
   - 提供搜尋與依多因子分數排序功能。

---

## 3. 驗收標準 (Acceptance Criteria)

- [ ] **AC-1 (資料結構合格)**：產出的 JSON 檔案能被有效解析。必要欄位無缺漏。
- [ ] **AC-2 (分頁切換正常)**：於瀏覽器開啟 `docs/index.html`。點擊台美股切換按鈕，資料正確更換。
- [ ] **AC-3 (響應式呈現)**：模擬手機寬度 (375px)。表格支援橫向捲動，排版不破版。
- [ ] **AC-4 (單元測試覆蓋)**：撰寫單元測試 `tests/test_c07_dashboard_builder.py`。測試全部通過。
