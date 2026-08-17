## 17. 完了判定と最終報告

次の証拠層を分離して判定する。

- 主目的ID、正常成功経路、禁止代替結果、および `目的達成PASS`・`FAIL`・`未証明`
- 主要な正常経路と重大failure境界の `診断可能性PASS`・`FAIL`・`未証明`・`該当なし`
- リスク分類、判定根拠、およびversion付きwork-definition manifestの同一性
- 実行割当と検証割当を分けた判断、`C0`、成果鍵・独立反証鍵、T0/T1/T2、および必須命題ごとのrisk vector・独立証拠分類
- 変更前baseline、version付きsupplement、および証拠manifestの完全性
- 外部状態変更がある場合のaction-readiness、pre-action auditの `PASS`・`修正要`・`未証明` または低リスク省略、実行直前identity/freshness、元操作結果、post-action verification、post-action snapshot
- containment・rollback・compensationがある場合のtrigger・承認・実行単位、recovery結果、post-recovery verification、post-recovery snapshot。recovery PASSは元操作結果および受入PASSと分離する
- 原因特定完了。修正ではraw evidence dossierとprovisional causal ledgerの分離、T0またはblind-first T1/T2、親・監査者の不一致処分を含む
- 新規・保守では適用する検証能力設計、修正では検出責任、verification-escape packetの `Confirmed`・`理由付きN/A`・`UNPROVEN`、および必須時の解消証拠
- 該当するVM・TEST-RCのidentity・状態、supported partition・identity lifecycle・event family・ordering・clock・observer・oracle・assertion dependency、同根因sibling、継続・退出・代替証拠・保留claim、および再入場条件
- candidate-bearing変更ではINT subpacketの介入link・共有mechanism・consumer・counterfactual・preservation・新規failure予測とU0 mapping、およびCHG packet、planned/actual semantic delta、preservation contract、impact cone・cut proof、予測内外の変更誘発failure仮説の閉包、後段証拠と残存risk。純read-onlyでは変更安全閉包だけの理由付き `該当なし`
- 停止作用へ該当する変更ではCONT subpacket、正常成功envelope、`NewlyStopped`、guardのactivation/effect reachability・合成・支配・固有役割、回復liveness。非該当では理由付き `該当なし`
- candidate-bearing変更では `U0`・`U1` のidentityと追加履歴、test-intervention ledger、未実行・quarantine・candidate汚染、impact branchの処分
- 実装完了と実装snapshot識別情報
- 実装構造監査PASSとテスト準備構造screen PASS、または条件を満たした低リスク正式監査省略
- 後段証拠状態とテスト移行可否。該当早期scope未証明の条件付き移行を使った場合は同一snapshot・test-plan identityへの限定再判定PASS
- 分割テストPASS
- 全体回帰テストPASS
- テスト対象同一性PASSとcandidate-bearing identity
- release candidate識別情報
- package PASS
- 実環境PASS
- 最終独立監査PASS、または条件を満たした低リスク正式監査省略

新規実装・保守・移行では、work-definitionで適用するとした検証能力chainが早期screenと必要な後段証拠で閉じていることを完了条件とする。修正では検出責任を判定し、verification-escape packetを `Confirmed`、`理由付きN/A` または `UNPROVEN` へ分類する。再発防止・検出能力が必須受入条件または高実害の防止条件なら、`Confirmed` または肯定的な `理由付きN/A` に加え、該当時はearliest breakの解消と感度証拠を完了条件とする。それ以外の `UNPROVEN` はPASSへ昇格させず、第10節と第15節に従い、製品修正の完了可否、理由付き残存risk、追加証拠、別作業候補を個別判断し、検出漏れ改善または再発防止PASSを主張しない。

candidate-bearing変更では作業種別を問わず、INTの介入・影響予測、planned/actual semantic delta inventory、preservation contract、双方向impact coneと局所cut proof、到達可能でmaterialな予測内外の変更誘発failure仮説が、第4節の汎用T0、完了・finding処分済みT1/T2を含む複合証拠、または独立根拠を持つ理由付き該当なしへ解決され、必要な後段証拠と最終監査の整合が確認されたことを完了条件とする。修正ではRCのraw evidenceと親ledgerを分離し、厳格なT0またはblind-first T1/T2で根因二鍵と不一致処分が閉じていることも要する。停止作用へ該当する場合は、CONT subpacketの正常成功envelope、`NewlyStopped`、停止合成、支配・dead guard処分、回復livenessも同じ閉包へ含める。`U0` から `U1` への追加履歴、test intervention、未実行・quarantine、candidate汚染、materialなorphan branchを処分し、恣意的なcase・oracle選択でPASSを作っていないことを別命題として確認する。これは主目的の成果鍵とは別命題であり、原要求の達成、元不具合の解消、テストPASSまたは全体回帰PASSだけで代用しない。純read-only作業はこの変更安全閉包だけを理由付き `該当なし` にできる。

検証系修正を退出した場合は、退出分類、未証明・保留したclaim、代替証拠、依存しない次作業、対象操作・release・完了への影響、および再入場条件を完了判定へ含める。`RETIRE-INVALID` は代替証拠で依存mandatory claimが閉じた範囲だけ完了可能とし、`DEFER-NONMANDATORY` は当該改善を現在taskの必須条件へ昇格させない。`PROCEED-INDEPENDENT` は保留claimに依存しない範囲だけ進め、`RELEASE-NO-GO / WORK-CONTINUE` はreleaseを禁止しても作業全体を完了No-Goにしない。退出、回数、予算到達をPASSまたは完了の代用にしない。

事前に定義したすべての主目的の正常成功経路と最低必須成果が `目的達成PASS`、必須受入条件がすべてPASS、適用対象の診断可能性がPASSまたは理由付き `該当なし`、実装構造監査とテスト準備構造screenがPASSまたは適正に省略され、検証範囲・証拠適用性ゲートで受入必須の全項目が有効な現candidate証拠、直接適用証拠、または立証済み証拠ブリッジへ解決され、受入必須の後段証拠とテスト対象同一性がPASSし、合理的に到達可能な修正必須findingが残らない場合のみ、「修正済み」「完了」「安全」と判断する。主処理なしの正常終了、空結果、statusだけの成功、恒常的disable・HOLD・skip、例外なし、process継続、テストPASSを目的達成の代用にしない。外部状態変更では、pre-action auditがPASSまたは適正に省略され、実行直前identity/freshness gate、post-action verification、および必要なpost-recovery verificationがPASSしても、それぞれを元操作結果や受入条件PASSの代用にせず、元操作と回復を別々に判定する。該当早期scope未証明の条件付き移行を使った場合は、同一snapshot・test-plan identityへの読み取り専用限定再判定PASSも必須とする。例外は、満たさない受入条件、理由、影響、期限または適用範囲、残存リスクを示してユーザーが明示的に承認した場合に限る。エージェント自身のリスク受容、監査省略、条件付きテスト移行、後段テストPASS、correction batch回数、時間・token・tool予算到達だけを目的・受入条件PASSまたは完了No-Goの代用にしない。`未証明` はPASSへ昇格させず、第15節の基準で対象操作No-Go、release No-Go、理由付き残存リスク、再計画、ユーザー判断待ち、または第4節の限定条件を満たす完了No-Goを区別する。

完了には、第4節の `成果鍵` と `独立反証鍵` の両方を必要とする。`C0`、適用される変更安全閉包と全必須命題がT0、完了・処分済みのT1/T2を含む複合証拠、または独立根拠を持つ理由付き該当なしへ解決され、必要なrisk vector coverageが閉じていることを完了条件とする。独立性が必要な命題、受入集合の完全性、変更安全性、または適用risk vectorが未証明のままなら、親が直接実行したこと、簡単な作業であること、短時間で終わったことを理由に完了へ昇格させない。

最終報告には、次のうち適用される項目と判断に必要な差分・状態・証拠参照を簡潔に含める。既存packetや不変な証拠本文を再掲せず、ID、version、hashまたは参照位置で結び付ける。

- リスク区分、各判定軸、採用理由、引下げ時の肯定的証拠
- 有効なwork-definition manifestのversion・hash、変更履歴、要求・受入・権限・比較baseline・監査範囲のidentity
- 元baselineとversion付きsupplementの境界、証拠manifest、完全性、後から取得した証拠の影響範囲
- 当初の時間予測range・確度・critical path、主要checkpoint、実績との差異、再見積りと効率判断
- 複数主目的がある場合のobjective ledger、依存順、active objective、context再入場時の再開点
- materialな新規発見とactive scopeへの採用候補について、`必須同一scope`・`効率化enabler`・`別作業候補`・`却下`、因果・cost・採否・元目的への復帰条件。明白な別件・却下は集約した一行記録でよい
- 委譲機会checkpointの判断、利用したsubagent job lease、invocation完了・追加attempt・retire・新規jobのterminal記録、要求したmodel・reasoning、`orchestrator受理済み`・effective metadata・設定未証明の別、および選定根拠。正常受理された通常turnについて子の自己照会不能を反復報告せず、拒否・downgrade・不一致・override無視・設定未証明だけを例外として示す
- 実行割当と検証割当を別々に選んだ根拠、`C0`、成果鍵・独立反証鍵、T0/T1/T2、担当risk vector・blind-first結果、および必須命題ごとの `決定的独立証拠`・`独立review必要`・`複合証拠`・`未証明`・`理由付き該当なし` の分類と解消結果
- 受入条件ごとの `PASS`、`FAIL`、`未証明`
- 主目的IDごとの正常成功経路、最低必須成果、禁止代替結果、および `目的達成PASS`・`FAIL`・`未証明`
- 診断可能性の適用範囲、first fault、reason code、因果再構成証拠、および `PASS`・`FAIL`・`未証明`・`該当なし`
- RC packetのraw evidence dossierとprovisional causal ledger、原因特定の内容と確度、T0またはblind-first challengeの独立導出、親・監査者の不一致と処分、修正前後の反証可能な予測
- 検証能力mapまたはverification-escape packet、検出責任、期待chainと実際chain、earliest break、分類、sibling範囲、感度証拠、対策、状態、未証明と残存risk
- VM・TEST-RCのidentity・分類・失効claim、supported state・identity・event・ordering・clock・observer・oracle・assertion dependency、同根因sibling、修正予測、継続・退出の価値判断、退出分類、代替証拠、保留範囲、次作業、再入場条件
- INT subpacketの介入link、共有mechanism・consumer、counterfactual・preservation・新規failure予測、U0 mapping、およびCHG packet、planned/actual semantic delta、impact cone・cut proof、予測との不一致、作者とblind-first監査が導出した変更誘発failure仮説、T0/T1/T2、後段partition・behavioral oracle・証拠、処分と残存risk
- CONT subpacket、baseline/candidate正常成功envelope、`NewlyStopped`、guard inventory・activation/effect reachability・合成順序・支配・固有役割、全guard有効時の正常経路、回復liveness、availability・throughput・資源への作用、処分と残存risk
- `U0`・`U1` のversion・hash・追加履歴、事前固定した選択規則・seed、test-intervention ledger、未実行・quarantine・candidateまたは共有state汚染、impact branchごとの処分と残存risk
- 今回変更した範囲と変更していない範囲
- 実装snapshotとrelease candidateそれぞれの識別情報、hash、差分、環境
- mechanical preflightの実施または省略理由、結果、snapshot同一性
- 実装構造監査、テスト準備構造screen、後段証拠状態、テスト移行可否の各フィールドと、条件付き移行時の完了判定保留・release candidate固定不可および解消証拠
- 早期監査の各系統の結果、再利用した証拠、再監査・再screenした差分、test-plan supplement、該当早期scope未証明の例外を使った場合の同一snapshot・test-plan identity確認と限定再判定
- Evidence Dependency Mapのversion・hash、R0～R3分類、継承・失効・追加claim、review key、監査・検証再入場の新情報・判断変更見込み・主目的への寄与、および重複を止めた処分
- 検証範囲・証拠適用性ゲートの分類、選択した検証level、cost判断、証拠ブリッジのID・freshness・非影響根拠・現candidateの限定検証・拡大条件・残存risk
- 低リスクで正式監査を省略した場合の条件別証拠と代替確認
- 実行したテスト区分、未実行・阻害テスト、全体回帰テストの結果
- テスト対象同一性ゲートのcandidate-bearing manifest、証拠metadata・隔離一時状態との境界、比較項目、差分、復元証拠、判定
- package、GUI、runtime、実環境の結果
- 外部状態変更がある場合のtarget/account/tenant/environment/resource、action manifest、権限・明示確認、pre-action auditの三分岐結果または省略根拠、実行直前に再取得したstate/version/etag/hash・依存状態・approval identity・guard/CASと照合結果、実行回数、外部送信・通知・副作用、post-action verification・snapshot
- failure・部分成功がある場合の最小保存証拠、緊急containmentの先行要件、rollback・compensation・有限段階recoveryごとのtrigger・target・input・最大回数・結果、post-recovery verification・snapshot、共通台帳outcome、再試行の有無、元操作結果とrecovery結果の分離判定
- 最終監査の各系統の結果
- findingごとの共通必須フィールド、分類、到達可能性、成立条件、強制guard・invariant、変更起因性、実害、診断性、検出・封じ込め・復旧可能性、および共通マトリクスによる判定
- 共通修正回数台帳と根本原因・必須failure単位の収束状況
- correction batchごとの目的達成状態・受入条件差分・新しい因果証拠・回帰・累積cost、および目的進捗・収束性ゲートの判定
- 全体再監査率、有効証拠再利用、同一review key重複、一必須命題を閉じる時間・tokenについて、取得costが判断価値を上回らない範囲の実績
- 現在の実行状態が、作業継続、再計画、ユーザー判断待ち、技術的阻害、対象操作No-Go、release No-Go、完了No-Goのいずれかと、その根拠
- ユーザー承認済み受入条件例外がある場合はその正確な範囲
- 残存リスク
- Go/No-Go
- 証拠の種類と限界

推測、メモリ由来、ソース確認、早期監査確認、テスト確認、package確認、実環境確認、最終監査確認を区別する。未検証の証拠層をPASSとして扱わず、No-Go基準に該当する未証明が残る場合は曖昧な完了表現を避ける。
