#### 正常継続性・停止合成subpacket

early return、disable、HOLD、skip、reject、fail-closed、fallback、timeout、retry exhaustion、feature flagその他、supported scopeの処理継続、可用性、throughput、到達可能性または回復性を新設・変更・削除するcandidateでは、CHG packet内に `CONT-<id> normal-continuity and stop-composition subpacket` を持つ。非実行成果、または該当作用を変えない変更では、actual diffと影響coneに基づく一行の理由付き `該当なし` でよく、新しいphase・監査・agentを増やさない。

作業全体の進行状態、製品への作用、発生eventの回復状態を混同せず、次の三軸で記録する。

- `W 作業状態`: 継続、再計画、ユーザー判断待ち、技術的阻害、対象操作No-Go、release No-Go、完了No-Go。
- `E 作用`: `ALLOW`、対象または機能を局所遮断する `LOCAL_CUT`、主目的または広い機能集合を遮断する `GLOBAL_CUT`。
- `R 回復状態`: eventなし、latched、診断中、recovery-ready、回復試行中、verified-resume、recovery-failed。`GLOBAL_CUT` は製品作用の分類であり、それだけで安全な診断、回復、再設計その他の作業全体を終了しない。

subpacketには、リスクに比例して次を含める。

- baselineとcandidateの正常成功envelope、停止を許す領域、および `NewlyStopped = BaselineSuccess - CandidateSuccess`。planned delta外のmaterialな `NewlyStopped` は、個別guardのtest PASSにかかわらず修正要とする。
- 各guardのID、predicate、supported input・state・sequenceからのactivation reachability、発火後に実際の作用へ届くeffect reachability、`ALLOW`・`LOCAL_CUT`・`GLOBAL_CUT`、reason code、解除条件、回復経路、前段guardを条件とした固有の防止・封じ込め、診断、回復の役割。
- 前段guardとの合成順序、優先順位、共有state、同時・連続発火、latch、timeout・retry・fallbackとの相互作用、全guardが登録・有効だが正常条件ではpredicateが偽となり最終成果へ到達する経路。
- `GLOBAL_CUT` ごとのcut範囲と、それにより作用を失う下位guard。下位guardは、削除・統合、診断専用、回復前提、回復後再有効化のいずれかへ処分し、固有の早期局所防止、原因識別、回復、または回復後保護がないdead・完全支配guardを残さない。
- 各guardの前段guard条件付きの限界価値。予防・封じ込め、診断、回復の固有価値と、誤停止、正常成功envelope縮小、latency・throughput・資源、復旧時間、主目的阻害の運用損失を比較する。校正された根拠がない数値scoreを捏造せず、判断不能は `未証明` とする。
- latchされたeventが、必要なscheduler・dependencyが利用可能な前提で、有限な回復手順と最大試行回数を経て `verified-resume`、対象操作No-Go、release No-Go、技術的阻害、またはユーザー判断へ到達する回復liveness。`recovery-failed` は対象操作No-Go、release No-Go、技術的阻害、またはユーザー判断のいずれかへ束縛する。event identity、永続attempt counter、解除条件、解除後stateを持ち、timer経過、restart、log出力、例外なしだけで解除PASSにしない。

fail-closedは観測・診断機能ではなく正常挙動を変える防止・封じ込めである。観測不足だけを理由に `GLOBAL_CUT` を追加してはならない。ただしtarget、権限、必須invariantを安全に束縛できず、実行前の観測が操作許可の必要条件である場合、または検出前に回復不能な高実害が生じる場合は、代替案、正常成功envelopeへの作用、回復経路を比較して対象操作・releaseのNo-Goまたは最小cutを選べる。主目的を停止専用へ暗黙に再設計せず、materialなtrade-offはユーザー判断へ渡す。

正常継続性・停止合成は、各guardの単独陽性・陰性だけで閉じない。合成表は同じpredicate・作用・診断・回復signatureを持つguardを等価group化でき、全組合せを無制限に列挙しない。各guardのactivation/effect reachability、代表的な支配関係、`NewlyStopped`、全guard有効時の正常経路、sticky stop、回復成功・試行枯渇・不正resume拒否を、T0、完了・処分済みT1/T2を含む複合証拠、または独立根拠を持つ理由付き該当なしへ解決する。planned delta外、正常成功envelope違反、または未承認のmaterialな `NewlyStopped`、役割未処分のdead guard、回復liveness欠落、または到達可能な未解消 `GLOBAL_CUT` はreleaseをNo-Goとし、明示要求・承認済みplanned delta内の停止、非material、または肯定的に遮断された未証明は第15節で個別判断する。
