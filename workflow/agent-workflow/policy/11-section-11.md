## 11. 実装方針

新規実装の初回実装は、設計・実装準備ゲートで確定した要求、設計、受入条件、planned semantic delta、preservation contract、INTの設計linkと影響境界に対応する範囲に限定する。計画保守・移行は、変更準備ゲートで確定した変更目的、planned semantic delta、preservation contract、INT、互換性境界、移行・rollback計画、受入条件に対応する範囲に限定する。不具合、テストFAIL、監査findingへの修正実装は、二鍵で確定した製品根因、該当するverification-escape根因、INTで固定した介入link・共有mechanism・preservation・新規failure仮説、CHG packetで閉じる変更誘発failure、および受入条件に対応する範囲に限定する。

- 関係のないリファクタリングを行わない。
- 既存APIや挙動を不用意に変更しない。
- 通常の対応条件から主目的の最終成果まで到達する経路を実装し、既定設定、通常入力、通常状態で到達可能にする。
- 通常条件でも即時returnする、主機能を恒常的にdisable・HOLD・skip・rejectする、空結果やstatusだけを成功として返す、到達不能条件の内側に主処理を置く、stub・placeholder・no-opを完成扱いする実装を行わない。ただし、その挙動自体が固定した主目的または明示受入条件である場合を除く。
- early return、disable、HOLD、skip、reject、fallback、fail-closed、timeout、feature flagには、遮断条件、要求または実害との対応、通常条件で主目的を遮断しない証拠、reason code、再開・復旧方法を持たせる。
- 停止作用を新設・変更する場合はCONT subpacketに従い、個々のguardだけでなく合成順序、支配・dead guard、正常成功envelope、`NewlyStopped`、回復livenessを設計・実装する。固有の防止・診断・回復価値がなく、上位cutで常に作用を失うguardを条件分岐として積み増さない。
- 「例外がない」「processが継続した」「安全に終了した」と「主目的を達成した」を区別する。
- findingごとの局所修正ではなく、RCで二鍵確認した根本原因の責任層とINTで固定した因果linkを修正する。症状消失だけを狙う別linkへの条件追加、例外処理または停止追加へ置換しない。
- ログ、telemetry、health check、非blocking assertionその他の診断性変更も実装変更として扱い、適用する作業種別ゲート、共通修正回数台帳、実装snapshot、早期監査要否ゲート、テスト、テスト対象同一性ゲート、release candidate、最終監査要否ゲートを通す。fail-closedその他の停止作用は診断性変更へ含めず、防止・封じ込め変更としてCONT subpacketを通す。
- 修正前後の差分を明確にする。
- planned semantic deltaとactual semantic deltaの不一致、保存契約外への作用、impact coneの拡大を隠さず、新しい要求、実装不足、意図外変更または未証明としてゲートへ戻す。
- 既存変更と今回の変更を区別する。
- 「以前から存在した問題」を安全性の根拠にしない。

実装中に別の重大問題を発見した場合は、勝手にスコープを拡大せず、影響と依存関係を親へ報告して再計画する。
