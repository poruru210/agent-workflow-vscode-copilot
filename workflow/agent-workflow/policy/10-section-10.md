## 10. 根本原因と修正着手ゲート

根本原因ゲートは、既存不具合の修正、mechanical preflightまたは変更後テストのFAIL、監査findingの修正、診断性変更、および新規実装、計画保守・移行その他の変更後に発見した必須failureへのゲートである。新規実装の初回着手には適用せず、要求、設計、対象境界、受入条件、検証方法、失敗時の安全策が揃ったことを設計・実装準備ゲートとする。計画保守・移行の初回着手には変更準備ゲートを適用するが、その後にFAILが発生した場合は根本原因ゲートを省略しない。

エラーメッセージや失敗箇所を確認しただけでは修正へ移らない。症状は、安全かつ許可範囲で再現可能なら再現する。再現が不能、危険、破壊的、または実環境で許可されない場合は、静的な制御・データフロー、incident記録、failure invariant、ログ・telemetry、状態遷移、artifact差分など複数の独立証拠で因果を確認し、未再現の理由と判断限界を記録する。合理的に特定可能な範囲で、次を満たした時点を修正着手ゲートとする。

- 症状の再現証拠、または再現不能・危険時の複数の独立した代替証拠により、障害の存在と因果を確認できる。
- 直接原因と責任を持つコンポーネントまたは層を特定できる。
- 入力から障害までの因果経路を説明できる。
- 主要な代替原因を証拠で除外できる。
- 同じ原因が生む別症状と影響範囲を把握できる。
- 修正によって問題が解消する理由を説明できる。
- 修正後の受入条件と確認方法を事前に定義できる。

十分に特定できない場合は、確認済み事実と原因仮説を分け、追加ログ、計測、最小再現、状態確認、制御・データフロー追跡を行う。推測だけで修正しない。

タイムアウト延長、例外の握り潰し、再試行回数の増加、条件分岐の継ぎ足しだけで症状を隠さない。

### Detailed sub-sections

Read the following files **in order** before continuing to Section 11. Together they are Section 10 and are all mandatory when applicable.

- [根因因果証拠packet・修正前challengeゲート](10a-root-cause-challenge.md)
- [検証能力・検出漏れゲート](10b-verification-escape.md)
- [検証系根因・検証モデル修正ゲート](10c-test-system-root-cause.md)
- [因果介入・修正影響subpacket](10d-causal-intervention.md)
- [変更誘発故障・保存契約ゲート](10e-change-safety.md)
- [正常継続性・停止合成subpacket](10f-continuity.md)
- [診断可能性ゲート](10g-diagnosability.md)
- [共通修正回数台帳ゲート](10h-correction-ledger.md)
- [テスト修正継続・退出・作業再配分ゲート](10i-test-exit.md)
- [監査・検証往復収束ゲート](10j-audit-convergence.md)
- [目的進捗・収束性ゲート](10k-objective-convergence.md)
