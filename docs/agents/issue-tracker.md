# Issue Tracker Configuration

## 追蹤器類型
- **混合模式 (Hybrid Mode)**: GitHub Issues + 本地 Markdown (.scratch/)

## 操作指引
1. **日常草稿與微小單元**：
   - 技能（如 /to-tickets）可在專案目錄 .scratch/<feature>/ticket-<id>.md 建立本地票券檔案，免連網且極速讀寫。
2. **正式里程碑與團隊任務**：
   - 當專案連結至 GitHub 遠端後，使用 GitHub CLI (gh issue create, gh issue list) 建立與同步 Issues。
3. **PR 關聯**：
   - Pull Request 預設不作為公開 Triage 輸入隊列，僅在代碼審查通過後合併。
