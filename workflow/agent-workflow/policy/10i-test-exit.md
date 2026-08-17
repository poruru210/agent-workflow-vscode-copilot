### テスト修正継続・退出・作業再配分ゲート

test、fixture、runner、diagnostic、oracle、reportその他の検証系を修正または再実行する前に、TEST-RCまたは一行の理由記録で、`(1)` 当該検証が主目的・必須受入・release/action判断のどれに必要か、`(2)` 新しい因果・識別証拠、`(3)` 次の修正の反証可能な予測と共有原因への作用、`(4)` 同根因siblingをまとめて処分できる範囲、`(5)` 時間・token・tool・agent・環境・手戻りcost、`(6)` 次に実行可能なprimary-objective workの価値、`(7)` 退出時の残存risk・代替証拠・依存release範囲を比較する。

検証系修正を継続できるのは、次をすべて満たす場合に限る。

```text
主目的・必須受入・release/action判断のいずれかに必要または高いdecision valueがある
AND 前回と異なる因果・識別証拠またはVM修正根拠がある
AND 修正後に変わる命題・判定を反証可能な形で予測できる
AND 局所assertion合わせではなく共有TEST-RC・VM claimへ作用する
AND 追加cost・誤判定・手戻りriskを含む期待価値が次のeligible work以上である
```

いずれかを満たさない場合は回数にかかわらず検証系修正を退出し、次の一つへ処分する。

- `RETIRE-INVALID`: test・oracleがinvalidで、有効な代替証拠により依存するmandatory claimを閉じられる。旧test・結果・invalid理由・代替証拠の適用範囲を残す。
- `DEFER-NONMANDATORY`: 現在の主目的・必須受入・release判断に不要な改善として別作業候補へ分離し、現在taskでは再入場しない。
- `PROCEED-INDEPENDENT`: 当該命題は `未証明` のまま、依存しないobjective、work package、partitionまたは成果物へ進む。未証明に依存する範囲だけ完了・release判断を保留する。
- `RELEASE-NO-GO / WORK-CONTINUE`: mandatoryまたは高実害の証拠が代替不能であるため対象操作・releaseはNo-Goとするが、同じtest修正を繰り返さず、診断、再設計、環境整備、別の独立目的またはユーザー判断へ進む。
- `BLOCKED-DECISION`: 権限、外部環境、正本情報またはmaterialなtrade-offの選択が必要であり、正確な阻害を記録してユーザー判断を待つ。独立して進められる目的は続ける。

退出は検証結果のPASS、製品correctness、目的達成または完了を意味しない。mandatoryかどうかはFAIL観測後に都合よく変更せず、事前固定した要求、正常成功envelope、risk、U0、preservation contractから判定する。mandatoryから外すには正本要求のversion変更または肯定的な非該当証拠と該当する独立screenを要する。skip、quarantine、timeout、未実行、masked、retired、deferredをPASSへ数えない。

退出後はobjective ledgerから、現在の権限・scope内で、阻害された証拠に依存せず、主目的の正常成功経路、他の必須受入、Go/No-Goを確定する高情報価値、critical path短縮の順に、risk調整後価値が最も高いeligible workを選ぶ。単に計画上の次番号へ進まず、選んだwork、期待成果、依存しない根拠、保留したclaim、再入場条件をcheckpointへ固定する。退出したTEST-RCへ再入場できるのは、新しいraw evidence、異なる因果予測、VM・正本要求のmaterial変更、新しい安全な識別手段、mandatory状態の変更、または以前より明確に高いrisk調整後価値を持つ新手法がある場合だけとし、test名、version、runner、agent、reviewer、modelの変更だけでは戻らない。
