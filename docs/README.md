# 📚 專案工程文檔雙向追蹤矩陣 (Documentation Traceability Matrix)

本專案採用**卡片式記憶法 (Card-Index)** 管理架構決策紀錄 (ADR) 與需求規格書 (Spec)，確保「決策原因 (Why)」與「實施規格 (What/How)」100% 雙向對應可追蹤。

---

## 🗂️ ADR ⇄ 規格書 橫向對照表

| 卡片編號 (Card ID) | 架構決策紀錄 (ADR - 決策原因 Why) | 對應需求規格書 (Spec - 實施規範 What/How) | 核心規範範疇 |
| :--- | :--- | :--- | :--- |
| **CARD-0001** | [CARD-ADR-0001_Dual_Track_Architecture](./adr/CARD-ADR-0001_Dual_Track_Architecture.md) | [CARD-SPEC-0001_Daily_Stock_Quant_System](./spec/CARD-SPEC-0001_Daily_Stock_Quant_System.md) | 雙軌量化仲裁、GitHub Actions 防封號機制、雙通道交付 |
| **CARD-0002** | [CARD-ADR-0002_Microstructure_Guardrails](./adr/CARD-ADR-0002_Microstructure_Guardrails.md) | [CARD-SPEC-0001_Daily_Stock_Quant_System](./spec/CARD-SPEC-0001_Daily_Stock_Quant_System.md) | 除權息復權還原 (uto_adjust=True)、大盤季線溫度計、休市日阻斷、向下整張截斷 |

---

## 📂 資料夾職責劃分
- **docs/spec/ (規格書資料夾)**：存放具體的產品需求、系統邊界、輸入輸出介面與詳細驗收標準 (Acceptance Criteria)。
- **docs/adr/ (架構決策紀錄資料夾)**：存放重大技術選型與架構考量背後的「決策動機 (Context)」、「權衡 (Trade-offs)」與「影響 (Consequences)」。
- **docs/agents/ (Agent 配置資料夾)**：存放 Agent Skills 所需的環境約束 (Issue Tracker, Triage 標籤, 領域架構)。
