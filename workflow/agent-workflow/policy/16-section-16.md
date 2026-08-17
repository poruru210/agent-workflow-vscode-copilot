## 16. 監査findingの診断、修正、再監査

監査でfindingがある場合は、固定snapshotへの監査を最後まで完了し、全findingを統合して第15節のゲートを終え、監査フェーズを正式に終了してから診断または修正フェーズへ移る。実装と監査を同時進行せず、監査中に一件ずつ修正しない。

- findingを根本原因と実害単位で統合し、同じ原因から生じるfindingを一括して扱う。
- baseline、実装snapshot、release candidateを比較し、変更起因、既存問題、診断性不足、潜在リスク、実害なし、未証明を区別する。
- `到達可能な修正必須` と、変更が必要と判断した `診断性不足` を修正対象にし、`既存の別問題/対応外` を含むそれ以外は理由と残存リスクを記録する。既存の別問題を修正する必要がある場合は、ユーザー権限と受入条件を確認して別作業として再計画する。
- 独立して安全な残りの診断・テスト区分を実行し、因果経路と影響範囲を特定する。
- 製品根因、該当するverification-escape根因、既存CHG packet上の変更誘発failureとpreservation contract違反、該当するCONT subpacket上の正常継続性・停止合成failure、修正後の確認方法を確定し、第10節の根因challenge・不一致処分、修正着手ゲート、共通修正回数台帳ゲートを通過する。
- 修正実装前に、新しいversionのINT、planned semantic delta、preservation contract、およびRC・INTから導出した `U0` を固定する。元のU0とoracleを履歴から消さず、正本要求またはoracle自体の誤りを修正する場合だけwork-definition更新・test-intervention処分・独立screenを通す。
- 全findingを収集してから、根本原因単位で関連修正を一括実装する。
- 修正後は新しい実装snapshotを固定し、固定済みINT・planned delta・preservation contract・U0を変更せず、CHGのactual delta、impact cone、cut proof、予測内外の変更誘発failure、該当するCONT subpacketを再導出する。blind-first監査とactual impactからの追加だけで `U1` を作り、第10節の収束ゲートとEvidence Dependency Mapで失効したclaim・risk vector・追加impactだけをテスト前の早期再監査へ渡す。サブエージェントの追加attemptで再監査を開始する場合も、第6節のユーザー向け表示先行条件を新しい作業turnごとに通過する。証拠同一性を確認できる未変更claimはreview keyを継承し、全監査しない。
- 早期再監査でテスト移行可能と判定された後だけ、第7節の共通テスト結果遷移へ戻る。

監査結果が `未証明` の場合は、事前固定した証拠・時間・token予算と停止条件の範囲内で、判定に寄与する追加証拠を取得するか、取得を妨げる正確な阻害要因を記録する。再入場前に第10節の監査・検証往復収束ゲートを通し、次の一往復が変え得るclaimと新しいidentity-bound evidenceがない場合は同じ監査・testを繰り返さない。予算へ到達した、安全で比例的な証拠経路が残らない、または阻害が確定した場合は無条件に反復せず、第10節の目的進捗・収束性ゲートで再計画、ユーザー判断待ち、技術的阻害、対象操作No-Go、release No-Go、完了No-Goを区別する。対象操作またはreleaseのNo-Goを維持しても、安全な診断・再設計・同一scope内の再計画まで自動的に終了せず、予算到達だけを完了No-Goの根拠にしない。snapshot、test-plan、識別情報、環境が変わらない場合は再固定せず、追加証拠が変え得るclaimだけを限定再判定する。第7節の該当早期scope未証明の条件付き移行で後段証拠を取得した場合も、candidate-bearing identityとtest-plan identityの同一性を確認したうえで限定再判定し、テスト結果だけでPASSへ自動昇格させない。candidate-bearing対象が変わった場合は新しい実装snapshotを固定するが、Evidence Dependency Mapで失効したclaimに限る早期差分監査、必要な共通テスト結果遷移、release candidate固定、最終監査の順へ戻る。test planだけが変わった場合はversion付きsupplementと限定再screenを使う。No-Go要否は第15節の未証明基準で判断する。

修正回数、監査・検証再入場、目的進捗、収束性と停止判定は第10節の共通修正回数台帳、監査・検証往復収束ゲート、および目的進捗・収束性ゲートを正本とし、監査findingだけでなくpreflight、テストFAIL、診断性変更、package・runtime・実環境その他すべての経路で共通適用する。
