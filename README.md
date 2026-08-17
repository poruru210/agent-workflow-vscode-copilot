# agent-workflow-vscode-copilot

VS Code GitHub Copilot 専用の Agent Workflow です。

Custom Agents、Agent Skills、Hooks、durable state、独立監査、分割検証、および動的 model routing 用 Extension を組み合わせ、**主目的 → 実装/変更 → 検証 → 独立監査 → Go/No-Go** を一貫して管理します。

- Custom Agent は **role / tools / authority** を固定します。
- model は role に固定せず、subagent invocation ごとに live catalog と job requirements から選択します。
- audit phase は対象を read-only に保ちます。
- long-running / delegated / correction-heavy task は workspace-local `.agent-workflow/` に durable state を持ちます。
- Hooks は enforcement の補助であり、Hook が動いたこと自体は correctness evidence ではありません。

## Visual guide

ワークフロー全体をアニメーション付きで確認できます。

- [Copilot Agent Workflow — Animated Visual Guide](docs/index.html)

Visual guide は **主幹の正常成功経路**、**phase 内で行う Orchestrator → subagent の委譲と結果統合**、**FAIL 時だけ主幹から一時離脱する diagnosis / correction と復帰**を別々の図として説明します。

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
├─ tests/                            # workflow / hook tests
├─ docs/
│  └─ index.html                     # single-HTML visual guide
└─ .github/workflows/ci.yml          # build / test / package / artifact upload
```

`extension/out/`, `extension/dist/`, prebuilt VSIX は Git 管理しません。CI がソースから生成します。

---

# Installation

## 0. 前提

- VS Code + GitHub Copilot を利用できること
- Model Catalog Extension は `engines.vscode: ^1.131.0` を要求します
- Repository 配置または Global 配置の **どちらか一方を基本**にしてください

同じ workflow を Repository / Global の両方へ配置することもできますが、同名 Custom Agent が重複して見えるなど運用上わかりにくくなるため、意図的な workspace override が必要な場合を除き片方を推奨します。

## 1. CI artifact を取得する — 推奨

GitHub の **Actions → 最新の成功した `CI` run → Artifacts** から
`agent-workflow-vscode-copilot` artifact をダウンロードします。

artifact には次の2成果物が入ります。

```text
agent-workflow-model-catalog-<version>.vsix
agent-workflow-vscode-copilot-workflow.zip
```

`agent-workflow-vscode-copilot-workflow.zip` の内容は Repository / Global で同一です。
違うのは展開先だけです。

---

# A. Repository 配置

その repository だけで Agent Workflow を使う場合です。

`agent-workflow-vscode-copilot-workflow.zip` の **中身**を対象 repository の `.github/` へ展開します。

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

重要なのは、`workflow/` というディレクトリを `.github/` の中へ作るのではなく、**workflow ZIP の中身を `.github/` 直下へ置く**ことです。

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

VS Code の既定 workspace discovery 位置と一致するため、追加の `settings.json` は不要です。

---

# B. Global 配置

すべての workspace で Agent Workflow を使う場合です。

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

Windows では通常、`~` はユーザープロファイルに対応します。例:

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

動的 model routing を正確に行うため、artifact 内の VSIX を VS Code へインストールします。

推奨手順:

1. VS Code を開く
2. `Ctrl+Shift+P`
3. **Extensions: Install from VSIX...**
4. `agent-workflow-model-catalog-<version>.vsix` を選択
5. 必要なら VS Code window を reload

CLI でもインストールできます。

```bash
code --install-extension ./agent-workflow-model-catalog-<version>.vsix
```

VSIX を手動インストールした Extension は Marketplace 配布版のような自動更新を前提にしないため、この repository の新しい artifact を取得したときに必要に応じて更新してください。

---

# 2. Installation verification

## Custom Agent

VS Code Chat の agent selector で次が見えることを確認します。

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

Command Palette から次を実行できます。

```text
Agent Workflow: Show Live Model Catalog
```

VS Code が現在公開している model の identity / family / version / maxInputTokens 等が Output に表示されれば Extension は動作しています。

Orchestrator は delegated job の直前に `#workflowModels` を利用し、role 固定ではなく job requirement に応じて model を選択します。

## Hooks

Repository 配置なら Hook script は次に存在します。

```text
<repo>/.github/agent-workflow/scripts/workflow_hook.py
<repo>/.github/agent-workflow/scripts/workflow_hook.ps1
```

Global 配置なら:

```text
~/.copilot/agent-workflow/scripts/workflow_hook.py
~/.copilot/agent-workflow/scripts/workflow_hook.ps1
```

Hook launcher は workspace から親方向へ Repository 配置を探索し、見つからない場合は Global 配置へ fallback します。

---

# 3. `.agent-workflow/` は「インストール先」ではない

`.agent-workflow/` は workflow 定義の配置場所ではありません。

Normal branch に入り、durable state が必要になった workspace で、実行時状態を保持するために使います。

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

- active objective / phase
- mandatory open claims
- versioned subagent invocation lease
- candidate / evidence identity
- Evidence Dependency Map
- context compaction 前の checkpoint
- correction / audit の継続状態

Compact read-only answer のためだけに `.agent-workflow/` を生成する設計ではありません。

---

# 4. How the workflow runs

通常経路の概略です。

```text
User Request
   │
   ▼
Compact 判定
   │ Normal
   ▼
Work Definition
   ▼
Risk / Plan
   ▼
Baseline
   ▼
Work-type branch
   ▼
Implementation / Change
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

FAIL / 未証明は正常経路上でそのまま patch せず、右側の correction loop へ分岐します。

```text
FAIL
  -> Evidence 保存
  -> RC / VER / TEST-RC
  -> INT / Correction
  -> New Snapshot
  -> 影響差分だけ Early Audit / Verification へ戻る
```

詳細は [Animated Visual Guide](docs/index.html) を参照してください。

---

# 5. Dynamic model routing

Custom Agent には model を固定しません。

delegated invocation ごとに次の順で選択します。

```text
Job Lease
  -> #workflowModels
  -> hard capability filter
  -> minimum sufficient candidates
  -> independence / correlated-blind-spot check
  -> risk-adjusted cost / latency / comparable recent evidence
  -> agent/runSubagent(model=...)
```

`#workflowModels` が提供するのは live availability / identity / context-capacity の evidence です。
API が公開しない cost tier、reasoning/thinking level、vision/tool suitability、quality ranking を架空に補完しません。

また、VS Code の subagent model は親 model の cost tier を超えられないため、delegation ceiling を広く取りたい場合は Orchestrator の親 model 側も考慮する必要があります。

---

# 6. Update / uninstall

## Workflow を更新

新しい CI artifact の workflow ZIP を、現在使用している配置先へ上書きします。

Repository:

```text
<repo>/.github/
```

Global:

```text
~/.copilot/
```

`.agent-workflow/` は runtime state なので、workflow 定義の更新時に無条件削除しないでください。

## Extension を更新

新しい VSIX を再度 **Extensions: Install from VSIX...** でインストールします。

## Workflow を削除

Repository install なら、今回配置した `.github/agents`, `.github/skills`, `.github/hooks`, `.github/instructions`, `.github/agent-workflow` の Agent Workflow 由来ファイルだけを削除します。既存の別 customization を巻き込まないようにしてください。

Global install も同様に `~/.copilot/` 内の Agent Workflow 由来ファイルだけを削除します。

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

- Model Catalog VSIX がインストールされているか確認
- `Agent Workflow: Show Live Model Catalog` を実行
- Extension が現在の VS Code version と互換か確認

### Agent が二重に見える

Repository と Global の両方に同じ workflow を配置していないか確認してください。通常は片方だけで十分です。

### audit 中に edit / mutating command が拒否される

仕様です。root-cause challenge、pre-action audit、early audit、final audit は audited target を read-only に維持します。

---

# Development

```bash
python -m pip install -r tests/requirements.txt
python tests/test_workflow.py

cd extension
npm install
npm test
npm run package:vsix
```

CI は source から次を検証・生成します。

```text
workflow source validation
-> TypeScript build / extension tests
-> VSIX package
-> workflow ZIP package
-> Windows PowerShell hook smoke test
-> Actions artifact upload
```
