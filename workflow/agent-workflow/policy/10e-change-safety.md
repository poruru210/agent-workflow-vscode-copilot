### 変更誘発故障・保存契約ゲート

このゲートは、コード、文書、設定、schema、build・package、生成物、GUI、外部操作その他のcandidate-bearingな変更が、主目的を達成する一方で新しいエンバグ、デグレ、既存機能・契約破壊を生じさせないことを反証する。製品根因とverification-escapeの解消だけではこの命題を閉じない。新しい監査phaseを設けず、新規実装・修正・保守移行の準備、実装snapshot、既存の早期監査二出力、分割検証、release candidate、最終監査へ同じ記録を通す。純read-onlyで対象・artifact・外部状態を変更しない作業は、このゲートだけを理由付き `該当なし` にできる。

変更前に、`planned semantic delta` と `preservation contract` をwork-definitionへ固定する。planned deltaは、通常入口、利用者またはconsumer、外部観測可能な旧状態から新状態への差、許可する状態変化・副作用・通知・永続化を記述し、ファイル名やpatch方法だけで表さない。preservation contractはplanned deltaの外側で維持するsupported scopeの正常経路、consumer契約、API・CLI・設定・schema・保存形式、状態・所有権・lifecycle、互換性、性能・資源、診断・復旧、package・runtime・GUI・外部境界をリスク比例で選ぶ。新規実装では新機能外、修正では原不具合外、保守・移行では互換性・rollbackを含む変更目的外を保存対象とし、正当な主目的変更を回帰として禁止しない。

リスクに比例した `CHG-<id> change-safety packet` を、既存manifest、根因packet、verification-escape packet、INT subpacket、action manifestへ関連付ける。packetには少なくとも次を含める。

- baseline・candidateまたはtarget identity、主目的・受入条件・根因ID・INT ID、およびplanned semantic deltaとpreservation contract。
- 固定snapshotのdiffから独立に導出できる範囲の `actual semantic delta`、planned deltaとの一致・欠落・意図外差分、および動的証拠なしでは確定できない `未証明`。
- INTが予測した介入link・共有mechanism・consumer・変更誘発failureとactual delta・impact coneの一致、不足、過剰、予測外作用。
- changed nodeから上流のentry・precondition・caller・state ownerと、下流のconsumer・return・exception・side effect・persistence・compatibility・diagnostics・recoveryへの双方向 `impact cone`。
- coneの各branchを止める安定contract boundary、実経路で強制されるguard・invariant、または非到達の肯定的な `cut proof`。cut proofは特定contract・branch・仮説だけを閉じ、未知の全経路を一括して非該当にしない。
- actual deltaとpreservation contractから導出した変更誘発failure hypothesis、その成立条件、supported実経路、観測違反、実害、guard・invariant、診断性、および反証証拠。
- 各仮説の `T0 決定的閉包`、完了・finding処分済みの `T1/T2`、独立根拠を持つ `理由付き該当なし`、または `未証明`、後段partition・behavioral oracle・拡大条件・残存risk。

actual semantic deltaは早期監査時点で静的・構造的に導出できる範囲に限定し、動的挙動、統合、性能、package、runtime、GUI、実環境でしか確定できない部分を推測でPASSにしない。これらは後段証拠状態へ `未証明` として送り、早期scopeの静的判定と混同しない。planned deltaとactual deltaの不一致を、後からplanned deltaを書き換えて消さず、要求変更、実装不足、意図外変更または未証明として処分する。

変更誘発failureは、少なくとも `新たに到達または非到達になった経路`、`値・型・schema・順序・時刻・所有権の変化`、`side effectの追加・消失・重複とidempotency`、`state・lifecycle・persistence`、`retry・timeout・並行性`、`resource・performance`、`permission・target`、`observability・diagnosability`、`build・package・runtime・consumer互換性` から、actual deltaへ因果接続するfamilyだけを用いて導出する。全familyを機械的に埋めず、適用しないfamilyは理由付き `該当なし` とする。仮説をactive scopeへ入れるのは、次のすべてを満たす場合だけとする。

```text
changed semantic propertyと因果接続
AND supported scopeの実経路または状態遷移から到達可能
AND preservation contract・必須受入・material harmのいずれかに違反し得る
```

早期独立監査では、監査者が作者のPASS判定、修正理由、test plan、既存仮説を不必要に先に受け取らず、元要求・baseline・固定actual diff・supported contractからblind-firstでplanned/actual delta、impact cone、保存契約違反、変更誘発failureを独自導出して初回findingを固定する。その後に作者のCHG packet、設計意図、verification-escape、test planと照合する。後段検証は、作者と監査者が導出した仮説の和集合のうち未閉包で適用対象のものから必要最小のpartition、supported実経路、behavioral oracleを選び、既存テストやpatchのprivate branchから仮説集合を逆算しない。

変更安全閉包には第4節のT0/T1/T2をそのまま用いる。semantic-neutralな変更をinline T0で閉じられるのは、変更対象、比較基準、side effect、意味的非影響、artifact・environment identityが決定的に閉じ、人間的なconsumer・到達可能性・否定命題判断が残らない場合だけとし、小差分、文言だけ、簡単というラベルを根拠にしない。通常のsemantic changeは既存T1 jobの非重複観点として統合し、高実害、複数責任層、外部write、証拠衝突または相関見落としがmaterialな場合だけ未解消vectorをT2へ分離する。変更安全観点を統合しても既存のR・F・C・E・D・O coverageを置換せず、subagent数をquotaにしない。

impact cone外、planned/actual deltaと因果のない一般改善、将来最適化、coverage件数だけを増やす仮説、同じmechanism・oracleを持つ等価caseの無制限列挙は第4節の主目的逸脱ゲートで別作業候補または却下とする。同一snapshot・packet・証拠を再監査せず、candidate、identity、planned/actual delta、契約、仮説、証拠または拡大条件が変わった影響差分だけを再確認する。全面回帰のcostと、impact mapping・限定検証・誤継承時実害のrisk調整後総costを比較し、安価で必要十分な方を選ぶ。

外部writeでは、実行前にaction manifestのplanned effect delta、target、許可side effect、preservation contract、anticipated impact coneを閉じ、実際のexternal semantic deltaはpost-action verificationとpost-action snapshotで確定する。実行前に未発生のactual effectをPASSにせず、実行後にplanned effectとの不一致、誤target、重複・欠落side effect、preservation contract違反を別結果として判定する。

変更安全閉包の完了には、planned/actual semantic delta inventory、preservation contract、impact coneと局所cut proof、および到達可能でmaterialな変更誘発failureが、T0、完了・finding処分済みT1/T2を含む複合証拠、または独立根拠を持つ理由付き該当なしへ解決され、成果鍵も別にPASSしていることを要する。`findingなし`、作者のself-review、元症状の解消、テストPASS、全体回帰PASSだけでは閉包しない。到達可能でmaterialな未解消仮説は対象操作またはreleaseをNo-Goとし、非material、肯定的に遮断・対応外、または必須条件でない未証明は第15節の到達可能性・実害・診断性で個別判断する。
