### 根因因果証拠packet・修正前challengeゲート

既存不具合、変更後FAIL、監査finding、package・runtime・実環境failureその他の修正前に、リスクと再現性に比例した `RC-<id> root-cause packet` を固定する。packetは、観測と解釈を混ぜない次の二層で構成する。

1. `Raw evidence dossier`: primary symptom、主目的・受入条件・failure ID、source・artifact・environment・version・input・state・取得時刻・取得方法・hashまたは再取得ID、未加工log・trace・state transition・実行記録、再現の陽性・陰性結果と取得範囲、欠落・破損・観測汚染・再現不能理由を記録する。ここには観測された事実と出典位置だけを置き、原因、責任、相関、修正案を事実として書かない。
2. `Provisional causal ledger`: 親がraw dossierから導出した最終正常状態からfirst fault、後続failure、最終結果までの因果link、直接原因候補、責任component・層、寄与条件、共有mechanismとsibling symptom候補、影響対象・非影響対象、主要代替原因、反証可能なpre-fix予測、確度と未証明を記録する。修正案と修正影響は混ぜず、後段の `INT` subpacketへ分離する。

一つの例外、最後に出たerror、失敗行、同じ原資料から派生した複数の言い換え、親または監査者の権威、投票、patch案のもっともらしさだけでpacketをPASSにしない。根因challengeをT0で正式省略できるのは、次をすべて肯定的に立証した場合だけとする。

- 低リスク、局所、同期的で、外部依存、並行性、共有state、複数責任層がない。
- raw evidenceのartifact・version・environment・input・stateと取得境界が固定されている。
- 同一の最小再現で、制御した原因入力または状態に応じてfailureの出現、消失、復帰が決定的に観測される。
- 責任componentと故障linkが機械的に一意で、主要代替原因がcontrolまたはinvariantにより論理的に排除される。
- 修正効果とpreservation behaviorを、親の意味判断に依存しない独立oracleで判定できる。
- 第4節のC0、対象identity、side effect、到達可能性、否定命題を含むT0条件をすべて満たす。

差分が小さい、短時間、親が直接作業する、再現caseが一つPASSしたという理由ではT0にしない。consumer影響、意味解釈、代替原因、非同期・共有mechanism、外部状態、複数責任層のいずれかにmaterialな判断が残ればT1とし、高実害、証拠衝突、相関blind spotまたは複数の独立責任層で一つのreviewでは未解消なvectorだけをT2へ分離する。

T1/T2の読み取り専用根因challenge監査では、初回finding固定前に、監査者へ元要求・受入条件・正本、比較baseline、固定artifact・environment identity、許可scope、raw evidence dossierだけを渡す。raw dossierに含まれる未加工のtest実行記録・時系列・取得範囲は除外せず、親による選択・相関・因果解釈、provisional causal ledger、修正・patch案、合否結論、他reviewerの結論を先渡ししない。監査者は独立に、first fault、責任component・層、必要な因果linkと寄与条件、主要代替原因と反証予測、共有mechanismと到達可能なsibling、影響・非影響範囲、変更すべき因果link、およびその介入が新たに壊し得る経路を固定する。その後に親ledger、該当するverification-escape packet、診断可能性判定と照合する。

親と監査者の不一致は、次のように処分する。raw事実またはidentityの不一致は正本を再取得して取得境界・汚染を確定する。first fault、責任層、因果linkの不一致は、競合仮説ごとに異なる観測予測を作り、最小で安全な識別証拠により反証する。代替原因は成立条件、到達経路、除外証拠をledgerへ残す。修正影響の不一致は後段 `INT`、`U0`、早期監査へ両仮説を渡す。識別できなければ `最有力だが未確定` または `未証明` のままにし、挙動patchを因果確認実験として開始しない。不一致自体を自動No-Goにせず、必須受入、到達可能性、実害、回復可能性で限定的に判定する。

根因状態は `確認済み`、`最有力だが未確定`、`未証明` を区別する。`確認済み` はraw identity、因果chain、責任層、主要代替原因、反証可能な予測が整合し、T0または完了・finding処分済みのblind-first T1/T2で二鍵が閉じた状態である。`最有力だが未確定` は代替原因をmaterialに縮小したが重要な因果証拠が残る状態、`未証明` は責任層または因果を決める証拠が不足する状態である。後二者では、安全でboundedな診断性変更、追加証拠取得、sandboxのcausal probe、再計画、正確な阻害または限定No-Goへ進む。

根因challenge監査は実装後の早期監査ではなく、診断完了後・修正開始前のphase gateである。必須と判定した場合は第6節のjob lease・待機ゲートを通し、terminalな結果と不一致処分を待たずに修正へ進まない。結果は、製品根因packetを `PASS`、`追加診断要`、`未証明` で、該当するverification-escape packetを `Confirmed`、`理由付きN/A`、`UNPROVEN` で別々に判定する。製品根因packetのPASSだけを製品側の修正着手ゲートへ渡す。verification-escapeの `UNPROVEN` は後段の必須受入・実害条件で別判定し、それだけで製品修正を自動停止せず、検出漏れ改善PASSにも昇格させない。
