# VS Code Copilot Agent Workflow — verified package

[![CI](https://github.com/poruru210/agent-workflow-vscode-copilot/actions/workflows/ci.yml/badge.svg)](https://github.com/poruru210/agent-workflow-vscode-copilot/actions/workflows/ci.yml)

VS Code GitHub Copilot専用のAgent Workflowです。`Global Workflow Core`という別抽象層はありません。

## 構成

```text
vscode-copilot-agent-workflow-verified/
├─ workflow/                      # 唯一のworkflow正本
│  ├─ agents/
│  ├─ skills/
│  ├─ hooks/
│  ├─ instructions/
│  └─ agent-workflow/
│     ├─ scripts/
│     ├─ policy/
│     └─ state-template/
├─ extension/
│  ├─ src/                        # Extensionソースの正本
│  ├─ test/
│  ├─ out/                        # TypeScript compile結果
│  └─ dist/agent-workflow-model-catalog-0.3.0.vsix            # インストール用VSIX
├─ validation/
├─ VALIDATION.md
└─ MANIFEST.sha256
```

`global/` と `repository/` の複製はありません。

## Repository配置

`workflow/` の**中身**を、対象repositoryの `.github/` へコピーします。

```text
<repo>/.github/
├─ agents/
├─ skills/
├─ hooks/
├─ instructions/
└─ agent-workflow/
```

## Global配置

同じ `workflow/` の**中身**を、ユーザープロファイルの `.copilot/` へコピーします。

Windows:

```text
%USERPROFILE%\.copilot```

Linux/macOS:

```text
~/.copilot/
```

## Model Catalog Extension

ワークフローの動的model routingを補助するExtensionです。Extension自身はmodelを選定・順位付けしません。

インストールするファイル:

```text
extension/dist/agent-workflow-model-catalog-0.3.0.vsix
```

VS Codeで `Extensions: Install from VSIX...` を実行するか、CLIで:

```bash
code --install-extension extension/dist/agent-workflow-model-catalog-0.3.0.vsix
```

インストール後、VS CodeをReloadし、`Agent Workflow: Show Live Model Catalog` またはAgent側の `#workflowModels` を利用できます。

## 動的モデル選定

Custom Agentには `model:` を固定していません。Workflow Orchestratorがsubagent invocationごとにlive catalog、job requirement、risk、独立性、cost/latency evidence、検証容易性から最低十分なmodelを選びます。

## 検証結果

詳細は `VALIDATION.md` を参照してください。実行可能な決定的検証はPASSしています。実VS Code/Copilot hostを必要とする項目は、実行環境にVS Code本体がないため `UNVERIFIED` のまま明示しています。

## CI

GitHub Actions (`.github/workflows/ci.yml`) では Ubuntu / Windows の両方で検証します。

- workflow構造・frontmatter・relative link・固定model不在
- Python Hookのphase enforcement / path resolution / checkpoint
- Windows runnerでPowerShell Hookのparseと主要behavior
- TypeScript 5.8.3 build
- Model Catalogのunit/mock activation test
- 同梱VSIXの構造・identity・決定的再生成
- 公式 `@vscode/vsce 3.9.2` による再package
- `MANIFEST.sha256` の整合性

実Copilotアカウントを必要とするlive model catalog列挙はCIの必須PASSにはしていません。
