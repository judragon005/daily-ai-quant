# 📇 [CARD-08] GitHub Actions 錯峰排程與自動化防護

- **卡片編號**: CARD-08
- **對應模組**: `.github/workflows/daily_quant.yml`
- **狀態**: `ready-for-agent`
- **對應規格**: [CARD-SPEC-0001 (FR-1, FR-5)](../docs/spec/CARD-SPEC-0001_Daily_Stock_Quant_System.md)
- **寫作規範**: [STE-TW 規範](../docs/standards/simplified-technical-chinese.md)

---

## 1. 任務目標
配置定時觸發之 GitHub Actions 工作流。加入安全防護機制，防範帳號停權。

---

## 2. 實作規範與介面定義

1. **排程設定 (Cron Schedule)**：
   - 台股排程：UTC 08:17（台灣時間 16:17 盤後）。
   - 美股排程：UTC 21:23（台灣時間 05:23 盤後）。
   - 支援 `workflow_dispatch` 手動觸發。
   - 禁止監聽 `on: push` 事件。
2. **安全防護設定**：
   - 建立虛擬環境並安裝 `requirements.txt`。
   - 注入 Secrets：`GEMINI_API_KEYS`、`TELEGRAM_BOT_TOKEN`、`TELEGRAM_CHAT_ID`。
   - 資料更新後執行 Commit。訊息一律包含 `[skip ci]` 標籤。
   - 設定單次執行超時限制：`timeout-minutes: 10`。

---

## 3. 驗收標準 (Acceptance Criteria)

- [ ] **AC-1 (YAML 語法校驗)**：Workflow YAML 語法合法無誤。
- [ ] **AC-2 (迴圈防護標籤)**：Git Commit 步驟必定帶有 `[skip ci]` 標記。
- [ ] **AC-3 (執行時間限制)**：工作流設定超時限制。執行時間不超過免費配額。
