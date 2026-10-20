# 🤝 專案上下文交接與維護指南 (HANDOFF.md)

本文件遵循 [80% 簡化技術中文規範 (STE-TW)](./standards/simplified-technical-chinese.md)。

---

## 1. 專案現狀總結 (Project Current State)

本專案已完成閉環開發工作流之全部 8 大模組實作與代碼審查：
- **版本**: v1.0.0
- **儲存庫**: `judragon005/daily-ai-quant`
- **測試狀態**: 25/25 項單元測試 100% 通過（執行耗時約 1.1 秒）。
- **架構原則**: 100% 無狀態設計 (Stateless)、零自建伺服器、全自動錯峰 GitHub Actions 排程。

---

## 2. 關鍵文檔索引 (Key Artifacts)

| 類型 | 文件路徑 | 說明 |
| :--- | :--- | :--- |
| **產品規格 (PRD)** | [`docs/spec/CARD-SPEC-0001_Daily_Stock_Quant_System.md`](./spec/CARD-SPEC-0001_Daily_Stock_Quant_System.md) | 包含 5 大功能需求與 6 項驗收標準。 |
| **架構決策 (ADR)** | [`docs/adr/CARD-ADR-0001_Daily_Stock_Quant_System_Architecture.md`](./adr/CARD-ADR-0001_Daily_Stock_Quant_System_Architecture.md) | 包含 8 大核心決策推演歷程。 |
| **技術寫作標準** | [`docs/standards/simplified-technical-chinese.md`](./standards/simplified-technical-chinese.md) | STE-TW 簡化技術中文規則。 |
| **Git 工作流規範** | [`docs/standards/git-workflow.md`](./standards/git-workflow.md) | 分支開發、本地雙門禁、CI 與大掃除 SOP。 |
| **任務分流看板** | [`.scratch/README.md`](../.scratch/README.md) | CARD-01 至 CARD-08 全部標記為 `done`。 |
| **展示儀表板** | [`docs/index.html`](./index.html) | 現代深色響應式戰情室前端。 |

---

## 3. 人類待辦事項 (Ready-for-Human Checklist)

若要啟用雲端 GitHub Actions 每日定時推播，請至 GitHub 儲存庫設定 Secrets：
前往：`https://github.com/judragon005/daily-ai-quant/settings/secrets/actions`
1. **`GEMINI_API_KEYS`**：輸入一組或多組 Gemini API 金鑰（以逗號分隔）。
2. **`TELEGRAM_BOT_TOKEN`**：輸入由 Telegram @BotFather 取得之 Bot Token。
3. **`TELEGRAM_CHAT_ID`**：輸入接收推播之個人或頻道 Chat ID。

---

## 4. 模組維護與執行指令 (Runbook)

- **執行全量單元測試**：
  ```bash
  python -m pytest tests/
  ```
- **本機模擬乾跑 (Dry-Run)**：
  ```bash
  python main.py --market TW --dry-run
  python main.py --market US --dry-run
  ```
- **本機真實執行 (需連網與金鑰)**：
  ```bash
  python main.py --market TW
  ```

---

## 5. 未來 Agent 接手推薦技能 (Suggested Skills)

未來的 AI 代理在接手本專案時，建議優先啟用以下技能：
1. **`02_Defensive Development`**：避免修改單一模組時破壞其他模組之風報比與評分計算。
2. **`git-guardrails-claude-code`**：防範非預期的破壞性 Git 操作，確保 `master` 分支穩定。
3. **`03_Unit Test Master`**：任何新增特徵因子時，強制執行紅綠循環測試。
