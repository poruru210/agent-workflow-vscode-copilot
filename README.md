# agent-workflow-vscode-copilot

VS Code GitHub Copilot 専用の Agent Workflow です。

Custom Agents、Agent Skills、Hooks、継続状態、独立監査、区分ごとの検証、動的モデル選択用Extensionを組み合わせ、**主目的 → 実装・変更 → 検証 → 独立監査 → Go/No-Go** を一貫して管理します。

- Custom Agent は **役割 / 利用できるツール / 権限境界** を定義します。
- モデルは役割へ固定せず、Subagentを呼び出す直前に現在利用できるモデル一覧と作業要件から選びます。
- 監査フェーズでは、監査対象を読み取り専用に保ちます。
- 長時間、Subagent委譲、複数目的、修正の繰り返しを含む作業では、workspace-local の `.agent-workflow/` に継続状態を保持します。
- Hooks は境界違反を防ぐ補助機構です。Hookが動いたこと自体は、成果物の正しさを示す証拠にはなりません。

## Visual guide

ワークフローの動きをアニメーション付きで確認できます。

- [Copilot Agent Workflow — Visual Guide](docs/index.html)

Visual Guideでは、次を別々の図として説明します。

1. **基本フロー** — 作業が問題なく進んだ場合の通常経路
2. **Subagent委譲** — 現在のフェーズから作業を切り出し、完了結果を同じフェーズへ戻す流れ
3. **失敗時の診断・修正** — FAILまたは未証明になった場合に診断・修正へ分岐し、変更内容に応じた地点から再開する流れ

詳細なフェーズの前に全体像も掲載しています。

## Repository layout

```text
.
├─ workflow/                         # 配布する Agent Workflow の唯一の正本
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
│  ├─ src/                           # Model Catalog Extension のソース正本
│  ├─ test/
│  └─ package.json
│
├─ tests/                            # workflow / hook / docs tests
├─ docs/
│  └─ index.html                     # single-HTML visual guide
└─ .github/workflows/ci.yml          # build / test / package / artifact upload
```

`extension/out/`、`extension/dist/`、生成済みVSIXはGit管理しません。CIがソースから生成します。

---

# Installation

## 0. 前提

- VS Code + GitHub Copilot を利用できること
- Model Catalog Extension は `engines.vscode: ^1.131.0` を要求します
- Repository配置またはGlobal配置の **どちらか一方を基本**にしてください

同じworkflowをRepositoryとGlobalの両方へ配置することもできますが、同名のCustom Agentが重複して見えるなど運用上わかりにくくなるため、意図的なworkspace overrideが必要な場合を除き、片方だけの利用を推奨します。

## 1. CI artifact を取得する — 推奨

GitHubの **Actions → 最新の成功した `CI` run → Artifacts** から、`agent-workflow-vscode-copilot` artifactをダウンロードします。

artifactには次の2成果物が入ります。

```text
agent-workflow-model-catalog-<version>.vsix
agent-workflow-vscode-copilot-workflow.zip
```

`agent-workflow-vscode-copilot-workflow.zip` の内容はRepository / Globalで共通です。違うのは展開先だけです。

---

# A. Repository 配置

特定のrepositoryだけでAgent Workflowを使う場合です。

`agent-workflow-vscode-copilot-workflow.zip` の **中身**を対象repositoryの `.github/` へ展開します。

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

`workflow/` というディレクトリを `.github/` の中へ作るのではなく、**workflow ZIPの中身を `.github/` 直下へ置く**点に注意してください。

### source checkout から直接配置する場合

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

VS Codeの既定workspace discovery位置と一致するため、追加の `settings.json` は不要です。

---

# B. Global 配置

すべてのworkspaceでAgent Workflowを使う場合です。

`agent-workflow-vscode-copilot-workflow.zip` の **中身**をユーザープロファイルの `~/.copilot/` へ展開します。

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

Windowsでは通常、`~` はユーザープロファイルに対応します。

```text
C:\Users\<USER>\.copilot\
```

### source checkout から直接配置する場合

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

推奨手順:

1. VS Codeを開く
2. `Ctrl+Shift+P`
3. **Extensions: Install from VSIX...**
4. `agent-workflow-model-catalog-<version>.vsix` を選択
5. 必要ならVS Code windowをreload

CLIでもインストールできます。

```bash
code --install-extension ./agent-workflow-model-catalog-<version>.vsix
```

VSIXを手動インストールしたExtensionはMarketplace配布版のような自動更新を前提にしないため、このrepositoryの新しいartifactを取得した際に必要に応じて更新してください。

---

# 2. Installation verification

## Custom Agent

VS Code Chatのagent selectorで次が見えることを確認します。

```text
Agent Workflow Orchestrator
Workflow Researcher
Workflow Implementer
Root Cause Reviewer
Early Auditor
Workflow Tester
Final Auditor
Pre Action Auditor
```

通常は **Agent Workflow Orchestrator** を入口にします。

## Model Catalog Extension

Command Paletteから次を実行できます。

```text
Agent Workflow: Show Live Model Catalog
```

VS Codeが現在公開しているモデルのidentity / family / version / maxInputTokensなどがOutputに表示されれば、Extensionは動作しています。

OrchestratorはSubagentを呼び出す直前に `#workflowModels` を利用し、役割固定ではなく作業要件に応じてモデルを選択します。

## Hooks

Repository配置ならHook scriptは次に存在します。

```text
<repo>/.github/agent-workflow/scripts/workflow_hook.py
<repo>/.github/agent-workflow/scripts/workflow_hook.ps1
```

Global配置なら:

```text
~/.copilot/agent-workflow/scripts/workflow_hook.py
~/.copilot/agent-workflow/scripts/workflow_hook.ps1
```

Hook launcherはworkspaceから親方向へRepository配置を探索し、見つからない場合はGlobal配置へfallbackします。

---

# 3. `.agent-workflow/` はインストール先ではない

`.agent-workflow/` はworkflow定義の配置場所ではありません。

通常フローへ入り、継続状態が必要になったworkspaceで、実行時の状態を保持するために使います。

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
- 候補状態 / 証拠のidentity
- Evidence Dependency Map
- context compaction前のcheckpoint
- 修正・監査を再開するための継続状態

Compactの読み取り専用回答のためだけに `.agent-workflow/` を生成する設計ではありません。

---

# 4. How the workflow runs

通常時の基本フローです。

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

Subagent委譲は基本フローとは別に進む工程ではありません。現在のフェーズから範囲を限定した作業だけを切り出し、完了結果を親Orchestratorが受け取って、**元のフェーズの判定へ戻します**。

```text
現在のフェーズ
   -> Job Lease
   -> #workflowModels
   -> モデル選択
   -> runSubagent(...)
   -> 完了結果
   -> 元のフェーズで統合・判定
```

### FAIL / 未証明になった場合

その場で症状だけを修正せず、診断・修正へ分岐します。

```text
FAIL / 未証明
  -> 証拠を保存
  -> RC / VER / TEST-RC
  -> 必要なら根本原因の独立確認
  -> INT / 修正
  -> 変更影響を再導出
  -> 変更内容に応じた地点から再開
```

再開地点は固定ではありません。

- **候補成果物を変更した**: 新しい `Implementation Snapshot` を固定 → Early Independent Audit → Partitioned Verification
- **テスト計画だけを変更した**: テスト準備の差分確認 → 必要なPartitioned Verification
- **追加証拠だけで再判定できる**: 該当する命題だけを限定再判定
- **外部操作の計画・対象・権限が変わった**: 実行準備ゲート → 必要範囲の実行前独立監査 → 実行直前の最新性確認

詳細は [Visual Guide](docs/index.html) を参照してください。

---

# 5. Dynamic model routing

Custom Agentにはモデルを固定しません。

Subagentを呼び出すたびに、次の順でモデルを選択します。

```text
Job Lease
  -> #workflowModels
  -> 必須能力で絞り込み
  -> 必要十分な候補に絞る
  -> 独立性 / コストを比較
  -> agent/runSubagent(model=...)
```

`#workflowModels` が提供するのは、現在の利用可否、identity、family、version、context capacityなどの情報です。性能順位表ではありません。

APIが公開しないcost tier、reasoning/thinking level、vision/tool suitability、quality rankingを推測で補いません。必要な場合は別の根拠で確認します。

また、VS CodeのSubagentモデルは親モデルのcost tierを超えられないため、委譲先の選択肢を広く取りたい場合は、Orchestratorに設定する親モデル側も考慮する必要があります。

---

# 6. Update / uninstall

## Workflow を更新

新しいCI artifactのworkflow ZIPを、現在使用している配置先へ上書きします。

Repository:

```text
<repo>/.github/
```

Global:

```text
~/.copilot/
```

`.agent-workflow/` は実行時の継続状態なので、workflow定義の更新時に無条件で削除しないでください。

## Extension を更新

新しいVSIXを再度 **Extensions: Install from VSIX...** でインストールします。

## Workflow を削除

Repository配置なら、今回配置した `.github/agents`、`.github/skills`、`.github/hooks`、`.github/instructions`、`.github/agent-workflow` のうち、Agent Workflow由来のファイルだけを削除します。既存の別customizationを巻き込まないようにしてください。

Global配置も同様に、`~/.copilot/` 内のAgent Workflow由来ファイルだけを削除します。

---

# 7. Troubleshooting

### `Agent Workflow hook script not found`

配置rootを確認してください。

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

RepositoryとGlobalの両方に同じworkflowを配置していないか確認してください。通常は片方だけで十分です。

### 監査中に編集や変更系コマンドが拒否される

仕様です。root-cause challenge、pre-action audit、early audit、final auditでは、監査対象を読み取り専用に維持します。

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
