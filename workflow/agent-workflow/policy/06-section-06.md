## 6. サブエージェントの利用

サブエージェントは作業効率を上げ、目的達成を早め、または必要な独立性・品質を合理的なcostで得るための手段であり、使用自体を目的としない。探索・実装等のworker割当と、検証の独立性確保を別々に判定する。呼出し前に次の利用ゲートを通し、見込まれる利益がcostを上回る場合だけ、独立して安全に進められる作業を境界の明確な作業パッケージとして委譲する。

### サブエージェント利用ゲート

親は少なくとも次を簡潔に比較する。

- 利益: critical pathと完了時間の短縮、独立作業の同時進行、専門性または異なる監査観点による誤判定リスクの低下、親が安価かつ確実に検証できること。
- cost: context抽出と指示作成、起動・待機・進捗管理、重複調査、共有状態や編集範囲の調整、成果統合と再検証、誤解または不完全な成果による手戻り。

次の場合は原則として探索・実装workerには使用しない。ただし、この判断を独立reviewの不要判定へ転用せず、第4節の独立閉包・多角的二鍵ゲートで別に決める。

- 親が短時間で完了できる単純または機械的な作業。
- 前工程への依存が強く、実質的に並行化できない作業。
- 同じファイル、環境、processまたは外部状態を競合操作する作業。
- 委譲に必要な説明量が実作業量と同等以上になる作業。
- 親が成果を検証するために同じ作業を全面的にやり直す必要がある作業。
- 同じartifactと同じ観点を複数エージェントが重複確認するだけの作業。

モデルと推論強度の選定は、利用ゲートで委譲が有益と判断された後に行う。高性能モデルを選択できること自体を委譲の理由にしない。実行中に待機、重複、阻害、品質不足等によって利益が失われた場合、親は追加委譲を停止し、統合、再割当、直列化、または直接処理へ切り替える。

### 委譲機会checkpoint

subagentの利用が許可されtool上で利用可能な場合、非trivialな探索・実装phaseの開始、critical pathまたは作業分解のmaterialな変更、長い待機・阻害、当初時間rangeの超過、独立packageの新規発生時に、委譲機会を一度だけ再評価する。親は、`(a)` critical path短縮または専門性のためのreadyな探索・実装worker packageと、`(b)` 独立閉包・多角的二鍵ゲートで未解消となった検証packageを区別し、直接実行時間、指示・起動・待機・共有状態調整・統合・再検証cost、予想するwall-clock短縮、品質・独立性・誤判定riskへの効果、編集・環境競合を簡潔に比較する。package、critical path、見積りが変わらない同一phaseで毎step再評価しない。

期待するrisk調整後純利益が正なら、権限と所有境界を満たすbounded packageを委譲または安全に並行化する。負なら親が直接実行し、具体的な非委譲理由を一行で記録する。非trivialな作業でworker候補を一度も列挙せず「親の方が速い」とだけ判断しない一方、agent数、同時実行枠、実装worker数を成果指標またはquotaにしない。検証packageはworker非委譲理由から独立に判定し、独立性が必要なら最小scopeで割り当てる。予測より親作業が長期化した場合は、当初の非委譲理由を自動維持せずcheckpointを再実行する。

各作業パッケージには、次を含める。

- 対象範囲と対象外範囲
- 読み取り・変更権限
- 期待する成果物
- 完了条件と証拠形式
- 他の作業との依存関係
- 使用可能な共有リソース
- 親へ返すべき要約、finding、未証明事項

同じファイル、DB、ブラウザ、ポート、プロセス、外部API、実行環境を複数エージェントが同時操作しないよう、所有権または分離環境を設定する。競合や状態汚染の可能性がある場合は、速度より直列実行と再現性を優先する。

### Subagent invocation lease・stateless同一性ゲート

VS Code Copilot の subagent は invocation ごとに stateless であり、親は完了した同一subagentへ follow-up message を送れない。したがって、各 invocation を一つの独立した bounded job execution として扱い、開始前に version 付き invocation lease を固定する。lease には、job ID、attempt ID、対応する主目的・受入条件ID、phaseと役割、対象artifact・snapshot・evidence identity、scope・対象外・権限、期待成果物と証拠、T0/T1/T2 route、担当risk vector・反証命題・正本・対象外観点、選定したmodel、要求reasoningまたは `指定不可`、想定時間range、完了条件、親の統合・検証方法、phase gateに必須か任意かを含める。

同じjobの追加作業が必要でも、以前のsubagent contextを継承したfollow-upとはみなさない。terminal結果を親が固定し、次のinvocationで必要な元要求、正本、固定identity、前回のterminal outputのうち必要最小限だけを明示的に再投入する。blind-first独立性が必要なroot-cause challenge、早期監査、最終監査、pre-action auditでは、以前の結論や親の因果解釈を初回導出前に再投入しない。

同じ job ID を再利用できるのは、主目的・受入条件、phase・役割、artifact・snapshot、監査観点、scope・権限、必要model class、独立性要件が同じで、前回terminal結果を受けた追加attemptである場合だけとする。役割、目的、artifact、監査角度、独立性、必要能力がmaterialに変わる場合は新しいjob IDとする。agent名、model名、prompt表現だけを変えて同じjobを新規jobとして扱わない。

VS Code の `agent/runSubagent` で custom agent を用いる場合、custom agent は role・tools・authority を固定する器として使い、`model` frontmatter は原則として設定しない。model は親orchestratorが invocation ごとに動的選定して明示指定する。subagent model の明示指定は custom agent の model より優先される一方、要求modelが親modelのcost tierを超える場合は親modelへfallbackするため、この制約をjob leaseへ記録し、必要なdelegation ceilingを満たす親modelをユーザーが選択しているか確認する。

### Subagent実行・再invocation・retireゲート

subagent開始後、親は同一invocationへ途中のfollow-upを送れないことを前提とする。running invocationがscope内で進行し、phase gateに必要ならterminal結果を待つ。同じjobを重複spawnせず、相互に独立し共有状態を競合しない別packageだけを並行実行する。

terminal結果を受けた後は、最新のjob lease、成果のphase必須性、得られた証拠、残りcostと期待利益から次を選ぶ。

- `完了`: 期待成果物・証拠が揃い、親が正本と照合できる。
- `同一job再invocation`: job identityは同じで、限定的な不足、明確な追加識別証拠、または成果形式不足があり、新しいattemptの期待純利益が正である。前回結果を必要最小限だけ入力し、同じ証拠しか増やさない再実行をしない。
- `retire`: scope逸脱、無関係作業、同一証拠しか増えないloop、対象identity失効、能力不足、tool failure、または追加attemptの期待利益がcostを下回る。partial outputと未証明を保存する。
- `新規job`: 目的、artifact、phase、役割、監査角度、独立性、必要能力、または因果・証拠経路がmaterialに変わる。以前のjobをterminal分類してから新しいjob leaseを作る。

親が先に仮結論へ到達したことや、進捗表示が少ないことだけで必須invocationを無効化しない。phase gateに必須の独立reviewはterminal結果、正確な技術的阻害、有効な正式省略、ユーザー承認済みscope変更、または対象操作・release No-Goへ確定するまでPASSとして扱わない。

context compaction、resume、window reload、親agent交代後はdurable checkpointとjob ledgerを再取得し、同じjobのterminal結果を失ったことを理由に無条件respawnしない。新規invocationは、新しいattemptが変え得る判定とdecision-bearing evidenceを明示できる場合だけ開始する。

### Model・reasoning動的選定ゲート（VS Code Copilot）

model名や固定順位を長期規則にしない。subagent invocation直前に、同梱する `#workflowModels` extension toolまたはVS Codeの現在のLanguage Models表示から利用可能modelを再取得する。`#workflowModels` は `vscode.lm.selectChatModels()` に基づくlive catalogであり、少なくともname、id、vendor、family、version、maxInputTokensを返す。利用可能model集合は変化し得るため、古いcatalogを固定表として使わない。

modelとreasoningは独立した二つの判断とする。まずjob leaseから必要能力を固定し、次にlive catalogと現在取得できる公式説明、現jobに近い比較可能な実績から最低十分な候補集合を作る。固定model名への役割割当はしない。

選定では少なくとも次を順に判定する。

1. `hard capability`: 必要context量、agent/tool適合性、必要modality、provider/organization制約を満たさない候補を除外する。catalog metadataだけでtool calling、vision、thinking、billing tier等を証明できない場合は、VS Codeの現在のModel Manager表示、providerの公式説明、または実行環境のaccepted/fallback結果で補う。推測だけで能力を付与しない。
2. `job difficulty`: job family、曖昧性、長期依存、因果推論深度、要求完全性、変更影響、証拠衝突、誤判定実害を評価し、必要model classを決める。
3. `independence`: blind-first T1/T2で相関見落としがmaterialな場合、既存reviewと同一model・同一approachの反復より、要件を満たす別modelまたは別手段を優先する。
4. `cost / latency`: 能力を満たす候補の中でrisk調整後総costとlatencyが最小の候補を選ぶ。最上位modelが存在すること自体を選択理由にしない。
5. `empirical evidence`: model version、tool、job family、評価条件が比較可能な最近の実績があれば、完全性、手戻り、latency、credit/token costを補助証拠にする。環境またはmodel versionが変われば自動継承しない。

数値性能やcostをVS Code APIが公開していない場合、架空のscoreを作らない。区別に十分な証拠がなければ、必要能力を満たすことが確認できる現在の親model、VS Code Auto、またはユーザーが利用可能と確認した候補を使い、選定限界をjob leaseへ残す。

VS Codeでは親agentが `agent/runSubagent` 呼出時にmodelを明示指定でき、その指定はcustom agentの`model`より優先される。そのため本構成のcustom agentsは原則modelを固定しない。ただし要求modelは親modelのcost tierを超えられず、超える要求は親modelへfallbackする。高いdelegation ceilingが必要なtaskでは、親orchestratorのmodelをそのceiling以上にユーザーが選択する。親を高能力modelにしても、workerは各jobで低cost側へ動的に下げられる。

reasoning effortは、現在のVS Code/providerがsubagent invocation単位で明示指定できる場合だけ指定する。明示指定fieldがない場合は、必要reasoningをjob leaseへ `requested reasoning` として記録し、実効値を推測せず `指定不可`、`親設定依存`、または確認できる実効状態として記録する。reasoning最大値を品質の代名詞にしない。

すべてのsubagent invocationより前に、ユーザーへjob名・目的、選定した現在利用可能model名、要求reasoningまたは指定不可状態、短い選定理由を表示する。model catalog取得不能、model指定不能、fallback、拒否、組織policy、cost-tier制約その他で設定を立証できないmandatory jobは `設定未証明` とし、独立証拠PASSへ使わない。

model catalog tool自体は選定を代行しない。これはlive availabilityとidentity evidenceを提供するだけであり、最終選定はwork-definition、job lease、risk、独立性、現在の公式model evidence、最近の比較可能実績を統合してorchestratorが行う。

