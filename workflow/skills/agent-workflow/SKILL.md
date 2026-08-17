---
name: agent-workflow
description: Rigorous VS Code GitHub Copilot execution workflow for investigation, implementation, defect repair, maintenance, testing, independent review, external actions, and multi-agent orchestration. Use for any non-trivial task that needs changes, tests, audits, delegation, release decisions, or durable evidence.
user-invocable: true
---

# VS Code Copilot Agent Workflow

For substantive work, follow [policy index](../../agent-workflow/policy/README.md) and every section it lists, in order, as the detailed source of truth.
For every delegated invocation, also follow [model-routing.md](../../agent-workflow/policy/model-routing.md).

## Bootstrap

Use the compact branch only when every condition is affirmatively true: short, single-purpose, read-only, low-risk, no implementation or file/setting change, no diagnostic/test execution, no formal audit, no external-action planning/write, no delegation, no correction cycle, no release/operation decision, no volatile identity/freshness, and a wrong answer cannot cause material harm.

Otherwise enter the normal workflow before substantive action.

## VS Code-specific invariants

- Custom Agents define roles, tools, authority, and read/write boundaries. Do not hard-code models in role agents.
- Before each subagent invocation, call `#workflowModels` when available, create an invocation lease, select the minimum sufficient current model, and explicitly request that model in `agent/runSubagent`.
- Subagent invocations are stateless. A second attempt is a new invocation; pass only the required context and preserve blind-first independence where required.
- Maintain durable state under `.agent-workflow/` for long, delegated, external-action, multi-objective, or correction-heavy tasks.
- Repository/user hooks are enforcement aids. Do not treat hook execution as correctness evidence.
- During root-cause challenge, pre-action audit, early audit, and final audit, the audited candidate/target is read-only.

## Durable state initialization

When the task enters the normal branch and durable state is warranted, create workspace-local `.agent-workflow/` from the schemas in [state-template](../../agent-workflow/state-template/). Do not create runtime state for a compact read-only answer merely because a session started.
