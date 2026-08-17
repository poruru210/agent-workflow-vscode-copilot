### 診断可能性ゲート

診断可能性は、主目的を止めずに不確実性を減らし、問題発生時に根本原因へ到達するための第一手段とする。合理的に到達可能な重大実害が未立証の問題へ、推測だけでearly return、disable、HOLD、reject、skip、retry、fallbackまたは例外の握り潰しを追加しない。挙動変更の根拠が不足する場合は、正常成功経路を維持する非blockingな観測・相関・原因識別を優先する。停止作用を伴う診断設計は診断強化だけで正当化せず、前項の正常継続性・停止合成subpacketで防止・封じ込めとして判定する。

主要な正常経路および合理的に到達可能な重大failure境界について、診断可能性を `PASS`、`FAIL`、`未証明`、`該当なし` のいずれかで判定する。`PASS` には、保存された証拠だけから合理的な時間内に次を再構成できることを要する。

- 要求・操作の開始点、operation IDまたはcorrelation ID。
- component、process、task、version、artifact、適用設定、feature flag、environment。
- 開始前の状態、主要phase、状態遷移、guard・分岐・early returnの判定とreason code。
- 外部依存の要求と応答区分、timeout、retry、cancel、fallbackの因果順序。
- 正常状態を最初に破った `first fault`、直接原因、責任componentまたは層にある根本原因、寄与条件。
- 影響対象と非影響対象、cleanup、containment、rollback、recovery、および最終利用者へ返した結果。

新規実装、計画保守・移行、および状態遷移、外部依存、非同期・並行、retry・timeout・fallback・recoveryを追加または変更するwork packageでは、初回実装前の設計・変更準備ゲートで診断性設計checkを行う。上記のうち必要なoperation・correlation、主要phase、stable reason code、依存結果、first-fault候補、状態遷移、保存対象、機密data除外、停止・復旧結果をどこで観測するかを定め、単純・同期的・局所的で既存観測だけで十分な項目は理由付き `該当なし` とする。これにより、早期監査で初めて診断設計不足を発見する手戻りを減らす。

最後に出た例外、timeout、retry exhaustion、cleanup failureだけを根本原因としない。後続failureはfirst faultと区別して因果順に記録する。主処理を実行していない結果を正常成功として記録せず、少なくとも `主目的完了`、`入力不正`、`前提不成立`、`限定guard停止`、`ユーザー停止`、`外部依存障害`、`timeout`、`cancel`、`fallback`、`unsupported`、`invariant違反`、`内部障害`、`原因未確定` を安定したreason codeで区別する。

診断項目には、どのfailure、実害判定、復旧判断に使うかを結び付ける。使用目的のない無制限log・telemetry・state dumpを追加せず、機密dataや個人情報を必要以上に記録せず、性能・容量・可用性への影響を予算化する。診断性補強には、必要に応じてsampling・rate limit、event集約、cardinality・volume・retention上限、redaction、bounded buffer、hot pathの同期I/O回避、CPU・memory・disk・network・latency budget、feature flag・無効化・rollback、および証拠取得後の維持・削減条件を持たせる。診断性の一般的向上だけでscopeを拡大せず、第4節の新規発見・主目的逸脱ゲートで現在failure・受入・再発防止・判断確定への価値を判定する。問題発生後の診断では回復不能な金銭・安全・data・security上の実害を取り戻せない場合、診断可能性だけで許容せず事前の防止または封じ込めを要求する。

原因識別のためのprobeが、隔離済み・非永続、外部writeなし、candidate-bearing source・artifact・設定・永続状態を変更しない、実行後の復元と非影響を確認可能、かつ事前固定した入力・最大回数・停止条件内である場合は、出荷される診断実装とは分けた軽量diagnostic-probe分岐を使える。probe前baseline supplement、probe identity・input・environment、取得証拠、実行後の復元・非影響を記録し、根因packetへ結び付けて終了する。条件を一つでも満たさない、probe codeや設定がcandidateへ入る、外部状態を変える、または高い不可逆実害が検出前に生じ得る場合は、通常の変更または外部action経路へ戻す。軽量probe PASSを製品の診断可能性PASS、実装PASS、release PASSへ転用しない。
