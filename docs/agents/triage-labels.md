# 分流標籤規範 (Triage Label Vocabulary)

本專案遵循 [80% 簡化技術中文規範 (STE-TW)](../standards/simplified-technical-chinese.md)。

| 標籤名稱 | 中文標籤 | 定義與觸發條件 |
| :--- | :--- | :--- |
| `needs-triage` | **待分流審核** | 新建立之 Issue 或需求。尚未評估範疇與優先順序。 |
| `needs-info` | **需補充資訊** | 需求描述模糊或缺乏邊界。等待人員補充細節。 |
| `ready-for-agent` | **可由 AI 開發** | 規格對齊完畢且驗收標準清晰。AI 可以直接以 TDD 模式開始實作。 |
| `ready-for-human` | **需人類介入** | 涉及機密金鑰配置、付費驗證或重大商業決策。需由人員手動處理。 |
| `wontfix` | **不予處理** | 違反 KISS 原則、過度工程化或超出專案範疇之需求。 |
