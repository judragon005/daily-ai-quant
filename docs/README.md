# 📚 專案工程文檔 1-to-1 雙向追蹤矩陣 (Traceability Matrix)

本專案貫徹**「單一規格書 (Spec) 1-to-1 完美對應單一架構決策紀錄 (ADR)」**原則：
- **CARD-SPEC (What & How)**：定義最終落地的系統邊界、輸入輸出介面與詳細驗收標準。
- **CARD-ADR (Why & History)**：記錄在同一會話中，透過多次深度對話與辯論演進出的全部推演歷程與決策共識。

---

## 🗂️ 1-to-1 核心對應表

| 卡片編號 (Card ID) | 需求規格書 (Spec - What/How) | 架構決策紀錄 (ADR - Why & Trail) | 包含的歷程里程碑 |
| :--- | :--- | :--- | :--- |
| **CARD-0001** | [CARD-SPEC-0001_Daily_Stock_Quant_System](./spec/CARD-SPEC-0001_Daily_Stock_Quant_System.md) | [CARD-ADR-0001_Daily_Stock_Quant_System_Architecture](./adr/CARD-ADR-0001_Daily_Stock_Quant_System_Architecture.md) | 包含 8 輪決策演進：環境選型 ➔ 股票母池 ➔ 雙軌仲裁 ➔ 交付通道 ➔ Key池 ➔ 防封號 ➔ 專案隔離 ➔ 拒絕過度工程化 (KISS) |

---

## 📂 目錄架構
- **docs/spec/**：存放實施標準規格書。
- **docs/adr/**：存放推演歷程與決策動機。
- **docs/agents/**：存放 Agent Skills 環境約定。
