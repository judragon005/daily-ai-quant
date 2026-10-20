# 1. 採納架構決策紀錄 (ADR) 與雙軌交叉量化選股機制

Date: 2026-10-20

## Status
Accepted

## 對應規格書 (Specification)
- [CARD-SPEC-0001](../spec/CARD-SPEC-0001_每日機構級AI股票量化系統規格書.md)

## Context
本系統需要在每日台股與美股收盤後，於隔晨 08:00 前自動化產出 20 檔兼具 0-100 量化高分、風報比 $\ge 2.0$ 且通過機構做空審判的可投資標的，並推播至 Telegram 與發布至 GitHub Pages。
需兼顧 100% 免費、避免 GitHub Actions 封號與 API Rate Limit。

## Decision
1. 採用 GitHub Actions 定時排程，以「靜態數據生成與 GitHub Pages 構建」為 CI/CD 語意，完全禁用 on: push 防範無限遞迴迴圈。
2. 採用「分層指數 + 流動性標準」初篩母池（美股 S&P500+Nasdaq100 約 550 檔，台股 0050+中型100 約 350 檔）。
3. 採用雙軌仲裁：軌道一純量化多因子 + 軌道二 Gemini 機構審查，強制執行興登堡做空一票否決。
4. 設定與任務追蹤器採用 Matt Pocock 體系之 GitHub Issues + 本地 .scratch/ 混合架構。

## Consequences
- 架構高度模組化且具備強防禦力。
- 零雲端伺服器維護成本，100% 免費安全。
