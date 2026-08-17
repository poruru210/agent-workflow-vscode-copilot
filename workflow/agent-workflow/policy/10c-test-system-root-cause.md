### 検証系根因・検証モデル修正ゲート

`VER` は検出責任があった製品failureのescapeに限定する。製品failureが未確定または存在しなくても、test・fixture・runner・diagnostic・oracle・reportがfalse PASS、false FAIL、masked failure、非代表的な実経路、状態汚染または不正な判定を生んだ場合は、製品 `RC` と `VER` から分離した `TEST-RC-<id> test-system root-cause record` を固定する。TEST-RCの存在だけで製品不具合またはVERをConfirmedにせず、必要な場合は相互参照する。

TEST-RCには、対象のmandatory product claim・受入ID、VM IDと失効claim、raw test evidence、first incorrect test-system link、責任層、false positive・false negative・masking・observer effect、同じVM claimを共有するsupported sibling、主要代替原因、反証可能な修正予測、修正または退出で変わる次のGo/No-Go・受入判断、代替証拠、累積costを含める。primary分類は、`STATE-MODEL`、`IDENTITY-LIFECYCLE`、`EVENT-FAMILY`、`ORDERING`、`CLOCK-DOMAIN`、`OBSERVER-EFFECT`、`SETUP`、`PATH`、`ORACLE`、`REPORT-GATE`、`UNPROVEN`、`理由付きN/A` から選び、寄与要因を別記できる。

同じVM claimを共有するsupported siblingが再露出して当該claimを反証した場合は、test名、assertion、fixture、timeoutまたは期待値だけを次々に局所patchしない。旧case・旧oracle・観測済み結果を履歴に残してVM claimをinvalidとし、影響するstate・event・identity・ordering・clock・observer・oracle・assertion dependencyを再導出し、同根因を一括修正するか、後段の価値ゲートで退出する。test-plan supplementのversion、test名、runner、担当agent、reviewerまたはmodelの変更でTEST-RC、correction history、累積cost、未解消mandatory claimをresetしない。

VM・TEST-RCの独立確認は既存T0/T1/T2へ統合する。決定的なschema・identity・機械的不変条件はT0で閉じ、state machine、並行性、許容順序、oracle完全性、observer effectその他の意味判断がmaterialなら既存のbounded T1へ非重複観点としてまとめ、証拠衝突、高実害または相関blind spotが残るvectorだけをT2へ分離する。VM・TEST-RCだけを理由に新しい監査phaseまたはsubagent quotaを増やさない。
