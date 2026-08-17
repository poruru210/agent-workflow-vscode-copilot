# VS Code GitHub Copilot 全体作業方針

> **VS Code Copilot 専用版**  
> この文書は VS Code の GitHub Copilot Agent、Custom Agents、Subagents、Agent Skills、Hooks、Language Model Tools を前提とする。共通Coreや他ハーネス向けadapterを定義せず、このファイル自体をVS Code Copilot運用の詳細正本とする。  
> Custom Agentはrole/tool boundaryを固定し、modelは原則固定しない。Subagentはinvocationごとにstatelessである。Hooksはpreview機能であり、policy enforcementの補助的な決定層として使うが、Hookの存在だけを受入PASSの証拠にしない。



## Detailed policy sections

Read these files **in order**. Together they are the detailed source of truth; no section is optional merely because it is stored separately.

- [1. 目的と適用範囲](01-section-01.md)
- [2. 基本原則](02-section-02.md)
- [3. リスク分類](03-section-03.md)
- [4. ステップと進捗管理](04-section-04.md)
- [5. 親エージェントの責任](05-section-05.md)
- [6. サブエージェントの利用](06-section-06.md)
- [7. 標準フェーズと作業種別分岐](07-section-07.md)
- [8. 作業前baselineの凍結](08-section-08.md)
- [9. エラー発生時の診断](09-section-09.md)
- [10. 根本原因と修正着手ゲート](10-section-10.md)
- [11. 実装方針](11-section-11.md)
- [12. 分割テスト](12-section-12.md)
- [13. 実装snapshotとrelease candidateの固定](13-section-13.md)
- [14. 二段階の非テスト依存独立監査](14-section-14.md)
- [15. findingの到達可能性・変更起因性・実害ゲート](15-section-15.md)
- [16. 監査findingの診断、修正、再監査](16-section-16.md)
- [17. 完了判定と最終報告](17-section-17.md)

## Model routing

For every delegated invocation, also apply [model-routing.md](model-routing.md).
