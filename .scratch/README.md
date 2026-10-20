# 🗂️ 任務票券索引表 (Task Tickets Master)

本專案所有任務採用卡片索引管理法 (Card-Index)。每張任務卡片具備獨立編號、權責模組與驗收條件。  
所有文件遵循 [80% 簡化技術中文規範 (STE-TW)](../docs/standards/simplified-technical-chinese.md)。

| 卡片編號 | 任務標題 | 任務卡片檔案 | 對應模組檔案 | 狀態 |
| :--- | :--- | :--- | :--- | :--- |
| **CARD-01** | 環境配置與 API 金鑰池管理 | [`CARD-01_INFRA_Gemini_Key_Pool.md`](./CARD-01_INFRA_Gemini_Key_Pool.md) | `src/c01_config.py` | `ready-for-agent` |
| **CARD-02** | 雙市場資料下載與除權息還原 | [`CARD-02_DATA_Market_Fetcher.md`](./CARD-02_DATA_Market_Fetcher.md) | `src/c02_data_fetcher.py` | `ready-for-agent` |
| **CARD-03** | 大盤雷達與防空警報模組 | [`CARD-03_MACRO_Market_Radar.md`](./CARD-03_MACRO_Market_Radar.md) | `src/c03_macro_radar.py` | `ready-for-agent` |
| **CARD-04** | 多因子評分與風報比計算引擎 | [`CARD-04_QUANT_Multi_Factor_RRR.md`](./CARD-04_QUANT_Multi_Factor_RRR.md) | `src/c04_quant_engine.py` | `ready-for-agent` |
| **CARD-05** | Gemini 機構審查與風險否決 | [`CARD-05_AI_Hindenburg_Audit.md`](./CARD-05_AI_Hindenburg_Audit.md) | `src/c05_ai_auditor.py` | `ready-for-agent` |
| **CARD-06** | Telegram 晨報摘要推播模組 | [`CARD-06_DELIVERY_Telegram_Card.md`](./CARD-06_DELIVERY_Telegram_Card.md) | `src/c06_telegram_notifier.py` | `ready-for-agent` |
| **CARD-07** | 儀表板資料產生器與展示頁面 | [`CARD-07_DASHBOARD_Web_UI.md`](./CARD-07_DASHBOARD_Web_UI.md) | `docs/index.html & src/c07_dashboard_builder.py` | `ready-for-agent` |
| **CARD-08** | GitHub Actions 錯峰排程與防護 | [`CARD-08_WORKFLOW_GitHub_Actions.md`](./CARD-08_WORKFLOW_GitHub_Actions.md) | `.github/workflows/daily_quant.yml` | `ready-for-agent` |
