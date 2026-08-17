# agent-workflow-vscode-copilot

VS Code GitHub Copilot 専用の Agent Workflow です。

Custom Agents、Agent Skills、Hooks、継続状態、独立監査、区分ごとの検証、動的モデル選択用Extensionを組み合わせ、**主目的 → 実装・変更 → 検証 → 独立監査 → Go/No-Go** を一貫して管理します。

- Custom Agent は **役割 / 利用できるツール / 権限境界** を定義します。
- モデルは役割へ固定せず、Subagentを呼び出す直前に現在利用できるモデル一覧と作業要件から選びます。
- 監査フェーズでは、監査対象を読み取り専用に保ちます。
- 長時間、Subagent委譲、複数目的、修正の繰り返しを含む作業では、workspace-local の `.agent-workflow/` に継続状態を保持します。
- Hooks は境界違反を防ぐ補助機構です。Hookが動いたこと自体は、成果物の正しさを示す証拠にはなりません。

## Visual guide

ワークフローの動きをアニメーション付きのシングルHTMLで確認できます。

- [`docs/agent-workflow-vscode-copilot-visual-guide-controls-state.html`](docs/agent-workflow-vscode-copilot-visual-guide-controls-state.html)

GitHubのblob表示ではJavaScriptアニメーションは実行されないため、アニメーションを確認する場合はHTMLをダウンロードしてブラウザで開いてください。

Visual Guideでは、同じ「左 = 基本フロー / 右 = 詳細」のレイアウトで次を説明します。

1. **基本フロー** — 通常時の各段階と次へ進む条件
2. **Subagent委譲** — 現在位置から作業を切り出し、完了結果を同じ位置へ戻す流れ
3. **失敗時の診断・修正** — FAIL地点から診断へ分岐し、変更内容に応じた地点から再開する流れ

`docs/index.html` は以前のリンクとの互換用リダイレクトだけを残しています。Visual Guideの正本は上記の名前付きHTMLです。

## Repository layout

```text
.
├─ workflow/                         # 配布する Agent Workflow の正本
│  ├─ agents/                        # Custom Agents
│  ├─ skills/                        # Agent Skills
│  ├─ hooks/                         # VS Code agent hooks
│  ├─ instructions/                  # file-based instructions
│  └─ agent-workflow/
│     ├─ policy/                     # 詳細 workflow policy
│     ├─ scripts/                    # hook implementation
│     └─ state-template/             # runtime state schema/template
│
├─ extension/
│  ├─ src/                           # Model Catalog Extension source
│  ├─ test/
│  └─ package.json
│
├─ tests/                            # workflow / hook / docs tests
├─ docs/
│  ├─ agent-workflow-vscode-copilot-visual-guide-controls-state.html
│  └─ index.html                     # compatibility redirect only
└─ .github/workflows/ci.yml          # build / test / package / artifact upload
```

`extension/out/`、`extension/dist/`、生成済みVSIXはGit管理しません。CIがソースから生成します。

---

# Installation

## 0. 前提

- VS Code + GitHub Copilot を利用できること
- Model Catalog Extension は `engines.vscode: ^1.131.0` を要求します
- Repository配置またはGlobal配置の **どちらか一方を基本**にしてください

同じworkflowをRepositoryとGlobalの両方へ配置することもできますが、同名Custom Agentの重複など運用上わかりにくくなるため、意図的なworkspace overrideが必要な場合を除き片方だけの利用を推奨します。

## 1. CI artifact を取得する — 推奨

GitHubの **Actions → 最新の成功した `CI` run → Artifacts** から `agent-workflow-vscode-copilot` artifact をダウンロードします。

artifactには次の2成果物が入ります。

```text
agent-workflow-model-catalog-<version>.vsix
agent-workflow-vscode-copilot-workflow.zip
```

`agent-workflow-vscode-copilot-workflow.zip` の内容はRepository / Globalで共通です。違うのは展開先だけです。

---

# A. Repository 配置

特定repositoryだけでAgent Workflowを使う場合です。

workflow ZIPの **中身** を対象repositoryの `.github/` へ展開します。

```text
<repo>/
└─ .github/
   ├─ agents/
   ├─ skills/
   ├─ hooks/
   ├─ instructions/
   └─ agent-workflow/
      ├─ policy/
      ├─ scripts/
      └─ state-template/
```

`workflow/` ディレクトリ自体を `.github/` の中へ作るのではなく、**workflow ZIPの中身を `.github/` 直下へ置く**点に注意してください。

source checkoutから直接配置する場合:

Linux / macOS:

```bash
mkdir -p .github
cp -R workflow/. .github/
```

PowerShell:

```powershell
New-Item -ItemType Directory -Force .github | Out-Null
Copy-Item -Recurse -Force .\workflow\* .\.github\
```

VS Codeの既定workspace discovery位置を使うため、追加の `settings.json` は不要です。

---

# B. Global 配置

すべてのworkspaceでAgent Workflowを使う場合です。

workflow ZIPの **中身** をユーザープロファイルの `~/.copilot/` へ展開します。

```text
~/.copilot/
├─ agents/
├─ skills/
├─ hooks/
├─ instructions/
└─ agent-workflow/
   ├─ policy/
   ├─ scripts/
   └─ state-template/
```

Windowsでは通常 `~` はユーザープロファイルに対応します。

```text
C:\Users\<USER>\.copilot\
```

source checkoutから直接配置する場合:

Linux / macOS:

```bash
mkdir -p ~/.copilot
cp -R workflow/. ~/.copilot/
```

PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME\.copilot" | Out-Null
Copy-Item -Recurse -Force .\workflow\* "$HOME\.copilot\"
```

---

# C. Model Catalog Extension をインストール

動的モデル選択を正確に行うため、artifact内のVSIXをVS Codeへインストールします。

1. VS Codeを開く
2. `Ctrl+Shift+P`
3. **Extensions: Install from VSIX...**
4. `agent-workflow-model-catalog-<version>.vsix` を選択
5. 必要ならVS Code windowをreload

CLIでもインストールできます。

```bash
code --install-extension ./agent-workflow-model-catalog-<version>.vsix
```

手動インストールしたVSIXは、このrepositoryの新しいartifactを取得した際に必要に応じて更新してください。

---

# 2. Installation verification

## Custom Agent

通常の入口は **Agent Workflow Orchestrator** です。VS Code Chatのagent selectorでOrchestratorを選択できることを確認します。

下位の役割別Custom AgentはOrchestratorから内部的に呼び出す構成であり、`user-invocable: false` のagentはselectorに直接表示されないのが正常です。

内部で利用する主な役割:

```text
Workflow Researcher
Workflow Implementer
Root Cause Reviewer
Early Auditor
Workflow Tester
Final Auditor
Pre Action Auditor
```

## Model Catalog Extension

Command Paletteから次を実行できます。

```text
Agent Workflow: Show Live Model Catalog
```

VS Codeが現在公開しているmodelのidentity / family / version / maxInputTokensなどがOutputに表示されればExtensionは動作しています。

OrchestratorはSubagentを呼び出す直前に `#workflowModels` を利用し、作業要件に応じてmodelを選択します。

## Hooks

Repository配置:

```text
<repo>/.github/agent-workflow/scripts/workflow_hook.py
<repo>/.github/agent-workflow/scripts/workflow_hook.ps1
```

Global配置:

```text
~/.copilot/agent-workflow/scripts/workflow_hook.py
~/.copilot/agent-workflow/scripts/workflow_hook.ps1
```

Hook launcherはworkspaceから親方向へRepository配置を探索し、見つからない場合はGlobal配置へfallbackします。

---

# 3. `.agent-workflow/` はインストール先ではない

`.agent-workflow/` はworkflow定義の配置場所ではありません。通常フローへ入り、継続状態が必要になったworkspaceで実行時状態を保持するために使います。

```text
<working-repository>/
└─ .agent-workflow/
   ├─ state.json
   ├─ evidence-map.json
   ├─ model-performance.json
   ├─ jobs/
   ├─ checkpoints/
   └─ audit/
```

主な用途:

- active objective / 現在のフェーズ
- 未解決の必須命題
- version付きSubagent Job Lease
- 候補状態 / 証拠identity
- Evidence Dependency Map
- context compaction前のcheckpoint
- 修正・監査を再開するための継続状態

Compactの読み取り専用回答のためだけに `.agent-workflow/` を生成する設計ではありません。

---

# 4. How the workflow runs

通常時の基本フロー:

```text
User Request
   │
   ▼
Compact 判定
   │ 通常フロー
   ▼
Work Definition
   ▼
Risk / Plan
   ▼
Baseline
   ▼
作業種別分岐
   ▼
実装 / 修正 / 変更
   ▼
Implementation Snapshot
   ▼
Early Independent Audit       [READ ONLY]
   ▼
Partitioned Verification      [U0 -> U1]
   ▼
Tested-target Identity Gate
   ▼
Release Candidate
   ▼
Final Independent Audit       [READ ONLY]
   ▼
Completion / Go-No-Go
```

### Subagent委譲

現在のフェーズから範囲を限定した作業だけを切り出し、結果を親Orchestratorが受け取って **元のフェーズの判定へ戻します**。

```text
現在のフェーズ
   -> Job Lease
   -> #workflowModels
   -> モデル選択
   -> runSubagent(...)
   -> 完了結果
   -> 元のフェーズで統合・判定
```

### FAILになった場合

その場で症状だけを修正せず、証拠保存と根本原因確認を行います。

```text
FAIL
  -> 証拠を保存
  -> RC / VER / TEST-RC
  -> 必要なら根本原因の独立確認
  -> INT / 修正
  -> 変更影響を再導出
  -> 変更内容に応じた地点から再開
```

### 未証明になった場合

必要な証拠が不足しているだけなら、直ちにRC / INT / 修正へ進みません。追加証拠取得、正確な阻害の記録、同一identity上の限定再判定を優先します。

再開地点の例:

- **候補成果物を変更した**: `Implementation Snapshot` → Early Independent Audit → Partitioned Verification
- **テスト計画だけを変更した**: テスト準備の差分確認 → 必要なPartitioned Verification
- **追加証拠だけで再判定できる**: 該当する命題だけを限定再判定
- **外部操作の計画・対象・権限が変わった**: 実行準備ゲート → 必要範囲の実行前独立監査 → 実行直前の最新性確認

詳細は名前付きの [Visual Guide](docs/agent-workflow-vscode-copilot-visual-guide-controls-state.html) を参照してください。

---

# 5. Dynamic model routing

Custom Agentにはモデルを固定しません。

```text
Job Lease
  -> #workflowModels
  -> 必須能力で絞り込み
  -> 必要十分な候補に絞る
  -> 独立性 / コストを比較
  -> agent/runSubagent(model=...)
```

`#workflowModels` が提供するのは現在の利用可否、identity、family、version、context capacityなどの情報であり、性能順位表ではありません。

APIが公開しないcost tier、reasoning/thinking level、vision/tool suitability、quality rankingを推測で補いません。必要なら別の根拠で確認します。

VS CodeのSubagent modelは親modelのcost tierを超えられないため、委譲先の選択肢を広く取りたい場合はOrchestratorの親model側も考慮します。

---

# 6. Update / uninstall

Workflow更新時は、新しいCI artifactのworkflow ZIPを現在の配置先へ上書きします。

Repository:

```text
<repo>/.github/
```

Global:

```text
~/.copilot/
```

`.agent-workflow/` は実行時の継続状態なので、workflow定義の更新時に無条件で削除しないでください。

Extensionは新しいVSIXを再度 **Extensions: Install from VSIX...** でインストールします。

削除時はRepositoryまたはGlobal配置先のAgent Workflow由来ファイルだけを削除し、既存の別customizationを巻き込まないようにしてください。

---

# 7. Troubleshooting

### `Agent Workflow hook script not found`

Repository:

```text
<repo>/.github/agent-workflow/scripts/
```

Global:

```text
~/.copilot/agent-workflow/scripts/
```

### `#workflowModels` が利用できない

- Model Catalog VSIXがインストールされているか確認
- `Agent Workflow: Show Live Model Catalog` を実行
- Extensionが現在のVS Code versionと互換か確認

### Agent が二重に見える

RepositoryとGlobalの両方に同じworkflowを配置していないか確認してください。

### 監査中に編集や変更系コマンドが拒否される

仕様です。root-cause challenge、pre-action audit、early audit、final auditでは監査対象を読み取り専用に維持します。

---

# Development

```bash
python -m pip install -r tests/requirements.txt
python tests/test_workflow.py
python tests/test_docs.py

cd extension
npm install
npm test
npm run package:vsix
```

CIはソースから次を検証・生成します。

```text
workflow source validation
-> docs visual-guide validation
-> TypeScript build / extension tests
-> VSIX package
-> workflow ZIP package
-> Windows PowerShell hook smoke test
-> Actions artifact upload
```
