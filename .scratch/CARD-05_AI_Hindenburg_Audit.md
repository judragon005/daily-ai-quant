# 📇 [CARD-05] Gemini 機構審查與風險一票否決模組

- **卡片編號**: CARD-05
- **對應模組**: `src/c05_ai_auditor.py`
- **狀態**: `done`
- **對應規格**: [CARD-SPEC-0001 (FR-4)](../docs/spec/CARD-SPEC-0001_Daily_Stock_Quant_System.md)
- **寫作規範**: [STE-TW 規範](../docs/standards/simplified-technical-chinese.md)

---

## 1. 任務目標
呼叫 Gemini API 審查候選標的。若發現財務舞弊或暴雷風險，直接否決並剔除。標註財報公布倒數。

---

## 2. 實作規範與介面定義

1. **機構審查函式 (`audit_stock_candidate(symbol: str, financial_info: dict) -> dict`)**：
   - 整合 `KeyPoolManager` 取得金鑰。
   - 審查項目：自由現金流負值、存貨異常攀升、大股東質押比率。
   - 回傳審查結論：`status` ('PASS' 或 'FAIL')、`reject_reason` (字串)、`brief_comment` (50 字以內摘要)。
2. **財報前夕預警函式 (`check_earnings_date(symbol: str) -> bool`)**：
   - 抓取下次財報公布日期。
   - 若公布日在 5 個交易日內，標記警示標籤 `[⚠️ 財報前夕]`。
3. **名單遞補機制 (`run_audit_pipeline(candidates_df, top_n=20) -> list[dict]`)**：
   - 審查依評分由高至低進行。
   - 若標的被否決，由下一名自動遞補，直到選滿指定名額。

---

## 3. 驗收標準 (Acceptance Criteria)

- [x] **AC-1 (否決機制生效)**：模擬輸入具有重大紅旗之標的。系統回傳 `FAIL` 並排除該標的。
- [x] **AC-2 (財報日標註)**：模擬即將公布財報標的。輸出結果包含「財報前夕」警示標籤。
- [x] **AC-3 (名額補足)**：候選清單中若有 2 檔被否決。最終輸出仍補滿 20 檔合格標的。
- [x] **AC-4 (單元測試覆蓋)**：撰寫單元測試 `tests/test_c05_ai_auditor.py`。測試全部通過。
