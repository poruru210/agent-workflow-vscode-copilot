## 12. 分割テスト

第7節で許可する隔離済み・決定的・安価でsnapshot同一性を変えないmechanical preflightだけは早期監査前に実行できる。同じparse、compile、import、collection、schema、format等でも、成果物または状態を変更する、非決定的、機能動作を含む、高コスト、隔離不能な場合はpreflightとして扱わず、早期監査後の分割テストへ含める。

早期独立監査の通過、条件付きテスト移行、または第14節の低リスク早期監査省略分岐後、最終独立監査の前に行うテストは、最初から全件を一括実行しない。対象に応じて、次のような区分に分ける。

- import、collection、静的確認
- コンポーネント別単体テスト
- 機能別テスト
- 正常系
- 異常系、failure injection
- 永続化、再起動
- 並行性、排他
- 統合テスト
- GUI、ブラウザ
- package、配布物
- 実環境

実装またはcandidate-bearing変更の前に、要求・C0、正常成功envelope、planned impact cone、state model、preservation contract、既知のfailure model、RCの反証予測、およびINTの介入・影響予測から初期検証母集団 `U0` を固定する。`U0` はtest名の一覧に限定せず、検証する命題、対象partition、supported entry・state・sequence、期待する外部観測可能なbehavioral oracle、必要なfixture・environment、証拠層、選択または代表化の根拠を持つ。新規実装では設計上の要求・riskとINT、修正では製品根因・検出責任・INT、保守・移行では変更目的・互換性境界・INT、文書・設定・外部操作では該当する検証mechanismへ読み替える。

VMが適用される検証では、原則としてstate、identity、event family、ordering、clock、observer、path、oracleの各claimを小さく決定的なconformance partitionで先に閉じ、その後に未閉包の相互作用だけをboundedなintegrated scenarioで確認する。統合・実環境scenarioを先行するのは、それでしか取得できない主目的・interaction命題、隔離・復元、停止条件、identity、結果が変える次判断を事前固定した場合に限る。小testの件数、巨大scenario一回のPASS、単一成功時系列の再現を網羅性の根拠にしない。

fail-fastによる後続failureのmaskingは、assertion dependencyを静的に確認して処分する。soft assertionまたは複数failure収集は、後続操作が当該assertionの真値に依存せず、状態整合性・安全性・oracle有効性を維持し、partitionを隔離・復元できる場合だけ使う。前提、共有stateまたは安全性へ依存する後続はhard barrierまたは別partitionとする。mandatory assertionのfailureは収集後もFAILであり、fail-fastで未実行のassertionは `masked`、依存不成立は `阻害` とし、PASSへ数えない。

変更または新設したVM classごとに、必要最小の代表positive variant、controlled negativeまたはfault-sensitivity、および正常成功envelope・preservation contract由来のpreservation oracleを対応付ける。controlled faultは検証感度の証拠であり、製品correctness、主目的PASSまたはrelease PASSの代用にしない。

実装snapshot固定後、blind-first早期監査が独自導出した仮説とactual impactから、実行対象は `U1 = U0 + blind-audit追加 + actual-impact追加` として確定する。`U0` のcase、partition、oracle、threshold、fixture、実経路または必須性を、candidateや途中結果に合わせて黙って削除・弱化・置換しない。正本要求の変更はwork-definition更新・rebaseline・影響範囲の再screenを要する。test自体の誤りが判明した場合も、元caseを履歴から消さず `invalid-oracle` その他の原因、製品判定への影響、replacement、独立確認を記録する。

実行前にテストマトリクスを作り、`U0`・`U1` のidentityと差分、各区分の対象、実行方法、依存関係、共有リソース、予定タイムアウト、進行状況、結果、ログ、未実行理由を記録する。第7節の検証範囲・証拠適用性ゲートの分類、適用する既存証拠ID、選択した検証level、cost判断、拡大条件、停止条件も主目的・受入条件ごとに対応付ける。

テストマトリクスでは、各主目的IDを正常成功経路の入口、主処理、必須状態変化・副作用、最終成果へ対応付ける。主要なfailure境界では、リスクに比例したfailure injectionまたは代替証拠により、保存された証拠からfirst fault、直接原因、根本原因の責任層、影響範囲、復旧結果を区別できることを確認する。修正では少なくとも、`根因仮説が誤ればFAILするoracle` と `介入が正常成功・preservationを壊せばFAILするoracle` をRC/INTから独立に対応付ける。candidate-bearing変更ではINTとCHG packetを結び、親・根因challenge・blind-first早期監査が独立導出した変更誘発failure仮説の和集合について、T0等で既に閉じたものと後段証拠を要するものを分け、後者をsupported実経路、preservation contract由来のbehavioral oracle、必要最小partitionへ対応付ける。testやpatchから仮説を逆算せず、単なる例外発生、log出力、mock呼出し、正常終了だけを目的達成、変更安全性または診断可能性PASSの証拠にしない。

CONT subpacketが適用される変更では、少なくとも次を `U1` へ含める。全guardが登録・有効でpredicateが偽となる正常成功経路、各変更guardの陽性、境界直外の陰性、同じsupported input・state・sequenceでbaselineは成功しcandidateが停止する反実仮説、代表的な支配・`GLOBAL_CUT`、sticky stop、正常な回復、試行枯渇、不正または未検証resumeの拒否である。すべてのguardが同時発火する非現実的caseを要求せず、実際の合成順序・共有state・到達可能性に沿う。

全組合せを機械的に実行しない。mandatory、高実害、変更された作用、支配関係、回復境界は全件を扱い、残りはrisk・state・effect・recovery・oracleによる等価partitionから代表を選ぶ。samplingが必要なら、baseline identity、work-definition hash、`U` version、stratum等から再現できる事前固定seedと選択規則を用い、結果を見てcaseを選び直さない。校正のないcoverage数値やcase数だけを網羅性の根拠にしない。

`U0` 固定後、特にcandidate、部分結果、borderline結果、または最初のFAILを観測した後に、skip、削除、quarantine、timeout、retry、threshold、assertion、fixture、mock、seed、順序、environmentを変更する場合は `test-intervention ledger` に旧値・新値、変更時点と観測済み結果、原因、正本由来oracle、false positive・false negativeと主目的への作用、変更前後の比較証拠、独立screen、影響する既存結果を記録する。skip・quarantineしたcaseはPASSではなく未実行または阻害として残し、mandatoryならrelease No-Goとする。threshold変更は結果を通すためでなく要求・riskから導出した事前判定規則を要する。

検出責任があるfailureの修正では、test matrixまたは該当する検証記録をverification-escape packetへ結び、earliest breakを解消するpartition、fixture・setup、supported entryからの実経路、behavioral oracle、report・CI・release gate、pre-fixまたはcontrolled-fault感度証拠、fixed candidateの期待結果を示す。検証系自体にfailureがある場合はVM・TEST-RC、失効claim、同根因sibling、assertion dependency、修正予測、退出・代替証拠を結ぶ。新規実装・保守・移行では、設計・変更準備時の検証能力mapを同じ項目へ読み替える。永続的な検証変更が不要な場合は、既存mechanismが根因修正後に当該failureを検出できる肯定的証拠または理由付きN/Aを記録する。

タイムアウトは安全装置であり、原因特定手段ではない。長時間処理には区間別ログ、heartbeat、現在処理中の対象、段階別タイムアウトを設定する。

分割実行後、各区分の和集合が `U1` と一致し、`U0` からの無断削除・弱化がなく、意図しない漏れがないこと、およびCHG・CONT packetで後段証拠を要するとした到達可能でmaterialな仮説が未処分のまま残っていないことを確認する。impact coneまたはCONT合成表の各branchは、T0、実行済みtest、局所cut proof、独立根拠を持つ理由付き該当なし、または `未証明` のいずれかへ明示的に処分し、materialなorphan branchがあれば網羅性をPASSにしない。

分割テスト通過後、相互作用、順序依存、状態汚染を検出するため、必要に応じて全件の回帰テストを実施する。全件テストは分割テスト、影響cone、保存契約または変更誘発failure閉包の代用にしない。

実装または修正後の分割テストと再テストはすべて第7節の共通テスト結果遷移に従う。途中で一つでもFAILした場合は、証拠を保存し、独立して安全な残りの診断・テスト区分を継続して失敗分布を確定してから、分割診断と根本原因ゲートへ戻る。製品RC、VER、TEST-RCを分離し、同じVM claim・TEST-RCの再露出では次のassertionを局所patchせず、第10節の継続・退出・作業再配分ゲートを通す。製品修正後は新しい実装snapshotを固定して早期差分監査を完了してから分割再テストへ戻る。test-planだけの修正はversion付きsupplementと限定screenを通す。FAILまたは受入条件に必須の未証明がある状態ではテスト網羅性確認をPASSにせず、release candidateを固定しないが、依存しないobjective・work packageは同ゲートの `PROCEED-INDEPENDENT` で進められる。

テスト前に、candidate-bearing identityと、テスト証拠metadataおよび宣言済みの隔離一時状態との境界をテストマトリクスへ記録する。candidate-bearing層には、該当するsource・worktree、設定、dependency・lockfile、toolchain input、feature flag、build・generation inputと生成物、package、runtime設定、永続的な候補状態、environment、platform identityを含める。ログ、レポート、時刻、証拠索引等は、候補の挙動、build input、成果物、環境へ影響しないことを事前定義し肯定的に証明した場合だけcandidate-bearing差分から除外できるが、テスト証拠として保存する。テスト用runtime・persistence stateを除外する場合は、事前に一時状態として宣言し、隔離、復元手順、停止条件、候補への非影響の確認方法を定める。各partitionの前後でcandidate identityと共有・永続stateを照合し、予期しない汚染が後続caseを都合よくPASSまたはFAILさせていないことを確認する。

build、package、code generationその他candidate-bearing層を意図して生成または変更する操作は、関連テストより前に完了する。その入力と生成物を含む新しい実装snapshotを固定し、必要な早期差分監査を終え、その正確なartifactをテストする。関連テスト後にcandidate-bearing層を意図して作り変えない。テスト実行自身がcandidate-bearing層を予期せず変更した場合は、単なる再snapshotまたは再テスト分岐とせず当該partitionのFAILとする。証拠を保存し、安全な残りpartitionを続行してから、分割診断、根本原因ゲート、共通修正回数台帳、修正、新snapshot、早期差分監査、再テストの順を通す。宣言済み一時状態は復元と候補への非影響を証明し、candidate identityとは別に記録する。復元不能、復元結果未証明、または候補への影響がある場合はFAILまたは受入上の `未証明` とする。
