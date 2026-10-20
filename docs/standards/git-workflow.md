# 🏛️ Git 分支開發、CI 門禁與大掃除標準作業規範 (git-workflow.md)

本文件遵循 [80% 簡化技術中文規範 (STE-TW)](./simplified-technical-chinese.md)。

---

## 1. 核心原則 (Core Principles)

- **杜絕主線直接提交**：`master` 分支僅接受經由 Pull Request (PR) 審核通過之代碼。
- **本地雙重門禁前置**：代碼在本地必須通過語法與單元測試，未通過者禁止推送至遠端。
- **架構感知結構化 PR**：所有 PR 必須闡明「為什麼改 (Why)」、「改了什麼 (What)」、「影響是什麼 (Impact)」，杜絕隨意混亂之提交。
- **嚴格遵守 GitHub 服務條款 (ToS)**：限制 Actions 執行上限為 5 分鐘，啟用併發自動取消，禁止在 CI 執行未授權爬蟲或暴露敏感金鑰。
- **合併後即刻滅跡大掃除**：PR 合併後立即清理本機與遠端分支，維持雙端 100% 潔淨一致。

---

## 2. 本地防呆雙門禁機制 (.githooks)

專案預設啟用原生 Git Hooks，無需安裝任何外部肥大套件：

1. **`pre-commit` (主線提交與敏感檔案阻斷)**：
   - 偵測當前分支，若為 `master` 或 `main`，強制阻斷 commit。
   - 掃描暫存區，若包含 `.env`、`*secret*`、`*.pem` 等憑證，立即拒絕提交。
2. **`pre-push` (推送前測試強制驗證)**：
   - 執行 `git push` 前，自動觸發 `python -m pytest tests/`。
   - 單元測試 100% 通過才放行推播。

> **本機啟用指令**：
> ```bash
> git config core.hooksPath .githooks
> ```

---

## 3. 日常標準開發循環 (Development Lifecycle)

### 步驟 1：開闢特性或修復分支
```bash
git checkout master
git pull --prune origin master
git checkout -b feature/<功能名稱>   # 新功能
# 或 git checkout -b fix/<修復名稱>  # 錯誤修復
```

### 步驟 2：本地編碼與測試
- 編寫功能代碼與對應的單元測試。
- 執行本地測試確認無誤：
  ```bash
  python -m pytest tests/
  ```

### 步驟 3：合規提交代碼
- 嚴禁盲目 `git add .`，僅精確暫存目標檔案。
- 嚴格使用繁體中文提交訊息：
  ```bash
  git add src/ tests/
  # 使用文字檔提交避免終端機編碼亂碼
  echo "feat(quant): 新增外資籌碼偏離度指標" > .git_commit_msg.txt
  git commit -F .git_commit_msg.txt
  rm .git_commit_msg.txt
  ```

### 步驟 4：推送分支並發起 PR
```bash
git push -u origin feature/<功能名稱>
```
- 本地 `pre-push` 自動執行全量測試。
- 通過後至 GitHub 發起 PR，範本將自動載入「Why / What / Impact」三段式架構。
- 等待 GitHub Actions (`ci.yml`) 自動檢查通過（綠燈）。

---

## 4. PR 合併後「大掃除與雙端一致性」SOP

當 PR 在 GitHub 上完成 Review 並點擊「Merge」合併回 `master` 後，立即執行以下 4 步清理本機環境：

```bash
# 1. 切換回 master 主線
git checkout master

# 2. 拉取最新代碼並修剪遠端已刪除的分支指標
git pull --prune origin master

# 3. 安全刪除已合併的本地特性分支
git branch -d feature/<功能名稱>

# 4. 驗證本機工作區清潔度
git status
```

---

## 5. GitHub 儲存庫網頁端推薦設定 (Repository Settings)

請專案管理員前往 GitHub 儲存庫進行以下兩項原生安全設定（免費用戶完全支援）：

1. **分支自動刪除 (Automatically delete head branches)**：
   - 路徑：`Settings` ➔ `General` ➔ `Pull Requests`。
   - 勾選 **`Automatically delete head branches`**。
   - 效益：PR 合併後，GitHub 自動清理遠端分支，杜絕殭屍分支堆積。
2. **主線保護規則 (Branch Protection Rule)**：
   - 路徑：`Settings` ➔ `Branches` ➔ `Add branch protection rule`。
   - 分支模式 (Branch name pattern)：輸入 `master`。
   - 勾選 **`Require a pull request before merging`**（禁止直接 push 到 master）。
   - 勾選 **`Require status checks to pass before merging`**，並指定 `code-quality-gate`（CI 綠燈前不可合併）。
