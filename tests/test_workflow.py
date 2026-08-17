from pathlib import Path
import json, re, sys, tempfile, subprocess, os
import yaml

ROOT = Path(__file__).resolve().parents[1]

def fail(msg):
    raise AssertionError(msg)

# Required layout
required = [
    ROOT/'workflow/agents/agent-workflow-orchestrator.agent.md',
    ROOT/'workflow/skills/agent-workflow/SKILL.md',
    ROOT/'workflow/hooks/agent-workflow.json',
    ROOT/'workflow/instructions/agent-workflow.instructions.md',
    ROOT/'workflow/agent-workflow/policy/README.md',
    ROOT/'workflow/agent-workflow/policy/model-routing.md',
    ROOT/'workflow/agent-workflow/scripts/workflow_hook.py',
    ROOT/'workflow/agent-workflow/scripts/workflow_hook.ps1',
    ROOT/'extension/src/extension.ts',
    ROOT/'extension/src/catalog.ts',
]
for p in required:
    assert p.exists(), f'missing required file: {p.relative_to(ROOT)}'

# Policy index links all 17 sections and they exist.
idx=(ROOT/'workflow/agent-workflow/policy/README.md').read_text(encoding='utf-8')
links=re.findall(r'\]\((\d{2}-section-\d{2}\.md)\)', idx)
assert len(links)==17, f'expected 17 policy sections, got {len(links)}'
for link in links:
    assert (ROOT/'workflow/agent-workflow/policy'/link).exists(), f'missing policy section {link}'

# No fixed model in custom agent frontmatter.
for p in (ROOT/'workflow/agents').glob('*.agent.md'):
    t=p.read_text(encoding='utf-8')
    front=t.split('---',2)[1] if t.startswith('---') else ''
    assert not re.search(r'(?m)^\s*model\s*:', front), f'fixed model in {p.name}'

# Hook JSON parses and contains expected events.
hook=json.loads((ROOT/'workflow/hooks/agent-workflow.json').read_text(encoding='utf-8'))
assert isinstance(hook.get('hooks'), dict)
for evt in ['PreToolUse','PreCompact','SubagentStart','SubagentStop']:
    assert evt in hook['hooks'], f'missing hook event {evt}'

# Python hook syntax + deterministic phase behavior.
pyhook=ROOT/'workflow/agent-workflow/scripts/workflow_hook.py'
compile(pyhook.read_text(encoding='utf-8'), str(pyhook), 'exec')
with tempfile.TemporaryDirectory() as td:
    td=Path(td)
    st=td/'.agent-workflow'
    st.mkdir()
    (st/'state.json').write_text(json.dumps({'phase':'early-audit','activeObjective':'OBJ-1','mandatoryOpenClaims':['C1']}),encoding='utf-8')
    payload=json.dumps({'hook_event_name':'PreToolUse','cwd':str(td),'session_id':'ci','tool_name':'edit','tool_input':{'path':'x.txt'}})
    cp=subprocess.run([sys.executable,str(pyhook)],input=payload,text=True,capture_output=True,check=True)
    result=json.loads(cp.stdout)
    assert result['hookSpecificOutput']['permissionDecision']=='deny', result
    payload=json.dumps({'hook_event_name':'PreToolUse','cwd':str(td),'session_id':'ci','tool_name':'execute','tool_input':{'command':'git status'}})
    cp=subprocess.run([sys.executable,str(pyhook)],input=payload,text=True,capture_output=True,check=True)
    result=json.loads(cp.stdout)
    assert result['hookSpecificOutput']['permissionDecision']=='allow', result

# Repository must not contain generated/build/bootstrap transport.
for forbidden in ['bootstrap','extension/out','extension/dist','MANIFEST.sha256','validation/result.json']:
    assert not (ROOT/forbidden).exists(), f'forbidden generated/bootstrap path tracked: {forbidden}'

print('workflow source validation PASS')
