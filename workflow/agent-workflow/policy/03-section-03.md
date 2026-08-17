## 3. リスク分類

作業開始時に、対象物の名称ではなく、操作のread/write、local・sandbox・non-production・productionの別、復旧可能性、外部効果、dataの機密性、金銭・安全・securityへの影響、および誤判定時の実害からリスクを分類する。複数の条件に該当するときは最も高いリスクを採用する。高い区分から下げるには、該当し得る高リスク条件が成立しないことの肯定的証拠と理由を計画へ記録する。

- 低リスク: read-onlyまたはno-writeで、局所的または隔離され、外部の永続状態を変更せず、materialなdata exposureがなく、容易に復元または再検証でき、誤判定時の実害が小さい。
- 通常リスク: boundedで可逆な変更、non-productionでの変更、一般機能または複数componentの変更、可逆なAPI・GUI・永続化その他の操作。ただし高リスク条件が一つも成立しない場合に限る。
- 高リスク: productionまたは外部への永続write、資金・決済・会計、安全、security・auth・permission、機密data、破壊的または不可逆な操作、公開send・publish・deploy・distribute・sign、稼働中runtimeへの操作、復元困難な変更、または誤判定が高い実害を生む作業。

package、EXE、API、GUI、ブラウザ、DB、外部サービス等の名称だけで自動的に高リスクとしない。hash取得その他のread-only inspectionは実際の外部効果と誤判定実害により低または通常リスクになり得る。build・packageの変更は通常リスク以上、sign・distribute・未信頼artifactの実行・production deployは高リスクとする。外部writeがない財務判断、security判断、release判定その他のread-only監査でも、誤判定時の実害が高ければ高リスクになり得る。

リスク区分、各判定軸の事実、採用理由、引下げの肯定的証拠を計画へ記録し、計画の粒度、担当数、モデル能力、推論強度、テスト範囲、監査系統数、外部操作前後のゲート、および完了証拠を調整する。

