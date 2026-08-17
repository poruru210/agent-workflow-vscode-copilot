## 8. 作業前baselineの凍結

変更後にエンバグ、デグレ、既存機能破壊、非要求変更を識別できるよう、実装、修正、診断テストその他の状態を変え得る操作の前に、現状を変更前baselineとして凍結する。baselineは変更後の実装snapshotおよびrelease candidateとは別の証拠であり、後から上書きしない。

baselineでは、対象とリスクに応じて少なくとも次を記録する。

列挙した層を機械的にすべて取得する前に、主目的・必須受入、変更または診断経路、既存diff、外部作用、回帰時の比較へ因果接続する層をbaseline applicability mapで選ぶ。肯定的なcontrol・data・state・build・runtime・external-flow証拠により接続不能な層は、理由付き `該当なし` として取得しない。接続が不明な層は `未証明` とし、通常・高リスク、影響範囲不明、production・release、金銭・security・safety・privacy、不可逆作用では広い側へ倒す。局所作業という名称だけでruntime、GUI、永続化、package、外部状態を除外せず、applicability判定costが安価な直接取得以上なら直接取得する。

- 有効なwork-definition manifestのversion、hash、ユーザー要求、設計、必須受入条件、candidate-bearing変更ではplanned semantic delta・許可side effect・preservation contract、許可scope・対象外、変更禁止範囲、権限・必要な明示確認
- 比較対象baselineのID、証拠manifest、取得済み・未証明・該当なしの完全性、および監査対象範囲・観点ID
- 正本となるソース、対象ファイル、版、識別情報、時刻
- commit、branch、作業ツリー、既存diff、未追跡ファイル、および今回の変更との境界
- 既存のpackage、EXE、ZIP、生成物、配布物、その内容とハッシュ
- 設定、環境変数、feature flag、依存関係、lockfile、toolchain
- 稼働中のruntime、process、実行パス、version、引数、ログ、telemetry
- DB、ファイル、queue、cache、checkpointその他の永続化状態とschema/version
- GUIの表示・操作結果、外部サービス、ブラウザ、デバイスその他の外部状態
- 受入対象とpreservation contractに関係する既存の正常経路・consumer挙動・API・互換性・性能・負荷・資源使用の観測値
- 既存テストの対象、実行コマンド、件数、結果、所要時間、ログ、既知の失敗

各証拠には、取得時刻、取得元、識別子またはパス、取得方法、対象範囲を付け、可能なものはハッシュまたは再取得可能な機械可読記録にする。テストや観測自体が状態を変え得る場合は、先にソース、作業ツリー、artifact、永続化状態を保存し、隔離環境または復元可能な方法で取得する。

対象外の層は理由付きで `該当なし` とできる。対象に関係するが取得していない、取得不能、または信頼できる形で固定できていない層は `未証明` とし、取得したかのように扱わない。受入条件必須の比較、合理的に到達可能な重大経路、金銭・安全・データ等の高実害、または重大な回帰判定に必要なbaselineが欠ける場合はNo-Goとする。対応外、到達不能、または任意の追加比較に限られる欠落は、自動No-Goとはせず理由と残存リスクを明記する。

baselineは「変更前から正しかった」ことの証明ではない。既知の失敗、既存のdirty state、環境差もそのまま記録し、変更による悪化と既存問題を区別する比較基準として使う。

baseline固定後に新しい要求、受入条件、権限情報、ログ、外部状態、比較証拠その他を得ても、元baselineを上書きしない。取得時刻、取得理由、取得前後の境界、元baselineとの関係、影響する比較・監査範囲を持つversion付きsupplementとして追記する。後知恵で重大な比較基準、受入条件、対応scope、権限、監査範囲を都合よく再定義せず、work-definition変更として第7節の再評価・再監査遷移を通す。

