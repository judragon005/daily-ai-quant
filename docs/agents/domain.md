# Domain Docs Configuration

## 結構配置
- **模式**: 單一上下文 (Single-context)
- **術語表位置**: 專案根目錄 GLOSSARY.md
- **架構決策紀錄 (ADR) 目錄**: docs/adr/ (命名格式: docs/adr/NNNN-<decision-title>.md)

## 讀取與更新約定
- Agent 在進行架構規劃 (/codebase-design) 或技術拷問 (/grill-with-docs) 時，必須優先查閱 GLOSSARY.md 與 docs/adr/。
- 重大技術變更（如替換爬蟲源、調整多因子權重公式）必須新增 ADR。
