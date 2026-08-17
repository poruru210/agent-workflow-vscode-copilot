# agent-workflow-vscode-copilot

VS Code GitHub Copilot専用のAgent Workflowです。Custom Agents、Agent Skills、Hooks、動的model routing用Extensionをソースとして管理します。

## Repository layout

```text
.
├─ workflow/
│  ├─ agents/
│  ├─ skills/
│  ├─ hooks/
│  ├─ instructions/
│  └─ agent-workflow/
├─ extension/
│  ├─ src/
│  ├─ test/
│  └─ package.json
├─ tests/
└─ .github/workflows/ci.yml
```

生成物 (`extension/out`, `extension/dist`, VSIX) はGit管理しません。GitHub Actionsがソースからbuild/test/packageし、Actions artifactとして次を出力します。

- `agent-workflow-model-catalog-0.3.0.vsix`
- `agent-workflow-vscode-copilot-workflow.zip`

## 配置

CI artifactの `agent-workflow-vscode-copilot-workflow.zip` は同一内容を用途に応じて配置します。

- Repository: zipの中身を `<repo>/.github/` へ
- Global: zipの中身を `~/.copilot/` へ

Model Catalog ExtensionはActions artifactのVSIXを VS Code の `Extensions: Install from VSIX...` からインストールします。

## Dynamic model routing

Custom Agentにはmodelを固定しません。Orchestratorはlive model catalog、job requirements、risk、independence、cost/latency evidence、検証容易性からsubagent invocationごとに最低十分なmodelを選択します。

## Development

```bash
python -m pip install -r tests/requirements.txt
python tests/test_workflow.py
cd extension
npm install
npm test
npm run package:vsix
```
