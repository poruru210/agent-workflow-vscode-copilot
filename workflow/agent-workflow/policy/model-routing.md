# Agent Workflow 動的モデルルーティング

## 目的

Custom Agentにmodelを固定せず、各subagent invocationの直前にjob requirementと現在利用可能なmodel集合から最低十分なmodelを選ぶ。役割・権限・tool boundaryとmodel selectionを分離する。

## Live catalog

最初に `#workflowModels` を呼び、現在VS CodeがLanguage Model APIで公開するmodelを取得する。返却値はavailability/identity/context capacityの証拠であり、知能順位表ではない。

Live catalogで確認できる主な項目:
- `name` / `id` / `vendor` / `family` / `version`
- `maxInputTokens`

APIが公開しないcost tier、thinking capability、vision/tool適合性、品質順位を推測で埋めない。必要なら現在のVS Code Language Models editor、provider公式説明、実行結果を追加証拠とする。

## Selection procedure

1. Job leaseを作り、`family / modality / context / tools / ambiguity / long-horizon dependency / harm / independence / verification ease`を固定する。
2. live catalogから明白に不適合な候補を除外する。
3. 低能力候補で不足する具体的理由がなければ、必要能力を満たす最小側を候補に残す。
4. T1/T2で独立性が必要なら、既存reviewと同一model/approachの相関を評価する。
5. 比較可能な最近の実績がある場合だけ、latency・credit/token・手戻り・完全性を利用する。
6. 最低十分な候補の中からrisk-adjusted total costが最小のmodelを選ぶ。
7. `agent/runSubagent` にmodelを明示し、開始前にユーザーへjob/model/reasoning/理由を表示する。
8. requested modelが親model cost tierを超えると親modelへfallbackするため、accepted configurationを確認する。

## Reasoning

reasoningはmodelとは別判断。現在のVS Code/providerがinvocation単位指定を公開していない場合は、必要強度だけをjob leaseへ記録し、実効値を `指定不可` または `親設定依存` とする。架空の実効値を書かない。

## No fixed mapping

次のような長期固定表を作らない。

- Reviewer = Model X
- Implementer = Model Y
- Security = 常に最上位model

model名、version、利用可否、組織policyは変わる。固定するのはselection criteriaとevidence requirementだけ。

## Parent cost ceiling limitation

VS Codeのsubagent modelは親modelのcost tierを超えられない。動的routingの選択空間を最大化したい場合は、親Workflow Orchestratorを「委譲先として使う可能性があるmodelの最大cost tier以上」で開始する。worker側はjobごとに低cost modelへ下げられる。
