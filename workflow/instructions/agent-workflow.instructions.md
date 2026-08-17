---
name: Agent Workflow
applyTo: '**'
description: Global bootstrap for the rigorous VS Code Copilot multi-agent workflow with dynamic model routing.
---

# Agent Workflow bootstrap

For every chat request, first classify whether the compact branch is allowed. Compact requires all of: short, single-purpose, read-only, low-risk, no implementation/file/setting change, no diagnostic/test execution, no formal audit, no external-action planning/write, no delegation, no correction cycle, no release/operation decision, no volatile identity/freshness, and no material harm from an incorrect answer.

If any condition is false or uncertain, use the `agent-workflow` skill and its detailed VS Code Copilot policy before substantive action. For orchestration-heavy tasks, use the `Agent Workflow Orchestrator` custom agent.

Do not bind worker/reviewer roles to fixed model names. Before every subagent invocation, use the live `#workflowModels` catalog when available and dynamically select the minimum sufficient currently available model from job requirements, risk, independence, cost/latency evidence, and current official model information. Show job/model/reasoning/rationale before invocation. Remember that VS Code subagent invocations are stateless and requested subagent models cannot exceed the parent model cost tier.
