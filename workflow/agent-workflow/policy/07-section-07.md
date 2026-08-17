## 7. 標準フェーズと作業種別分岐

すべての作業は、最初に次の共通準備を行う。

ただし、低リスク・短時間・read-onlyで、外部write、実装、実行環境変更、release・運用判断、金銭・security・safety・privacy上のmaterialな判断、volatile targetへの依存を伴わない照会・説明・単純reviewは、`目的と質問 / 対象と正本 / 取得時刻またはversion / 許可scope / 結論と限界` を一つのcompact recordへ統合できる。この分岐では独立した詳細manifest、細分化plan、広範baseline、時間・token budget文書を作らず、必要な正本を読み取って回答する。途中で状態変更、外部判断への転用、identity・freshness疑義、materialなrisk、複数phaseまたは長期化が発生した時点で通常準備へ昇格する。compact record自体のcostを実作業以上にしない。

```text
要求・主目的・最低必須成果・禁止代替結果・正常成功経路・設計・範囲・変更禁止範囲・受入条件・権限の確定
-> version付きwork-definition manifestの固定
-> 複数主目的時のobjective ledger・依存順・active objective固定
-> リスク分類
-> 時間予測・critical path・効率checkpointを含む詳細計画と担当割当
-> 変更前baselineの凍結
-> 作業種別の確定
```

コード、文書、ローカル設定、build・packageその他のlocal artifactを作成または変更する作業は、変更前baselineを凍結した後、目的に応じて新規実装、既存不具合修正、計画保守・移行へ明確に分岐する。各分岐の要求・設計、根因、変更準備、snapshot、早期監査、テスト・検証、release candidate、最終監査は、artifact種別に応じて「実装」を作成・編集・生成へ、「テスト」をparse・render・schema・意味・互換性・package確認等の該当検証へ読み替え、適用不能な層だけ理由付き該当なしとする。複数種別を含む場合は作業全体を一括分類せず、境界と依存関係を定めた作業パッケージ単位で分類する。分類が曖昧な部分には適用可能なうち厳しいゲートを用い、既知の不具合を含む部分は修正着手ゲート前に編集しない。

### 新規実装

既知の不具合を直すのではなく、新しい要求または挙動を初めて実装する場合は、初回実装前に存在しない根本原因を要求しない。

```text
要求・設計・受入条件・検証方法を確定
-> 新機能外のpreservation contractとplanned semantic deltaを固定
-> 設計上の介入link・共有mechanism・consumer・変更誘発failureをINT subpacketへ前向きに固定
-> 正常成功envelope・停止許可領域・初期検証母集団U0を固定し、該当時は停止合成を設計
-> 主目的・riskから実経路・behavioral oracle・判定gateまでの検証能力設計check
-> 正常経路・重大failure境界の診断性設計check
-> 設計・実装準備ゲート
-> 主目的実現ゲート
-> 初回実装
-> 実装snapshot・早期独立監査遷移
```

### 既存不具合修正

既に観測された故障、仕様逸脱、回帰、運用障害を修正する場合は、変更前baselineに加え、安全かつ許可範囲で再現可能なら再現証拠を、再現不能、危険、破壊的、または不許可なら第10節で定める複数の独立した代替証拠を起点にする。

```text
変更前baselineの確認
-> 安全に可能な場合は症状の再現と証拠保存
-> 独立して安全な残りの診断・テスト区分の継続
-> 分割診断
-> raw evidence dossierと親のprovisional causal ledgerを分離した根因因果証拠packet・診断可能性判定
-> 検出責任の適用判定とverification-escape packet
-> 条件該当時のblind-first読み取り専用根因challenge監査と親ledgerとの不一致処分
-> 根本原因の状態確定・修正着手可否判定
-> 因果介入link・共有mechanism・consumer・preservation・変更誘発failureをINT subpacketへ固定
-> 原不具合外のpreservation contractとplanned correction semantic deltaを固定
-> 正常成功envelope・停止許可領域・初期検証母集団U0を固定し、該当時は停止合成を設計
-> 修正着手ゲート
-> 主目的維持ゲート
-> 修正実装
-> 実装snapshot・早期独立監査遷移
```

### 計画保守・移行

依存関係更新、設定・schema・data移行、性能改善、挙動非変更リファクタリング、build・package変更など、既知の不具合修正でも新機能追加でもない計画変更は、この経路を用いる。

```text
変更前baselineの確認
-> 変更目的・互換性境界・移行方法・rollback・受入条件・検証方法を確定
-> preservation contractとplanned semantic deltaを固定
-> 変更する設計link・共有mechanism・consumer・変更誘発failureをINT subpacketへ前向きに固定
-> 正常成功envelope・停止許可領域・初期検証母集団U0を固定し、該当時は停止合成を設計
-> 既存検証の適用性と変更後の検証能力設計check
-> 正常経路・重大failure境界の診断性設計check
-> 変更準備ゲート
-> 主目的維持ゲート
-> 実装または移行
-> 実装snapshot・早期独立監査遷移
```

### 非コード外部状態変更

GUI、ブラウザ、SaaS、cloud、device、DB、外部APIその他の外部正本を直接変更する操作は、コード実装後の早期・最終監査経路とは別に、次の外部状態変更分岐を通す。調査、説明、review、hash取得、状態照会その他のread-only非実装作業はこの分岐の実行段階へ入れない。一方、コードを変更しないことを理由に外部writeをread-only作業として扱わない。

実行前にread-onlyで、正確なtarget、account、tenant、environment、resource ID、current state、version、依存状態を確認し、外部対象baselineとして固定する。次を含むversion付きaction manifestを作る。

- 実行する正確な操作と入力、target ID、scope
- targetについて予定するplanned effect delta、意図して変えないresource・consumer・権限・永続状態その他のpreservation contract
- planned effectが介入するstate・contract・因果link、共有resource・consumer、anticipated impact、新たに生じ得るfailure、および該当する `INT` subpacketのID
- supportedな正常成功envelope、停止を許す領域、および該当時のCONT subpacket。外部設定、feature flag、policy、DB stateその他が処理継続・可用性・throughput・回復性を変えない場合は理由付き `該当なし`
- 要求・C0、正常成功envelope、anticipated impact cone、state model、preservation contractから固定した初期検証母集団 `U0` と、各命題のpre-action・post-action検証方法
- 外部send・通知・公開の有無と宛先、不可逆効果、依存状態
- 予定時刻、回数、および一回の管理単位の境界
- 認証、権限、適用される明示確認
- 受入結果、停止条件、dry-runまたはsandboxの可否と結果
- rollbackまたはcompensationの可否、手順、必要権限
- 緊急containmentおよび有限段階recoveryの各段階について、事前承認された正確なtrigger、target、input、手順、最大回数、段階後verification
- 変動する対象を安全に束縛する許容version条件、guard・invariant、conditional writeまたはcompare-and-set precondition
- 実行後に外部正本で確認する結果、副作用、通知、永続状態

この方針は権限を拡張しない。action-readiness gateでは、work-definition manifestとaction manifestの同一性、target baselineの完全性、ユーザー権限、必要な明示確認、入力と対象、依存状態、停止条件、dry-run・sandbox、rollback・compensation、post-action verificationに加え、該当するINT・CONT subpacket、正常成功envelope、`U0` を確認する。pre-action auditのblind-first追加とanticipated impact追加を含むappend-onlyな `U1-pre` が閉じるまで、停止作用を含む外部writeを実行しない。破壊的、金銭、外部send、公開、production、不可逆な操作は、適用される高位指示および確認要件を満たすまで実行しない。

```text
外部対象baselineとaction manifestの固定
-> 権限・必要な明示確認の取得
-> action-readiness gate
-> pre-action監査要否ゲート
   -> 通常・高リスクまたはmaterial impactの合理的可能性あり:
      固定plan・action manifest・target baselineへの読み取り専用独立pre-action audit
      -> finding全収集・統合
      -> 第15節のplanned-action materiality gate
         -> PASS: 実行直前identity/freshness gateへ
         -> 修正要: 監査完了 -> 分割診断 -> 根本原因ゲート
            -> 共通修正回数台帳 -> 必要なmanifest・target baseline修正
            -> version/hash再固定 -> 必要な権限・確認の再取得
            -> action-readiness gate -> pre-action audit再実行
         -> 未証明: 追加証拠取得
            -> material・permission・target・safetyに関係または回復不能: No-Go
            -> 肯定的な非該当・非到達証拠あり: 理由付き判定へ
   -> 低リスク省略条件をすべて立証: pre-action audit省略証拠を記録
-> PASSまたは有効な低リスク省略: 実行直前identity/freshness gate
   -> PASS: 許可済みの正確な操作を一回の管理単位で実行
   -> 差異・stale・approval失効・対象不明:
      実行禁止 -> version付きbaseline supplementまたは新baseline・manifest固定
      -> 権限・確認 -> action-readiness gate -> 影響範囲のpre-action auditへ
-> 外部正本で結果・副作用・通知・永続状態を検証しactual impactを導出
-> U1-preへactual-impact追加を加えたU1-postとCONTの実作用・回復性を処分
-> post-action snapshot固定
-> 作業の性質に応じたpost-action verification・独立監査・実装経路の後段ゲート
```

pre-action audit中は対象外部状態を変更せず、操作のdry-runも状態を変えるなら監査後の許可済み実行として扱う。監査完了、全findingの統合、planned-action materiality gateの `PASS` または有効な低リスク省略、および必要な権限・確認の成立前に操作しない。`修正要` では監査を完了してから、分割診断、根本原因ゲート、共通修正回数台帳を通し、work-definition manifest、action manifest、target baselineまたはversion付きsupplementの必要部分を修正してversion・hashを再固定する。scope、effect、target、permissionが変わる場合は必要な確認を再取得し、action-readiness gateとpre-action auditを再実行する。`未証明` は追加証拠を取得し、materiality、permission、target identity、safetyに関わるものまたは証拠回復不能はNo-Goとする。対応外・到達不能を非阻害とするには肯定的証拠を要し、単なる未確認をPASSにしない。pre-action auditは、post-action verification、コード変更に適用される実装後早期・最終監査、テスト、実環境確認の代替ではない。状態変更そのものを「実装後の早期監査で後から見る」という理由で実行前監査なしに進めない。

外部write後はplanned effect deltaとactual effect delta、anticipated impactとactual impact、正常成功envelope、該当するCONTのactivation/effect reachability・`GLOBAL_CUT`・支配・回復livenessを照合する。`U1-pre` へactual-impact由来の命題を追加した `U1-post` を固定し、既存命題を削除・弱化せず、materialな `NewlyStopped`、orphan branch、未処分の副作用、回復失敗をpost-action verificationと該当する独立監査へ渡す。外部writeが成功した事実だけでこれらをPASSにしない。

実行直前identity/freshness gateでは、外部正本をread-onlyで再取得し、account、tenant、environment、resource ID、target state・version・etag・hash、依存状態、action manifest、work-definition manifest、permission・confirmation・approval identity、予定時刻・回数、guard・invariantをpre-action audit済みの値と照合する。完全一致、監査済みの許容version条件、またはconditional write・compare-and-set preconditionがPASSした場合だけ一回の管理単位を実行する。差異、stale baseline、失効したapproval、不明な対象では実行せず、元baselineを上書きしないversion付きsupplementまたは新baselineとmanifestを固定して、権限・確認、action-readiness gate、影響範囲のpre-action auditへ戻る。頻繁に変わる対象は、監査済みinvariantとfail-closedなconditional writeまたはcompare-and-setをaction manifestに定義する。対象と条件を安全に束縛できなければNo-Goとする。

操作がFAIL、部分成功、予期しない副作用、通知、永続状態差分、または受入未達になった場合は、まず安全を損なわず取得できる最小証拠を保存する。遅延が実害を拡大し、かつaction manifestに事前固定・承認された正確なtrigger、target、input、最大回数、手順をすべて満たす場合に限り、fail-closed containmentまたはrollback・compensationを診断前に一回の管理単位で先行できる。未計画の回復、scope・target・inputを変える回復、blind retryは禁止し、停止してユーザー判断を求める。緊急性がなければ、独立して安全な診断区分、分割診断、根本原因ゲート、第10節の共通修正回数台帳を先に通し、その後に許可範囲内のrecoveryだけを行う。

containmentまたはrecoveryの各段階後は必ず外部正本で結果、残存副作用、通知・送信、永続状態、権限、整合性を検証し、post-recovery snapshotを固定して共通修正回数台帳のoutcomeへ記録する。承認済みの有限段階recoveryでも各段階のtrigger、最大回数、verificationを守る。recoveryがFAIL、部分成功、またはmaterialな `未証明` なら、無断再試行せず可能な安全状態を維持して停止・報告しNo-Goとする。その後、分割診断、根本原因ゲート、共通台帳、および必要な再計画へ進む。recovery PASSは元の操作PASS、受入条件PASS、または作業完了を意味せず、元操作結果とは別の証拠層として扱う。

### コード変更と外部writeを含む複合作業の合成ゲート

一つのtaskがコード・artifact変更と外部状態変更を含む場合は、外部writeの役割を先に固定し、各分岐を独立に通したうえで次の依存順へ合成する。外部writeの権限、pre-action audit、直前identity/freshness、post-action verificationは、コード側の監査・テストで代用しない。

- sandbox、test tenant、隔離device、検証DBその他への外部writeが変更candidateの統合・実環境証拠を取得する操作なら、`実装完成 -> 実装snapshot -> 早期監査 -> 条件付きテスト移行可 -> 外部action readiness・pre-action audit・直前identity -> 一回の検証write -> post-action verification・復元 -> tested-target identity -> release candidate -> 最終監査` の順とする。検証write前の早期監査は静的scopeのPASSであり、そのwrite結果のPASSを先取りしない。
- deploy、publish、distribution、production適用、実利用者へのsendその他、release candidateを外部へ適用するwriteなら、`コード側の必須テスト・tested-target identity -> release candidate -> 最終監査PASSまたは有効な正式省略 -> 外部action readiness・pre-action audit・直前identity -> 一回の適用write -> post-action verification` の順とし、未監査candidateを外部適用しない。
- コードcandidateと因果的に独立した非コード操作は外部状態変更分岐だけを通す。両者が同じtaskに含まれても、片方のPASSを他方へ転用しない。

外部writeが検証用かrelease適用かを分類できない、同じwriteが両方を兼ねて安全な合流点を固定できない、またはproduction writeを必須テストとして先行させる必要がある場合は、勝手に順序を選ばず設計・環境・権限を再計画し、必要ならユーザー判断またはrelease No-Goとする。

### 実装snapshot・早期独立監査遷移

初回実装後、既存不具合の修正後、計画保守・移行後、mechanical preflightまたはテストFAILの修正後、監査findingまたは診断性不足の修正後は、まず実装完成度ゲートを通す。対象work packageについて、計画した変更が完了し、主目的・必須受入条件と実装箇所の対応、planned semantic delta、preservation contractが固定され、通常の対応入口から主処理、必須状態変化・副作用、最低必須成果までの静的な制御・データフローが成立し、未許可のplaceholder・stub・no-op・恒常的disable・HOLD・skipがなく、既知の未実装・対象外・未証明が記録され、snapshotへ含めるcandidate-bearing inputと生成物の境界が確定した場合だけPASSとする。actual semantic delta、impact cone、変更誘発failureはsnapshot固定後に独立導出・照合するため、作者の想定だけでこの段階にPASSさせない。未完成な部分実装を監査可能な完成snapshotとして扱わず、実装不足は実装フェーズへ、実装中に発見したfailureは分割診断と根本原因ゲートへ戻す。

実装完成度ゲートPASS後は、機能・統合・高コスト・状態変更テストより先に次の遷移へ入る。

```text
実装・修正の完了
-> 実装完成度ゲート
   -> FAIL: 未完成部分の実装継続、またはfailureの分割診断・根本原因ゲート
   -> PASS: 実装snapshot固定
-> 任意のmechanical preflight
   -> FAIL: 証拠保存 -> 分割診断 -> 根本原因ゲート
            -> 共通修正回数台帳ゲート -> 修正 -> 新しい実装snapshot固定へ
   -> PASSまたは該当なし: 監査要否ゲートへ
-> 監査要否ゲート
   -> 通常・高リスクまたは省略条件不成立:
      サブエージェント利用時は第6節のユーザー向け表示先行条件PASS
      -> 読み取り専用の早期独立監査
      -> finding全収集・統合
      -> 到達可能性・変更起因性・実害ゲート
      -> 実装構造監査を `PASS` / `修正要` / `未証明` で判定
      -> テスト準備構造screenを `PASS` / `修正要` / `未証明` で判定
      -> 後段で取得する証拠状態を別記
      -> 独立したテスト移行可否判定
   -> 低リスク省略条件をすべて立証: 早期監査省略証拠を記録
      -> 後段で取得する証拠状態を別記
      -> 独立したテスト移行可否判定
-> 実装構造監査PASSかつテスト準備構造screen PASS、または有効な低リスク省略
   / 後段必須証拠未証明
   / 条件付きテスト移行可: 検証範囲・証拠適用性ゲート
   -> 完了判定保留・release candidate固定不可で共通テスト結果遷移へ
-> 早期範囲未証明 / 安全な後段テストでのみ証拠取得可能
   / 条件付きテスト移行可: 検証範囲・証拠適用性ゲート
   -> 完了判定保留・release candidate固定不可で共通テスト結果遷移へ
-> テスト移行不可: 追加証拠取得またはNo-Go
-> 修正要: 早期監査完了 -> 分割診断 -> 製品根因・該当するverification-escape・変更誘発failureの特定
           -> 修正着手ゲート -> 共通修正回数台帳ゲート
           -> 根本原因単位の一括修正 -> 新しい実装snapshot固定へ
```

mechanical preflightは、固定snapshotの同一性を変えない隔離環境またはno-write方式で決定的かつ安価に実行できる、対象に応じたparse、compile、import、collection、schema、format等に限る。これは構文・収集・機械的不整合の証拠であり、テストPASS、機能動作、統合、性能、package、runtime、実環境を保証しない。機能・統合・高コスト・外部状態または永続状態を変える確認は早期監査後に行う。preflight結果と実装snapshotの識別情報を結び付け、実行前後のsnapshot同一性を確認する。

早期ゲートでは、`(1)` 実装構造監査の判定、`(2)` テスト準備構造screenの判定、`(3)` 後段で取得する動的挙動、統合、性能、package、runtime、GUI、実環境等の証拠状態、`(4)` テスト移行可否を、相互に上書きしない別フィールドとして記録する。実装構造とテスト準備構造に修正必須がなく、判定に十分な証拠がある場合は、後段証拠が `未証明` のままでも両早期scopeをPASSとする。安全で、隔離または復元可能で、fail-closedなテスト方法、guard、停止条件が確定していれば、`実装構造PASS / テスト準備構造PASS / 後段証拠未証明 / 条件付きテスト移行可 / 完了判定保留 / release candidate固定不可` と記録して必要なテストへ進める。後段テストPASSによっていずれかの早期scopeをPASSへ昇格させるのではなく、この分岐では両scopeが既にPASSしている。

例外として、実装構造またはテスト準備構造scopeそのものの判定証拠を安全な後段テストでしか取得できない場合は、該当scope、証拠の欠落、テストがそれを取得できる因果を明示し、`該当早期scope未証明 / 条件付きテスト移行可 / 完了判定保留 / release candidate固定不可` と記録する。後段証拠を取得した後、実装snapshotとtest-plan supplementのidentityが同一であることを確認し、テスト結果だけで自動的にPASSへ昇格させず、release candidate固定前に同じ読み取り専用対象へ該当scopeだけの限定再判定を行う。すべての該当早期scopeがPASSになった場合だけ先へ進み、`修正要` は共通修正経路またはtest-plan差分修正経路へ、`未証明` は追加証拠取得またはNo-Goへ移る。テストの安全性、隔離、復元、guard、停止条件、破壊性自体が未証明なら、いずれの条件付き移行も不可とする。宣言した隔離一時状態を復元できない、または候補へ影響しないことを証明できない場合も移行不可またはテストFAILとする。対応外または到達不能を非阻害とする場合は、対応範囲、入口、設定、状態遷移、guardまたはinvariantについて肯定的証拠を要求し、証拠がないことを到達不能の証拠にしない。

早期監査は実装完成度ゲートを通過した固定snapshotについて、高コストな動的テスト前に静的・構造的欠陥を除去するためのゲートであり、preflight、テスト、最終独立監査の代替ではない。早期監査後の実装修正では、変更差分、その責任component、直接の呼び出し元・利用先、状態・API・設定・永続化・主目的経路への影響面と、CHG packetで変化したplanned/actual delta、preservation contract、impact cone、仮説だけを原則としてテスト前に再監査し、証拠同一性を確認できる未変更範囲を毎回フル監査しない。テストmatrix・fixture・期待値・隔離・復元・停止条件だけを変更し、work-definition、candidate-bearing実装、artifact、設定、依存関係、CHG packetの根拠を変えていない場合は、同じ実装snapshotにversion付きtest-plan supplementを結び、テスト準備構造screenの変更差分だけを読み取り専用で再判定する。実装snapshotを再固定せず、実装構造監査を再実行しない。追加証拠だけで未証明を解消する場合も、同一性を確認して該当フィールドだけを限定再判定する。version付きwork-definition manifest、およびsourceと各hash・diff、設定、dependencyとlockfile、toolchain、feature flag、build・generation input、生成物hash、platform・runtime identity、environmentの該当項目すべてで同一性を証明できる未変更範囲だけ早期監査証拠を再利用する。設計・責任境界・主目的経路・API・schema・永続化・packageを変更した、planned/actual delta・preservation contract・impact cone・変更誘発failureのいずれかがmaterialに変わった、影響範囲を限定できない、証拠同一性を失った、変更が広範、または重大リスクを持つ場合は必要な広さへ再監査を拡大する。

ユーザー要求、設計、必須受入条件、planned semantic delta、preservation contract、許可scope・対象外、変更禁止範囲、権限・必要な明示確認、比較baselineのIDまたは証拠manifest・完全性、監査対象範囲・観点IDのいずれかを変更、追加、または補完した場合は、技術hashが同じでも影響範囲の早期監査証拠を再利用しない。要求・受入・権限ゲートを再評価し、受入マッピング、CHG packet、テストマトリクスを更新して影響範囲を再監査する。実装変更が必要なら通常の修正、実装snapshot固定、早期監査、共通テスト結果遷移へ戻る。実装変更が不要でも、work-definition変更により必要になったテストだけを再実行し、無関係で同一性を立証できるテスト証拠は再利用できる。

### 検証範囲・証拠適用性ゲート

実装を伴う作業では、早期監査または有効な低リスク省略の後、テストその他の後段証拠取得へ移る前に、主目的ID・必須受入条件・証拠層ごとに必要な検証範囲を決める。read-onlyの調査・診断・reviewではbaselineと情報源を固定した後、外部状態変更ではaction readinessとpre-action auditの各段階で、それぞれ同じ軽量判定を作業種別に読み替えて行う。軽量な範囲判定は常に行うが、version付きの詳細な証拠ブリッジは、利用可能な既存証拠があり、再検証costがmaterialな場合だけ作る。影響分析、証拠ブリッジ作成、照合の合計costが安価な再実行以上なら、ブリッジを作らず再実行する。

各項目を、次のいずれかへ分類する。

- `新規証拠必須`: 新しい要求、変更した経路、現在candidate固有の成果、またはfreshnessが必須であり、現candidateから証拠を取得する。
- `直接適用可`: candidate-bearing identity、work-definition、環境、前提、freshnessが同一で、既存証拠を同じ対象へ直接適用できる。
- `証拠ブリッジで継承`: 対象identityは変わったが、差分と肯定的な非影響証拠により、既存証拠が支える受入条件の成立範囲を現candidateへ対応付けられる。
- `限定再検証`: 変更component、直接境界または一つの証拠層だけを再検証する。
- `影響経路再検証`: 変更から到達可能なcontrol・data・state・consumer・integration経路を再検証する。
- `全面失効`: 影響範囲を限定できない、identityまたはfreshnessを失った、設計・責任境界が変わった、または重大riskがあり、該当証拠層を全面再検証する。
- `未証明`: 適用可否を決める肯定的証拠が不足する。
- `該当なし`: 当該目的・受入条件・作業種別に適用しない理由が明確である。

影響分析では、control・data・state遷移、return・exception、retry・timeout・fallback・recovery、concurrency・lock・queue・同期I/O、CPU・memory・disk・network・latency、API・schema・設定・feature flag、build・package・runtime、GUI・外部環境、logging・telemetry・診断性を必要な範囲で確認する。特定のファイル名、変更種別、または「ログだけ」等のラベルだけで非影響と判断しない。

証拠ブリッジには、既存candidate・証拠ID、現candidate ID、正確なdiff、対象の主目的・受入条件ID、元証拠の環境・時刻・設定・dependency、freshnessとdrift、変化した前提と不変の前提、肯定的な非影響証拠、現candidateで行う限定検証、拡大条件・停止条件、残存riskを記録する。既存artifactのPASSを現artifactのPASSへ名称だけで付け替えず、既存証拠が依然支える受入条件と非影響範囲を対応付ける。変更層、現artifact・package・runtime固有の同一性、およびfreshnessが必要な層には現candidateの新規証拠を要求する。

新規実装では新しい主目的・受入条件に新規証拠を要求し、既存挙動の非回帰など変更非影響を立証できる層だけ既存証拠を適用する。既存不具合修正では根本原因、変更経路、再現症状、目的回復へ新規証拠を要求し、非影響を立証した周辺だけ継承する。保守・移行では互換性、schema・data、rollback、build・package、性能その他の変更対象へ新規証拠を要求する。read-onlyの調査・診断・reviewでは実装snapshotを要求せず、情報源、取得時刻、coverage、freshness、driftと時間checkpointから証拠適用性を判定する。非コード外部状態変更では第7節の実行直前identity/freshness gateが常に優先し、古いtarget・account・permission・versionの証拠を実行準備PASSへブリッジしない。

検証levelは `再実行なし`、`限定・差分`、`影響経路`、`全面` の最小十分なものを選び、FAIL、未証明、drift、影響範囲の非限定、または想定外差分があれば一段以上拡大する。高risk、volatileな外部状態、または検出前に不可逆な金銭・安全・data・security実害が生じ得る場合は、証拠ブリッジを防止・封じ込め・現在状態の必須検証の代用にしない。必須受入条件の証拠が揃い、拡大条件がなくなった時点で検証拡大を終了する。全面再検証のcostと、影響分析・ブリッジ・限定検証のcostに誤継承時の実害を加えた値を比較し、risk調整後の総costが小さい経路を選ぶ。

### 共通テスト結果遷移

早期独立監査でテスト移行可能と判定された実装snapshotに対する分割テストと再テストは、同じ結果遷移に従う。

```text
分割テストまたは再テスト
-> PASS: テスト網羅性確認
         -> 必要に応じた全体回帰テスト
         -> 早期範囲結果ゲート
            -> 既に早期監査範囲PASSまたは有効な低リスク省略: テスト対象同一性ゲートへ
            -> 早期範囲未証明の条件付き移行:
               同一実装snapshot identity確認 -> 読み取り専用の限定再判定
               -> PASS: テスト対象同一性ゲートへ
               -> 修正要: 共通FAIL修正経路へ
               -> 未証明: 追加証拠取得またはNo-Go
         -> テスト対象同一性ゲート
         -> 同一性PASSかつ受入必須の後段証拠PASS: release candidate固定
            -> 最終監査要否ゲート
            -> 通常・高リスクまたは省略条件不成立: 最終独立監査へ
            -> 低リスク省略条件をすべて立証: 最終監査省略証拠を記録
               -> 完了判定へ
         -> テスト実行がcandidate-bearing層を予期せず変更: 当該partitionのFAIL
            -> 証拠保存 -> 安全な残りpartition -> 分割診断 -> 根本原因ゲート
            -> 共通修正回数台帳 -> 修正 -> 新しい実装snapshot固定
            -> 早期差分監査 -> 影響範囲に必要な分割テストへ戻る
         -> テスト外で対象内差分あり: 新しい実装snapshot固定
            -> 早期差分監査 -> 影響範囲に必要な分割テストへ戻る
         -> 証拠metadataのみの差分: 非影響を立証・記録
            -> release candidate固定へ
-> FAIL: 証拠保存
         -> 独立して安全な残りの診断・テスト区分の継続
         -> 分割診断
         -> 根本原因・該当するverification-escapeの特定
         -> 修正着手ゲート
         -> 共通修正回数台帳ゲート
         -> 修正実装
         -> 新しい実装snapshot固定
         -> 変更差分と影響面の早期再監査
         -> 分割再テストへ戻る
```

FAILまたは受入条件に必須の未証明があるテスト結果からrelease candidate固定または最終監査へ進まない。条件付き移行で取得する予定だった必須の後段証拠がPASSすれば完了判定保留を解消候補にできるが、実装構造監査またはテスト準備構造screenの判定をテスト結果で代用しない。該当早期scope未証明の例外は同一snapshot・test-plan identityへの限定再判定PASSを別途必要とする。後段証拠がFAILまたは取得不能、限定再判定が修正要または未証明ならrelease candidate固定不可を維持する。テスト網羅性確認で漏れが判明した場合、全体回帰テストがFAILした場合、またはテスト実行がcandidate-bearing identityを予期せず変えた場合も同じFAIL遷移へ入る。テストFAILの実装修正後に早期差分監査を省略して直接再テストしない。test planだけを修正した場合は、第7節の限定再screen後に該当する分割テストへ進む。

release candidate固定後は次の最終監査結果遷移に従う。

```text
必要な最小coverageによる最終独立監査
（サブエージェント利用は第6節の利用ゲートとユーザー向け表示先行条件の通過後のみ）
-> baselineとの比較
-> findingの全収集と根本原因単位の統合
-> 到達可能性・変更起因性・実害ゲート
-> PASS: 完了判定
-> 修正要: 監査完了 -> 分割診断 -> 根本原因・該当するverification-escapeの特定
           -> 修正着手ゲート -> 共通修正回数台帳ゲート
           -> 根本原因単位の一括修正
           -> 新しい実装snapshot固定 -> 早期差分監査
           -> 共通テスト結果遷移
-> 未証明: 追加証拠取得または阻害要因の明示
           -> release candidate変更なし: 再固定せず同じrelease candidateを再監査
           -> 変更あり: 新しい実装snapshot固定 -> 早期差分監査
                     -> 共通テスト結果遷移
           -> 必須証拠が現時点で不足: release No-Goを維持して目的進捗・収束性ゲートへ
              -> 許可された代替証拠または合理的な回復見込みあり: 証拠取得・再計画
              -> 回復不能かつ代替経路なしで第4節の限定条件成立: 完了No-Go
           -> 対応外・到達不能・任意確認のみ: 理由付き残存リスクとして完了可否を判断
```

同一対象・同一jobについて、診断と修正、実装変更とその独立監査、監査とfinding修正、テストとcandidate変更を同時進行させない。相互に独立し所有境界が分離された別packageは第6節の並行化ゲートに従える。根因challenge、pre-action audit、早期監査、最終監査は第2節と各専用分岐の正規順序へ置き、後段監査規則を理由に前段監査を省略・遅延しない。低リスクの正式監査省略は第14節の条件をすべて立証した明示分岐に限り、暗黙に省略しない。調査、説明、レビューなどread-onlyで実装も外部writeも伴わない作業は、必要な証拠を取得した時点で該当しない後続フェーズを省略できるが、省略理由、適用した監査形態、未証明事項を記録する。

