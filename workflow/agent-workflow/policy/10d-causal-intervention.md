### 因果介入・修正影響subpacket

candidate-bearingな変更では、実装前に `INT-<id> causal-intervention and impact subpacket` を固定する。これは新しいphaseまたは監査回数ではなく、根因・設計判断をplanned semantic delta、CHG、U0/U1、action manifestへ接続する設計入力である。不具合修正ではPASSした `RC-<id>` を参照し、新規実装・計画保守・移行では要求・設計・変更目的を起点に同じ項目を前向きに記録する。純read-onlyでは理由付き `該当なし` にできる。

INTにはリスクに比例して次を含める。

- 切断、変更または新設する因果・設計linkとsemantic property、およびなぜ主目的または元failureを解決すると予測するか。
- そのpropertyを共有するmechanism、upstream・downstream、到達可能なsibling・consumer・state owner、および肯定的な非影響境界。
- 正常成功envelope、preservation contract、状態・副作用・所有権・順序・性能・資源・診断・recoveryで変えてはならないもの。
- 介入が誤り、過剰または不足なら観測されるcounterfactual prediction。
- 変更によって新たに生じ得るfailure hypothesis、その成立条件、実害、既存guard・invariant、診断、containment・rollback・recovery、および必要なbehavioral・preservation oracle。
- root cause、shared mechanism、consumer、state、performance、diagnostics、recoveryの各観点について、適用内容、独立根拠を持つ理由付き該当なし、または未証明。

INTは「なぜ、どのlinkへ介入し、どの作用を予測するか」に限定し、CHGは固定snapshotから「実際に何が変わったか」を独立導出する。実装後にINTを書き換えてactual deltaへ合わせず、不一致は要求変更、設計・実装不足、意図外変更、予測漏れまたは未証明として処分する。修正では根因challengeと不一致処分の完了後、planned correction deltaとU0を確定する前にINTを固定する。新規実装・保守・移行では設計・変更準備内で固定し、外部writeではaction manifestのplanned effect・anticipated impactへ接続してpost-actionのactual effectと照合する。

INTの準備完了には、変更link、共有mechanism、正常成功・preservation、到達可能でmaterialな新規failure、diagnostics・recovery、および後段で反証するU0 oracleが明示されていることを要する。全組合せや全consumerの無制限列挙は要求せず、同一mechanism・state・effect・oracleの等価partitionは代表化する。T0では新しいreviewを増やさず、T1では根因challengeと介入影響を一つのbounded jobへ統合し、T2は未解消vectorだけを分離する。
