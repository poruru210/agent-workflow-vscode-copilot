### 検証能力・検出漏れゲート

ここでいう検証はunit・integration・回帰testだけでなく、parse、compile、schema、render、意味・互換性確認、package・runtime identity、GUI・実環境確認、外部操作のprecondition・post-verification、read-only判断の情報源・freshness・反証確認を含む。この節の `製品根因` はコード製品に限定せず、文書、設定、schema、package、判断、外部操作その他の成果・対象側でfailureを生んだ根因を意味する。作業種別に応じ、次の共通検証chainから適用部分だけを用いる。

```text
主目的・要求・受入条件
-> risk・failure model
-> 選択した検証mechanism・partition
-> fixture・入力・data・設定・environment
-> supported entryから対象のcontrol・data・state・consumer実経路
-> 外部観測可能なbehavioral oracle・assertion・判定基準
-> collection・report・CI・release・action gate
-> Go/No-Goまたは受入判定
```

state、event、identity、lifecycle、ordering、clock、observer、fixtureまたはoracleが検証結果へmaterialに影響する場合は、上記chainの意味境界を `VM-<id> verification-model subpacket` として固定する。これは新しいphaseではなく、新規実装・保守・移行では検証能力mapの一部、修正では該当するVER・TEST-RC・U0/U1・test planの共通入力である。該当mechanismがない場合だけ、肯定的根拠を持つ理由付き `該当なし` とする。

VMにはリスクに比例して次を含める。

- supportedなstate・event・lifecycleと、要求・risk・effect・oracleによる等価partition。全状態・全組合せを機械的に列挙しない。
- identityの生成、選択、継承、部分更新、rotation、別名・family、失効、およびoracleを過去に観測した固定IDではなく当該実行で選択された対象または外部不変条件へ束縛する規則。
- 正規event・request・result familyと、必須のhappens-before、許容されるpartial order・scheduler差・並行分岐。
- virtual、monotonic、wall-clockその他のclock domain、責任component、変換、boundary、timeout・周期・経過時間の判定規則。
- supported entryから責任component・consumerまでの実control・data・state経路、fixture・environment、および外部観測可能なbehavioral oracle。
- 診断・trace・state readがlock、schedule、state、latencyまたは結果を変えないためのatomic snapshot、読取回数、hot-path costその他のobserver-effect制約。
- assertion間の前提・状態依存、fail-fastで未実行になるdownstream assertion、hard barrier、独立partition、および安全に収集できるmasked assertionの関係。

新規実装では正常成功envelopeと設計からVMを前向きに作り、修正・保守・移行ではbaselineのVMを変更影響と検証適用性に照らして維持または更新する。単一の成功時系列、特定ticket・generation・request prefix、偶然のthread順序、例外なし、mock call、巨大scenario一回のPASSをsupportedな正常状態集合の代用にしない。

新規実装では、初回実装前の設計・実装準備ゲートで、各必須受入条件と合理的に到達可能な重大failureをこのchainへ前向きに対応付ける。初回実装前に存在しない検出漏れ根因を要求せず、実経路、oracle、必要なpartition、後段gateが設計上成立することを確認する。計画保守・移行では、既存証拠と検証chainの適用性、変更で失効するlink、新規・限定・影響経路・全面の検証範囲を変更準備ゲートで定める。文書、設定、schema、package、read-only判断、外部操作では、testという名称に拘らず上記の該当mechanismへ読み替える。

既存不具合、変更後FAIL、監査finding、package・runtime・実環境failureその他、期待された検証を通過して観測されたfailureでは、製品根因packetを固定した後・修正前challenge監査より前に、検出責任の有無を判定する。当時の要求、supported scope、risk、運用・release契約から検出責任があった場合は、製品根因とは別の `VER-<id> verification-escape packet` を固定し、期待chainと実際chainを前から比較して、検出能力が最初に失われた `earliest break` を特定する。testが存在しなかった、testがPASSした、または今回の症状を再現するcaseを追加した事実だけを検出漏れ根因にしない。

verification-escape packetには、リスクに比例して次を含める。

- failure・主目的・受入条件・製品根因ID、baseline・test plan・runner・CIまたは該当検証実行のidentity。
- 当時のsupported scope、要求・riskに基づく検出責任、および責任なしとする場合の肯定的根拠。
- 期待chainと、test source、selection、fixture、入力、設定、mock・stub、trace、oracle、report、CI・release gate等から再構成した実際chain。
- earliest break、責任component・層、下流の寄与要因、主要な代替escape原因の除外証拠。
- 同じearliest break、risk class、fixture、実経路、oracleまたはgateを共有するsupported scope内の到達可能なsibling範囲と、代表partitionまたは全件を選ぶ理由。
- 製品修正、test・fixture・runner・report・CIその他の検証系修正を分けた対策、修正後の感度確認方法、未証明と残存risk。

primary分類は、`REQ-RISK`（要求・riskからscenario未選択）、`SELECT`（partition・優先度・実行対象未選択）、`SETUP`（fixture・data・設定・時刻・environmentで前提不成立）、`PATH`（mock・stub・entrypoint差異で実経路未通過）、`ORACLE`（外部挙動の違反をFAIL化不能）、`REPORT-GATE`（collection・retry・quarantine・report解析・required check・release/action gateでFAIL消失）、`UNPROVEN`、`理由付きN/A` のいずれかとし、寄与要因を別記できる。`理由付きN/A` は新規要求、当時のsupported scope外、または検出責任なしを当時の正本から肯定的に示した場合だけ使用し、履歴・証拠不足は `UNPROVEN` とする。

検出能力の立証では、可能で安全なら隔離されたpre-fix baselineまたは同等artifactで新規・修正版検証がFAILし、fixed candidateでPASSすることを示す。pre-fix実行が危険、不許可、破壊的、非再現または外部依存で困難な場合は、controlled fault、既存trace・履歴、静的因果、複数の独立代替証拠を用い、限界を記録する。修正着手前の動的確認は第10節の軽量diagnostic-probe条件を満たす場合だけ行い、永続test source、candidate、外部状態を変更しない。

検証はprivate branch、例外文、内部call回数、mock呼出し、`例外なし` またはstatusだけへ密結合させず、要求由来の外部観測可能なbehavioral oracleを用いる。mock・stubは境界を制御するために使えるが、リスクに比例して少なくとも一つは対象責任componentとsupported entryからの実control・data・state経路を通る証拠を持つ。controlled faultやmutationはtest感度の証拠であり、製品correctness、coverage数値、主目的PASSの代用にしない。

製品根因とverification-escape根因に対応する永続変更は、修正着手ゲート通過後に同じcorrection batch内で責任境界別に実装し、共通snapshot・早期監査・分割検証へ渡す。すべての想定caseを無制限に追加せず、同じearliest breakを共有し現在の主目的・受入・supported scopeへ到達可能なsiblingだけを対象にし、等価partitionは代表caseでよい。因果のない一般的テスト改善、将来最適化、coverage数値だけを上げる変更は第4節の新規発見・主目的逸脱ゲートで別作業候補または却下とする。

verification-escape packetは新しい独立監査phaseではなく根因challenge監査の入力である。第4節のT0/T1/T2とD・E・R等のrisk vectorで、決定的に閉じる命題はtoolで閉じ、意味・実経路・検出責任・oracleにmaterialな不確実性が残る場合だけboundedな独立reviewを行い、高実害・複数責任層・証拠衝突・相関見落としがある場合だけ観点を分離する。subagent数をquotaにせず、既存の根因challenge jobへ非重複観点として統合できる場合は一つのjobで扱う。

packet状態は `Confirmed`、`理由付きN/A`、`UNPROVEN` とする。`UNPROVEN` は分析状態であって検出漏れ解消PASSではないが、それだけで製品修正を自動停止しない。再発防止・検出能力が固定した必須受入条件である、または検出前に回復不能な高実害が生じ得る場合は必要証拠までrelease・対象操作をNo-Goとし、それ以外は製品修正を進めても検出漏れ改善を主張せず、残存risk、追加証拠経路、別作業候補を明記する。
