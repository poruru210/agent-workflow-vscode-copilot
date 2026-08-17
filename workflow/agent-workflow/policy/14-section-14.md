## 14. 二段階の非テスト依存独立監査

独立監査は、テスト結果だけに依存して合否を判断しない。テストは最終監査の補助証拠として利用できるが、監査者は変更前baselineと固定snapshotを現物で比較し、変更により新たに生じた問題、悪化した問題、変更前から存在した問題を区別する。監査入力には有効なversion付きwork-definition manifest、比較baselineとsupplementの証拠manifest・完全性、監査対象範囲・観点IDを含める。`実装構造監査`、`テスト準備構造screen`、`後段証拠状態`、`テスト移行可否`、`テストPASS`、`最終独立監査PASS` は別の証拠層または状態として報告し、一つの結果で他を上書きしない。

各監査は第4節のEvidence Routeとrisk vectorを既存phaseへ適用する。T1では未解消vectorを一つのbounded reviewへまとめ、T2では相関した見落としを断つ必要があるvectorだけを別reviewer、model、contextまたは独立手段へ分離する。通常・高リスクで確保する観点数はagent数ではなく非重複vectorのcoverageとし、同一reviewerが複数vectorを扱う場合も各命題と結果を別々に記録する。同じmodel、prompt、artifact、証拠、既存結論を反復しただけの確認を独立coverageへ加算しない。

初回監査は固定scopeの必要claimを扱う。再監査は第10節の監査・検証往復収束ゲートとEvidence Dependency Mapを通し、失効したclaim、未解消vector、追加されたactual-impact claimだけを対象にする。全体hashの変化は新identityを示すが、それ自体を全claim失効または全文再読の理由にしない。監査者にはclaimを判定するための最小十分な正本・diff・依存context・preservation contractを渡し、境界を証明できない、共有contractへ到達する、またはmaterialな反証findingが出た場合だけscopeを段階的に拡大する。

監査者は初回finding固定前に、元要求・正本、baseline、固定対象、許可scope、supported contractから `C0` と担当vectorをblind-firstで確認する。candidate-bearing変更では、作者のCHG packet、PASS判定、修正意図、test plan、既存仮説、他reviewerの結論を不必要に与える前に、固定diffからplanned/actual delta、impact cone、保存契約違反、変更誘発failureを独自導出して初回findingを固定する。その後に作者の記録と照合し、テスト結果は初回観察後のevidence reconciliationで使用する。最終監査に必要なテスト、runtime、package、実環境証拠はこの順序で使用し、blind-firstを理由に必須証拠を省略しない。

### 早期独立監査

早期独立監査は、実装完成度ゲートを通過した固定実装snapshotに対し、変更後テストより先に読み取り専用で行う。部分実装、既知のplaceholder、または正常成功経路が成立していない状態を、監査可能な完成snapshotとして繰り返し監査しない。サブエージェントへ委譲する場合は、監査開始のtool callより前に第6節のユーザー向け表示先行条件を通過する。task cardや監査名の表示だけで代用しない。主な観点は次のとおりとする。

- 主目的ID、最低必須成果、禁止代替結果、設計、受入条件と実装差分の一致
- 通常の対応入口から主処理、必須状態変化・副作用、最終利用者の成果までの正常成功経路
- early return、disable、HOLD、skip、reject、fallback、fail-closed、feature flagが通常成功経路を不当に遮断しないこと
- 該当するCONT subpacketについて、全停止作用のblind-first inventory、activation/effect reachability、合成順序、`GLOBAL_CUT`、dead・完全支配guard、正常成功envelopeと `NewlyStopped`、全guard有効時の正常経路、回復liveness
- baselineからの要求外変更、明白なエンバグ、デグレ、既存機能破壊
- RCのblind-first二鍵と不一致処分、INTの介入link・共有mechanism・consumer・counterfactual・preservation予測、およびCHGのactual delta・双方向impact coneが整合し、親の根因仮説、症状修正または既存テストだけへ過適合していないこと
- CHG packetのplanned/actual semantic delta、preservation contract、双方向impact cone・cut proof、到達可能でmaterialな変更誘発failureと、INT予測外の作用を見落としていないこと
- 呼び出し元、対応入口、最終利用者までの制御フローとデータフロー
- 状態遷移、所有権、guard、invariant、cleanup、shutdown
- API、CLI、設定、data/schema、保存形式、運用手順の互換性
- 例外、タイムアウト、部分失敗、再試行、並行性、排他、競合
- first fault、reason code、相関情報、根本原因の責任層、影響範囲、cleanup・containment・recoveryを再構成できる診断可能性
- 逆方向の依存関係と影響面
- テスト設計、テストが実経路を通るか、欠落した正常系・異常系・境界条件
- `U0` が要求・C0・正常成功envelope・planned impact・state・preservation contractから固定され、`U1` が追加のみで構成され、after-the-factな削除・oracle弱化・threshold変更・fixture差替え・candidate汚染・materialなorphan branchがないこと
- 新規・保守では検証能力map、修正ではverification-escape packetと対策が、要求・risk、fixture、supported実経路、behavioral oracle、report・CI・release gateまで一貫し、症状だけへ過適合していないこと
- VMとTEST-RCが該当する場合、supported state・identity lifecycle・event family・partial order・clock domain・observer-effect・assertion dependency・masked assertionが固定され、単一成功時系列または次のassertionへの過適合がなく、継続・退出・代替証拠が主目的上の価値で判定されていること

同じ固定snapshotに対する一回の早期監査から、次の二出力を分けて確定する。

1. `実装構造監査`: 要求・設計・差分、正常成功経路、制御・data flow、状態、API・互換性、例外・並行性、明白な回帰、診断可能性構造に加え、RC/INTの予測とCHGの静的に判定可能なactual delta、preservation contract、impact cone・cut proof、予測内外の変更誘発failure、および該当するCONT subpacketの正常成功envelope、停止合成、支配・dead guard、回復livenessの構造を `PASS`・`修正要`・`未証明` で判定する。
2. `テスト準備構造screen`: 主目的・必須受入条件と実経路を必要な分割テストへ対応付け、明白に欠落した正常系・異常系・境界、fixture、隔離・復元、停止条件、診断観測点、candidate identityに加え、該当する検証能力map、verification-escape packet、VM・TEST-RC、RC仮説を反証するoracle、INT/CHGと監査者の未閉包な変更誘発failure仮説の和集合、preservation contract由来のbehavioral oracle、`U0`・`U1` の追加専用履歴、assertion dependency・masked assertion、CONT必須case、test-intervention ledger、orphan branch、report・CI・release gate、および検証系修正の継続・退出・代替証拠の構造までを `PASS`・`修正要`・`未証明` で判定する。これは実行後の動的妥当性、coverage数値、package・runtime・GUI・実環境PASSを判定しない。

両出力を同じ報告にまとめても、判定と修正対象は混同しない。実装修正は新しい実装snapshotを必要とするが、早期再監査scopeは第10節の収束ゲートとEvidence Dependency Mapで失効した実装claim・risk vector・追加impactに限定する。test planだけの修正は、candidate-bearing identityとwork-definitionが不変であることを確認し、version付きtest-plan supplementを固定してその差分だけを再screenし、実装構造監査を再実行しない。同じreview keyを理由なく再監査せず、再入場は対象・依存前提の変更、identity喪失、または特定の未証明・既存結論を変え得る新証拠がある場合に限る。

早期監査は静的・構造的観点を中心に、高コストなテスト前に修正可能な欠陥を除去する。動的挙動、統合結果、性能、package、runtime、GUI、実環境のPASSを早期監査の完了条件にせず、それらの未証明だけを理由に静的・構造的修正を要求しない。両対象範囲に修正必須がなく判定証拠が十分ならそれぞれPASSとし、後段証拠は別に `未証明` と記録できる。後段証拠の未証明を理由に既に立証した早期scopeを未証明へ戻さず、逆に後段テストPASSを早期scope PASSの代用にしない。早期scopeそのものを安全な後段テストでしか判定できない例外では、第7節の条件付き移行、同一snapshot・test-plan identity確認、およびrelease candidate固定前の読み取り専用限定再判定を必須とする。早期監査はテストと最終独立監査の代替ではない。

### 最終独立監査

最終独立監査は、固定したrelease candidateに対し、早期監査の証拠とテスト証拠を入力にして読み取り専用で行う。サブエージェントへ委譲する場合は、監査開始のtool callより前に第6節のユーザー向け表示先行条件を通過する。baselineからrelease candidateまでを比較し、特に次を確認する。

- 早期監査後の修正・生成・設定差分と、その影響面
- 分割テストと全体回帰の対象、実経路、結果、未実行範囲
- 該当する検証能力mapまたはverification-escape packetについて、pre-fix・controlled-fault・代替感度証拠、fixed candidateの結果、実経路、behavioral oracle、report・CI・release gateが実際に成立したこと
- 該当するVM・TEST-RCについて、state・identity・event family・ordering・clock・observer・oracle・assertion dependency、同根因sibling、修正予測、test intervention、退出・代替証拠・保留claimが一貫し、invalid・masked・deferredな検証をPASSへ変換していないこと
- RCのraw identity、blind-first二鍵、親・監査者の不一致処分、INTの介入link・共有mechanism・consumer・counterfactual predictionと、実際の修正・後段証拠が一貫すること
- CHG packetについて、planned/actual delta、preservation contract、impact cone・cut proof、作者と早期監査が導出した変更誘発failure、後段の実経路・behavioral oracle・動的証拠、早期監査後の差分、残存riskが一貫して閉じていること
- 該当するCONT subpacketについて、正常成功envelopeと `NewlyStopped`、全guard有効時の正常経路、activation/effect reachability、支配・dead guard処分、`GLOBAL_CUT`、sticky stop、回復成功・試行枯渇・不正resume拒否、およびavailability・throughput・資源への合成作用が閉じていること
- `U0` から `U1`、実行結果までの選択履歴、after-the-factなtest intervention、未実行・quarantine、candidate・共有state汚染、materialなorphan branchが正しく処分され、都合のよいPASSへ変換されていないこと
- 動的な状態遷移、異常系、並行性、統合、終了・復旧挙動
- 性能、latency、throughput、負荷、メモリ、handle、接続その他の資源使用
- 永続化、migration、再起動、復旧、rollback後の整合性
- GUIの表示、入力、操作経路、状態反映、既存ユーザーフロー
- source、生成物、package、配布物、実行中runtimeの内容、hash、設定、経路の同一性
- 外部サービス、ブラウザ、デバイスその他の実環境との整合
- baselineからrelease candidateまでの要求外変更、回帰、既存問題の到達可能化・悪化・検出困難化

実装snapshotからrelease candidateまで変更されていないclaimは、version付きwork-definition manifest、Evidence Dependency Map、および対象sourceと各hash・diff、設定、dependency・lockfile、toolchain、feature flag、build・generation input、生成物hash、platform・runtime identity、environmentの該当依存項目で証拠同一性を確認できる場合に限り、早期監査証拠をreview keyごと再利用する。ユーザー要求、設計、必須受入条件、許可scope・対象外、変更禁止範囲、権限・必要な確認、比較baselineのIDまたは証拠manifest・完全性、監査対象範囲・観点IDが変更、追加、補完された影響claimでは、技術hashが同じでも早期監査証拠を再利用しない。要求・受入・権限ゲート、受入マッピング、テストマトリクスを更新し、失効claimと追加impactを再監査して、変更により必要になったテストだけを再実行する。実装変更が必要なら通常の修正、snapshot、限定早期再監査、テスト遷移へ戻る。最終監査はC0・成果鍵、未解消claim、早期監査後の差分、動的・統合・出荷・実環境証拠、および証拠継承の妥当性へ重点を置き、継承済みの不変claimを全文再監査しない。ただしR3、dependency境界不明、証拠同一性喪失、または重大な反証findingがある場合は必要範囲を拡大する。

最終監査は、検証範囲・証拠適用性ゲートの分類、証拠ブリッジのdiff・identity・freshness・非影響根拠、現candidateの限定検証、拡大条件の発生有無を確認する。既存証拠の再利用件数や再検証の省略自体を効率の成果とせず、必須受入条件を支える現在有効な証拠と総costの比例性を判定する。

### 外部状態変更の実行前独立監査

第7節の非コード外部状態変更では、通常・高リスクまたはmaterial impactの合理的可能性がある場合、実行前に固定したwork-definition manifest、action manifest、正確なtarget baselineへ読み取り専用の独立pre-action auditを行う。監査者は対象account・tenant・environment・resource/current state、権限・明示確認、正確な操作・入力・回数、planned effect delta、許可side effect、preservation contract、INTの介入link・共有resource・consumer・新規failure予測、anticipated impact cone、外部send・通知・不可逆効果、依存状態、停止条件、dry-run・sandbox、guard・invariant、rollback・compensation、受入結果、post-action verificationの整合と欠落を確認する。停止作用が該当する場合は、正常成功envelope、CONTのguard inventory・合成・`NewlyStopped`・回復liveness、`U0` をblind-firstで反証し、監査追加とanticipated impact追加を含むappend-onlyな `U1-pre` を確定する。監査中に対象外部状態を変更せず、全findingを収集・統合した後、第15節のplanned-action materiality gateで `PASS`、`修正要`、`未証明` を判定して監査を終了する。

pre-action auditの再入場も第10節の収束ゲートを通す。action manifest、target、permission、planned effect、依存stateまたはfreshnessが変わったclaimだけをEvidence Dependency Mapから失効させ、影響範囲を再監査する。volatile targetのfreshness再取得は必須だが、freshness値が変わった事実だけで不変な権限・操作意味・rollback・consumer claimを全再監査せず、監査済み許容条件またはguardの外へ出た依存claimだけを再判定する。

`PASS` または厳格な低リスク正式省略だけを実行直前identity/freshness gateへ渡す。`修正要` と `未証明` を実行許可として扱わない。修正によりwork-definition、action manifest、target baseline、scope、effect、permission、guard、rollbackが変わる場合は、新しいversion・hash、必要な再確認、action-readiness gate、影響範囲のpre-action auditを必要とする。追加証拠だけで対象が変わらない場合も、同じ固定対象へ読み取り専用で判定し直し、未確認をPASSへ自動昇格させない。

低リスクでpre-action auditを省略できるのは、下記の正式監査省略条件を外部操作へ読み替え、target baseline、action manifest、権限・確認、可逆性、外部効果の非material性、post-action verificationをすべて肯定的に立証し、独立した省略記録を残した場合だけとする。pre-action auditは実装後の早期監査または最終監査の代替ではなく、post-action verificationもpre-action auditの代替ではない。外部状態変更後は作業の性質と実害に応じてpost-action snapshotへの独立監査を行う。

### 正式監査省略の低リスク分岐

早期監査と最終監査はそれぞれ独立に要否を判定する。正式監査を省略できるのは低リスク作業であり、次の条件をすべて証拠化した場合に限る。

- 変更が機械的、局所的、容易に復元可能である。
- 呼び出し元、依存先、状態、利用者を含む影響面が明確で限定される。
- 変更前baseline、diff、実装snapshot、該当する場合はrelease candidateの識別情報とhashが固定されている。
- 適用可能な安価で決定的な機械確認がPASSし、その対象と限界が記録されている。
- 必須受入条件ごとの証拠があり、未証明と残存リスクが明記されている。
- 挙動、API、設定、永続化、build・package・配布物、runtime、性能、GUI、外部サービス・デバイスその他の外部状態へmaterial impactを与える合理的な可能性がなく、その非影響を肯定的証拠で説明できる。
- 第4節の独立閉包・多角的二鍵ゲートで `C0` を含むすべての必須命題が `T0 決定的閉包` または独立根拠を持つ `理由付き該当なし` へ解決され、要求集合の漏れ、意味解釈、完全性、否定命題、side effect、到達可能性、変更影響、対象同一性に親の判断だけへ依存する不確実性が残っていない。
- candidate-bearing変更では、planned/actual delta、preservation contract、impact cone・cut proof、変更誘発failureが第4節の汎用T0条件および第10節の変更誘発故障・保存契約ゲートにより決定的に閉じ、human judgmentまたは未証明が残っていない。

通常・高リスク、上記のいずれかが未証明、material impactの可能性がある、または合理的疑義がある場合は省略しない。低リスクというラベル、作業の簡単さ、差分の短さ、親のself-review、テストPASSだけを省略根拠にしない。親が成果物と確認方法の双方を作成した場合は共通前提による相関した見落としを確認し、未解消ならboundedな独立reviewを行う。省略時は、早期監査または最終監査のどちらを省略したか、判断者、受入条件ごとの独立証拠分類、根拠、代替確認、未証明、残存リスクを記録し、第7節の明示分岐を通る。省略は監査PASSと同一ではなく、最終報告では `低リスク正式監査省略` として別に示す。

独立監査は各ゲートで新しい監査チームを作らず、作業全体で必要な最小coverageを配分する。T0で閉じない通常リスクは原則として異なる2つの非重複risk vectorを作業全体で確保し、早期と最終へ分けてよい。高リスクは原則3つの非重複vectorを作業全体で確保し、相関見落としがmaterialな場合だけT2としてreviewerまたは独立手段を分離する。追加監査は、未解決の証拠衝突または未coverageの重大riskを具体的に示せる場合だけ行う。低リスクで一部または全部を省略する場合はC0、T0、判断と代替確認を記録する。証拠同一の未変更範囲は再利用し、独立性を損なわない限り同じbounded auditorの差分再確認を許可する。監査者には他の監査者の結論を初回finding固定前に与えず、親はblocking findingを正本と照合する。親が到達可能性、受入違反または実害、変更起因性を確認できないfindingは修正を開始せず、非阻害または未証明として処理する。
