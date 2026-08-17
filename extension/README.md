# Agent Workflow Model Catalog 0.3.0

`#workflowModels` / `agent-workflow_getModelCatalog` を提供する、Agent Workflow専用の小さなVS Code拡張です。

## 役割

この拡張は **モデルを選びません**。`vscode.lm.selectChatModels()` が現在公開するモデル一覧を、Workflow Orchestratorが参照できるread-only toolとして公開するだけです。

返すのは公開APIで取得できるidentity/context-capacity情報です。cost tier、reasoning/thinking強度、品質順位、latency、modality/tool適合性を欠落フィールドから推測しません。

## Source / build

正本は `src/` です。

```bash
npm install
npm run compile
npm test
npm run package:vsix
```

公式 `@vscode/vsce` を使えないオフライン環境では、同梱prebuiltと同じdeterministic packageを次でも再生成できます。

```bash
npm run package:vsix:offline
```

同梱済みVSIXは `dist/agent-workflow-model-catalog-0.3.0.vsix` です。

## Install

VS CodeのCommand Paletteから `Extensions: Install from VSIX...` を選び、`dist/agent-workflow-model-catalog-0.3.0.vsix` を指定します。

または:

```bash
code --install-extension dist/agent-workflow-model-catalog-0.3.0.vsix
```

## Command

`Agent Workflow: Show Live Model Catalog` で、現在のcatalogをOutput Channelに表示できます。
