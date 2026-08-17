### 監査・検証往復収束ゲート

監査は、主目的、必須受入、変更安全性、対象操作またはrelease判断を変え得る欠陥・未証明を発見または反証するために行い、監査PASSの取得、finding件数、監査・テスト往復回数を成果にしない。早期監査、test-plan screen、分割テスト、最終監査、pre-action audit、post-action監査、finding再監査へ再入場する前に、既存台帳または一行記録へ次を固定する。

- 未解消の主目的ID・必須受入命題・変更安全命題と現在の `PASS`・`修正要`・`未証明`。
- 前回以降に変わったcandidate・snapshot・CHG、test-plan supplement・U1、baseline・target・freshness、または新しいraw evidenceのidentity。
- finding・未証明の根因と該当するRC・VER・INT・CHG・CONT、およびEvidence Dependency Map上で失効した命題。
- 今回だけ再確認するscope、次の一往復で変え得る判定、再利用する証拠、再実行しない範囲、主目的達成への寄与。

全体hashはcandidate identityと変更検出に使用するが、hash変化だけで全監査命題を失効させない。actual diffとEvidence Dependency Mapにより、差分を次のように分類する。

- `R0 identity/mechanical`: 改行、順序非依存metadata、生成時刻その他、意味・挙動・成果物・環境へ非影響を決定的に示せる差分。identity・parse・diff確認だけで閉じる。
- `R1 local semantic`: 局所表示、診断文言、独立した設定その他、影響境界を肯定的に示せる差分。該当命題、直接consumer、必要なoracleだけを再確認する。
- `R2 shared boundary`: API・schema・共通関数・共有state・永続化・停止guard・権限・外部作用・性能経路その他の共有契約差分。到達可能なimpact coneと関係risk vectorへ拡大する。
- `R3 evidence-wide`: 要求・必須受入・正本・baseline・権限のmaterial変更、広域設計変更、identity chain断絶、またはimpact boundaryを証明できない差分。失効が及ぶ必要範囲を全面再確認する。

小差分、同一ファイル内、ログだけという名称をR0/R1の根拠にせず、hot path、制御flow、機密性、共有consumerその他へ作用すればR2以上とする。逆に全体hash変更、ファイル数、差分行数だけでR3にしない。各監査結果は `snapshot/evidence identity + work-definition version + claim ID + risk vector + evidence version` をreview keyとし、terminalに処分済みの同一keyを、findingの言い換え、同じlogの再読、同一test再実行、reviewer・model交代、または表示・格納形式だけの変更で繰り返さない。

再入場は次の分岐とする。

```text
candidateまたは対象状態が変化
-> Evidence Dependency Mapで失効命題を抽出
-> 影響差分だけ再監査し、必要なU1 partitionだけ再テスト

test planだけが変化
-> version付きsupplementと限定screen
-> 実装構造監査を再実行しない

同一対象へ新しい識別証拠がある
-> その証拠で変わり得る未証明命題だけ限定再判定

上記がなく、次回で判定が変わる合理的見込みもない
-> 同一監査・同一testを反復しない
-> 診断、再計画、理由付き残存risk、または適切な対象操作・release No-Goへ移る
```

ただし、主目的・必須受入が未達、mandatoryなU0/U1命題が未実行、candidate identityがmaterialに変化、または新証拠が既存結論を反証し得る場合は、このゲートを監査・検証省略に使わない。早期構造監査PASS後に動的証拠が未取得という理由だけで同じ構造監査へ戻らず、動的testが構造命題を直接反証した場合だけ該当命題を限定再判定する。経過時間または往復回数で強制終了せず、判断を変える新証拠と比例的な経路がある限り継続できる。反復停止は完了または目的達成PASSではなく、主目的未達なら診断・設計・実装・証拠・権限・環境の阻害層を明示して次の有効経路へ移る。
