# 📇 [CARD-04] 多因子評分矩陣與風報比計算引擎

- **卡片編號**: CARD-04
- **對應模組**: `src/c04_quant_engine.py`
- **狀態**: `ready-for-agent`
- **對應規格**: [CARD-SPEC-0001 (FR-3)](../docs/spec/CARD-SPEC-0001_Daily_Stock_Quant_System.md)
- **寫作規範**: [STE-TW 規範](../docs/standards/simplified-technical-chinese.md)

---

## 1. 任務目標
計算個股 0 至 100 分量化多因子總分。計算 2 倍 ATR 停損目標點位。輸出初篩清單。

---

## 2. 實作規範與介面定義

1. **多因子評分函式 (`calculate_factor_scores(df_dict) -> pd.DataFrame`)**：
   - 價值因子 (30%)：計算本益比 (PE) 與股價淨值比 (PB)。
   - 品質因子 (25%)：計算股東權益報酬率 (ROE) 與毛利率。
   - 動能因子 (20%)：判斷均線排列 (MA20/50/200)。計算 14 日 RSI。
   - 市場特徵 (25%)：計算營收動能與相對大盤強度。
   - 輸出正規化後 0 至 100 分加權分數。
2. **大摩風報比計算 (`calculate_rrr_levels(price, atr14) -> dict`)**：
   - 停損價 = 現價 - (2 × ATR)。
   - 目標價 = 現價 + (2 × (現價 - 停損價))。
   - 風報比 (RRR) 固定設定為 2.0。
3. **部位建議計算 (`calculate_position_size(price, stop_loss, capital=1000000, risk_pct=0.01) -> int`)**：
   - 買進股數 = `(capital × risk_pct) / (price - stop_loss)`。
   - 台股建議部位向下整數截斷至整張 (1000 股)。

---

## 3. 驗收標準 (Acceptance Criteria)

- [ ] **AC-1 (分數邊界)**：傳入股票資料集。所有標的多因子總分介於 0 到 100 之間。
- [ ] **AC-2 (風報比約束)**：計算產出之點位。所有標的之風報比嚴格等於 2.0。
- [ ] **AC-3 (部位風險限制)**：計算部位結果。單筆停損金額不大於總資本的 1%。
- [ ] **AC-4 (單元測試覆蓋)**：撰寫單元測試 `tests/test_c04_quant_engine.py`。測試全部通過。
