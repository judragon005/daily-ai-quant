# 🏛️ 每日機構級 AI 股票量化系統 - 協作與規範 (AGENTS.md)

本專案致力於每日台股與美股盤後自動化數據獲取、文藝復興多因子評分 (0-100)、大摩風報比計算 (RRR ≥ 2.0)、AI 機構面審查與興登堡做空一票否決，並透過 GitHub Pages 儀表板與 Telegram Bot 推播晨報。

---

## Agent skills

### Issue tracker
混合採用 GitHub Issues 與本地 .scratch/ Markdown 檔案追蹤。詳見 docs/agents/issue-tracker.md。

### Triage labels
採用 5 大標準分流標籤（含繁體中文雙語標記）：
eeds-triage、
eeds-info、
eady-for-agent、
eady-for-human、wontfix。詳見 docs/agents/triage-labels.md。

### Domain docs
採用單一上下文 (Single-context) 佈局，通用術語定義於根目錄 GLOSSARY.md，架構決策紀錄於 docs/adr/。詳見 docs/agents/domain.md。
