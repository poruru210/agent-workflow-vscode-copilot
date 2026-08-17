## 13. 実装snapshotとrelease candidateの固定

変更前baselineを保持したまま、変更後状態を目的の異なる二種類のsnapshotとして固定する。実装snapshotとrelease candidateを同じ名称や識別子で扱わない。

### 実装snapshot

実装snapshotは、実装または修正が完了し、機能・統合・高コスト・状態変更テストを開始する前の状態である。第7節の限定mechanical preflightと早期独立監査の開始前に、少なくとも次を記録する。

- snapshot識別子、固定時刻、commitまたは作業ツリー識別情報
- 対象source・ファイル一覧、各hash、baselineからのdiff、直前の実装snapshotがある場合はそこからのdiff
- 設定、dependency、lockfile、toolchain、feature flag、build・generation input
- 早期監査に関係する生成物hash、platform・runtime identity、environment。まだ生成・実行していない層は `未証明` または `該当なし`
- 対象範囲、変更禁止範囲、比較対象baselineの識別情報
- version付きwork-definition manifestのID・hashと、比較baselineの証拠manifest・完全性、監査対象範囲・観点ID
- Evidence Dependency Mapのversion・hash、必須claim ID、依存する対象node・consumer・risk vector・失効条件、および継承可能なterminal review key
- 該当するRC・VER・INT packetのIDと状態、INTの介入link・共有mechanism・consumer・counterfactual・preservation予測、およびCHG packetのID、planned semantic delta、preservation contract、snapshot固定後にactual delta・impact cone・変更誘発failureを独立導出する状態
- 該当するCONT subpacketのID、正常成功envelope・停止許可領域・guard inventory・合成表、および初期検証母集団 `U0` のversion・hash。該当しない場合は理由付き `該当なし`

関連テストがbuild、package、code generationその他の生成物を対象とする場合、それらの意図した生成・変更は実装snapshot固定前に完了し、その入力と生成物hashをsnapshotへ含める。生成後のsnapshotを必要な早期差分監査へ渡し、その正確なartifactだけをテストする。関連テスト後に候補を意図して再生成しない。まだ生成していない層を `未証明` とできるのは、その層が当該snapshotに対する後続テストのcandidate-bearing対象でない場合に限る。実装snapshotは高コストテスト前の構造監査対象であり、テスト済みまたは出荷可能であることを意味しない。

実装snapshotごとにcandidate-bearing identityのmanifestを作る。該当するsource・worktree、設定、dependency・lockfile、toolchain input、feature flag、build・generation inputと生成物、package、runtime設定、永続的な候補状態、environment、platform identityを候補同一性へ含める。これとは別に、version付きwork-definition manifestとbaseline・supplementの証拠manifestをsnapshotのevidence identityへ結び付ける。テストコマンド、ログ、レポート、時刻、証拠索引その他のテスト証拠metadata、および宣言済みで隔離・復元される一時的runtime・persistence stateは別manifestにする。証拠metadataをcandidate-bearing identityから除外するには、その種別と格納先をテスト前に定義し、候補へ非影響であることを肯定的に証明する。一時状態を除外するには、隔離、復元、および候補への非影響を証明する。技術的なcandidate-bearing identityが同一でも、work-definitionまたはbaseline evidence identityが変われば第7節の影響範囲の証拠再利用ゲートを通す。

candidate-bearing manifestは層別fingerprint、取得境界、取得時刻、親子hashまたは同等の改ざん・変更検出情報を持つimmutable identity recordとして再利用できる。後段ゲートでは同じ全層を無条件に再収集・再hashせず、前回fingerprint以後に変更可能だった層、watch・diff・build記録等が変化を示す層、freshness必須層だけを再取得し、未変更層はrecordのidentityを照合して継承する。変更検出の完全性を立証できない、取得境界外の変更が可能、identity chainが切れた、または影響がmaterialなら該当層を再取得する。runtime、権限、volatile external state、実行直前target identityその他のfreshness必須確認はfingerprint継承で置換しない。

Evidence Dependency Mapは、claimごとに主目的・必須受入・preservation contract、根拠source・baseline・packet・test、対象nodeとupstream・downstream・consumer、risk vector、前提・freshness、PASSしたsnapshot・review key、および失効triggerを記録する。candidate全体のhashが変わっても、actual diffから当該claimへの到達経路がなく、前提・identity・freshnessが維持されることを肯定的に示せるclaimは継承できる。逆に技術hashが同じでも要求・受入・権限・baseline・証拠前提が変わったclaimは失効する。Map作成・更新costが回避する再読・再監査cost以上の粒度へ細分化せず、同じdependencyと失効triggerを持つclaimはgroup化できる。

### 証拠ブリッジ

第7節で `証拠ブリッジで継承` を選んだ場合は、既存証拠manifestと現実装snapshotのevidence identityの間にversion付き証拠ブリッジを固定する。ブリッジはcandidate-bearing identityを置換せず、どの受入条件のどの証拠層が、どの非影響証拠と限定検証により現candidateへ適用できるかだけを表す。現candidateで新規取得した証拠、既存証拠、非影響証拠を区別し、最終監査と最終報告から追跡可能にする。ブリッジの前提、freshness、identityまたは拡大条件が崩れた場合は該当証拠を `未証明` または `全面失効` へ戻し、必要な検証を再選定する。

### テスト対象同一性ゲート

分割テスト、網羅性確認、必要な全体回帰がPASSした後、release candidate固定前に、実際にテストした実装snapshotと現在状態を照合する。candidate-bearing manifestにあるsource・worktreeと各hash・diff、設定、dependency・lockfile、toolchain input、feature flag、build・generation inputと生成物、environment、package、runtime設定、永続的な候補状態、platform identityのうち該当する全層を比較し、テストコマンド、結果、ログ、証拠metadata、一時状態の復元証拠を対応するsnapshotと結び付ける。関連テストが固定snapshot内の正確なartifactを対象にしたこと、およびテスト後にcandidate-bearing層を意図して作り変えていないことを確認する。

テスト実行自身がcandidate-bearing identityを予期せず変更した場合は、テストPASSを現在状態へ引き継がず、単なる再固定にも進まない。当該test partitionをFAILとし、証拠保存、安全な残りpartition、分割診断、根本原因ゲート、共通修正回数台帳、修正、新しい実装snapshot、早期差分監査、必要な再テストを通す。テスト以外の許可された操作で対象内に挙動または成果物へ影響し得る差分が生じた場合も、テストPASSを引き継がず、新しい実装snapshot、早期差分監査、影響範囲に必要な分割テストと必要な全体回帰へ戻る。時刻、証拠索引、ログ格納先、署名その他、事前定義した証拠metadataだけが変わり、source、build input、挙動、成果物、環境へ影響しないことを肯定的に証明して記録した場合に限りcandidate差分から除外できるが、証拠として保存する。宣言済みの隔離一時状態は復元と非影響の証明後だけ別扱いにでき、復元不能または候補へ影響する場合はFAIL、復元・非影響が確認不能なら `未証明` とする。同じmandatory identity failureが再露出した場合は、固定回数で次の局所修正を決めず、第10節の新証拠・予測・価値・退出条件に従う。

### release candidate

release candidateは、実装構造監査とテスト準備構造screenがPASSまたは適正に省略され、該当早期scope未証明の条件付き移行を使った場合は同一snapshot・test-plan identityへの限定再判定がPASSし、受入に必須の後段証拠、分割テスト、網羅性確認、必要な全体回帰、テスト対象同一性ゲートがすべてPASSし、CHG packetの到達可能でmaterialな仮説と、該当するCONT subpacketの正常成功envelope・停止合成・回復livenessについて最終監査前に必要な証拠・処分が揃い、materialなorphan branchその他releaseを阻害する未解消がない状態の最終監査対象である。条件付きテスト移行それ自体、後段テストPASSだけ、またはいずれかの早期scope・変更安全命題のrelease阻害未証明が残る状態では固定しない。少なくとも次を記録する。

- release candidate識別子、固定時刻、commitまたは作業ツリー識別情報
- 全対象source・ファイルと生成物のhash、baselineからの全diff、テスト対象となった実装snapshotからのdiff
- 設定、dependency、lockfile、toolchain、feature flag、build・generation input、platform・runtime identity、environment
- 対応するテストマトリクス、結果、ログ、実行環境の識別情報
- package、EXE、ZIP、配布物、runtimeが該当する場合は内容、hash、実行パス、設定
- 比較対象baseline、証拠を引き継ぐ実装snapshot、テスト対象同一性ゲートの識別情報
- version付きwork-definition manifestのID・hash、baselineとversion付きsupplementの証拠manifest・完全性、監査対象範囲・観点ID
- Evidence Dependency Mapのversion・hash、継承したreview key、失効・追加したclaimと理由
- 該当するRC・VER・INT packetのIDと状態、INTの介入・影響予測、およびCHG packetのID、planned/actual semantic delta、preservation contract、impact cone・cut proof、予測内外の変更誘発failure仮説と証拠・処分・残存risk
- CONT subpacketのIDと状態、baseline/candidate正常成功envelope、`NewlyStopped`、guard合成・支配・回復liveness、`U0`・`U1`、test-intervention ledger、orphan branchの処分。非該当なら理由

固定したsnapshotの監査中は対象を読み取り専用とし、修正、build、生成、設定変更その他の同一性を変える操作を行わない。監査前後で識別情報、hash、差分、環境が変化していないことを確認する。変化した場合は証拠同一性を失った範囲を新しいsnapshotとして扱い、必要なゲートへ戻る。
