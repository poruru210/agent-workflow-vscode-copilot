
declare function require(id: string): any;

import { CatalogQuery, normalizeCatalog } from './catalog';

const vscode: any = require('vscode');
const TOOL_NAME = 'agent-workflow_getModelCatalog';
const COMMAND_NAME = 'agent-workflow.showModelCatalog';

function errorMessage(error: unknown): string {
  if (error && typeof error === 'object' && 'message' in error) {
    const message = (error as { message?: unknown }).message;
    if (typeof message === 'string') return message;
  }
  return String(error);
}

export async function readCatalog(input: CatalogQuery = {}): Promise<ReturnType<typeof normalizeCatalog>> {
  const selector: Record<string, string> = {};
  if (typeof input.vendor === 'string' && input.vendor.length > 0) selector.vendor = input.vendor;
  const models = await vscode.lm.selectChatModels(Object.keys(selector).length > 0 ? selector : undefined);
  return normalizeCatalog(models, input);
}

function successPayload(models: ReturnType<typeof normalizeCatalog>) {
  return {
    ok: true,
    generatedAt: new Date().toISOString(),
    source: 'vscode.lm.selectChatModels()',
    limitation: 'The public model catalog exposes identity/context-capacity metadata. Do not infer cost tier, reasoning/thinking level, modality/tool suitability, latency, or quality ranking from fields that are not returned.',
    count: models.length,
    models,
  };
}

function failurePayload(error: unknown) {
  return {
    ok: false,
    generatedAt: new Date().toISOString(),
    source: 'vscode.lm.selectChatModels()',
    error: errorMessage(error),
    models: [],
  };
}

class ModelCatalogTool {
  async invoke(options: any): Promise<any> {
    let payload: unknown;
    try {
      payload = successPayload(await readCatalog((options && options.input) || {}));
    } catch (error: unknown) {
      payload = failurePayload(error);
    }
    return new vscode.LanguageModelToolResult([
      new vscode.LanguageModelTextPart(JSON.stringify(payload, null, 2)),
    ]);
  }
}

export function activate(context: any): void {
  context.subscriptions.push(vscode.lm.registerTool(TOOL_NAME, new ModelCatalogTool()));
  const channel = vscode.window.createOutputChannel('Agent Workflow');
  context.subscriptions.push(channel);
  context.subscriptions.push(vscode.commands.registerCommand(COMMAND_NAME, async () => {
    let payload: unknown;
    try {
      payload = successPayload(await readCatalog({}));
    } catch (error: unknown) {
      payload = failurePayload(error);
      vscode.window.showErrorMessage(`Unable to read model catalog: ${errorMessage(error)}`);
    }
    channel.clear();
    channel.appendLine(JSON.stringify(payload, null, 2));
    channel.show(true);
  }));
}

export function deactivate(): void {}
