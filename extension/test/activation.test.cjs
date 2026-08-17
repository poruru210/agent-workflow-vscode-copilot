
const test = require('node:test');
const assert = require('node:assert/strict');
const Module = require('node:module');

function loadWithMock(models) {
  let registeredTool;
  let registeredCommand;
  let selectorSeen;
  const channelLines=[];
  class LanguageModelTextPart { constructor(value){ this.value=value; } }
  class LanguageModelToolResult { constructor(content){ this.content=content; } }
  const mock = {
    lm: {
      selectChatModels: async (selector) => { selectorSeen=selector; return models; },
      registerTool: (name, tool) => { registeredTool={name,tool}; return {dispose(){}}; },
    },
    commands: { registerCommand: (name, fn) => { registeredCommand={name,fn}; return {dispose(){}}; } },
    window: {
      createOutputChannel: () => ({clear(){channelLines.length=0;},appendLine(x){channelLines.push(x);},show(){},dispose(){}}),
      showErrorMessage: () => {},
    },
    LanguageModelTextPart,
    LanguageModelToolResult,
  };
  const original=Module._load;
  Module._load=function(request,parent,isMain){ if(request==='vscode') return mock; return original.call(this,request,parent,isMain); };
  const path=require.resolve('../out/extension.js');
  delete require.cache[path];
  let extension;
  try { extension=require(path); } finally { Module._load=original; }
  const context={subscriptions:[]};
  extension.activate(context);
  return {registeredTool, registeredCommand, getSelector:()=>selectorSeen, channelLines};
}

test('activation registers the expected read-only language model tool and command', async () => {
  const h=loadWithMock([{name:'M',id:'m',vendor:'copilot',family:'f',version:'1',maxInputTokens:4096}]);
  assert.equal(h.registeredTool.name,'agent-workflow_getModelCatalog');
  assert.equal(h.registeredCommand.name,'agent-workflow.showModelCatalog');
  const result=await h.registeredTool.tool.invoke({input:{vendor:'copilot',minInputTokens:1000}});
  assert.deepEqual(h.getSelector(),{vendor:'copilot'});
  const payload=JSON.parse(result.content[0].value);
  assert.equal(payload.ok,true);
  assert.equal(payload.count,1);
  assert.equal(payload.models[0].id,'m');
  assert.match(payload.limitation,/Do not infer cost tier/);
});

test('empty catalog is a valid result', async () => {
  const h=loadWithMock([]);
  const result=await h.registeredTool.tool.invoke({input:{}});
  const payload=JSON.parse(result.content[0].value);
  assert.equal(payload.ok,true);
  assert.equal(payload.count,0);
  assert.deepEqual(payload.models,[]);
});
