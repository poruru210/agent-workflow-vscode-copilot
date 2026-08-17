#!/usr/bin/env python3
import sys, json, os, re, shutil
from pathlib import Path
from datetime import datetime, timezone

def now(): return datetime.now(timezone.utc).isoformat()

def get_root(data):
    cwd = data.get('cwd') or os.getcwd()
    return Path(cwd).resolve()

def load_json(path, default):
    try: return json.loads(path.read_text(encoding='utf-8'))
    except Exception: return default

def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    tmp.replace(path)

def append_jsonl(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a', encoding='utf-8') as f:
        f.write(json.dumps(value, ensure_ascii=False) + '\n')

def state_paths(root):
    d = root / '.agent-workflow'
    return d, d/'state.json', d/'audit'/'events.jsonl', d/'jobs-runtime.json'

def normalize_command(inp):
    if not isinstance(inp, dict): return ''
    for k in ('command','cmd','script','text'):
        v=inp.get(k)
        if isinstance(v,str): return v.strip()
    return ''

def is_write_tool(name):
    s=(name or '').lower()
    keys=('edit','replace','insert','create_file','createfile','deletefile','delete_file','writefile','write_file','applypatch','apply_patch','renamefile','movefile')
    return any(k in s for k in keys)

def command_is_obviously_readonly(cmd):
    c=cmd.strip().lower()
    readonly=(
        'git status','git diff','git log','git show','git branch --show-current','git rev-parse','git ls-files',
        'pwd','ls','dir ','get-childitem','get-content','type ','cat ','head ','tail ','grep ','rg ','findstr ',
        'sha256sum','shasum','certutil -hashfile','pytest --collect-only'
    )
    if re.search(r'[;&|\n]|\$\(', c):
        return False
    return any(c.startswith(x) for x in readonly)

def command_is_obviously_mutating(cmd):
    c=' '+cmd.lower()+' '
    patterns=[
      r'\bgit\s+(commit|push|merge|rebase|reset|checkout|switch|clean|add|rm|mv)\b',
      r'\b(rm|del|erase|rmdir|mv|move|cp|copy|touch|mkdir|chmod|chown)\b', r'\bfind\b.*\b-delete\b',
      r'\b(remove-item|set-content|add-content|out-file|new-item|copy-item|move-item|rename-item|clear-content)\b', r'\bsed\s+-i\b', r'\btee\b', r'>>|(?<![<])>(?!>)',
      r'\b(npm|pnpm|yarn)\s+(install|add|remove|update|publish)\b', r'\b(pip|uv)\s+(install|uninstall)\b', r'\b(apt|apt-get|dnf|yum|brew)\s+(install|remove|upgrade)\b',
      r'\b(docker|kubectl|helm|terraform)\b.*\b(apply|delete|destroy|push|create|patch|replace|rollout)\b'
    ]
    return any(re.search(p,c) for p in patterns)

def output(o):
    sys.stdout.write(json.dumps(o,ensure_ascii=False))

def main():
    raw=sys.stdin.read()
    try: data=json.loads(raw) if raw.strip() else {}
    except Exception: data={}
    root=get_root(data); d,state_path,audit_path,jobs_path=state_paths(root)
    state_exists=state_path.exists(); state=load_json(state_path,{}) if state_exists else {}
    event=data.get('hook_event_name','Unknown')
    if state_exists:
        append_jsonl(audit_path,{'at':now(),'event':event,'session':data.get('session_id')})
    if event=='SessionStart':
        if state_exists:
            msg=f"Agent Workflow durable state exists at {state_path}. Active phase={state.get('phase')!r}, objective={state.get('activeObjective')!r}, open mandatory claims={len(state.get('mandatoryOpenClaims') or [])}. Re-enter from durable state before inferring completion or next steps from chat history."
        else:
            msg='No .agent-workflow/state.json exists. Stay file-system-clean for a compact read-only answer. If the task enters the normal branch and durable state is warranted, initialize .agent-workflow/ from the Agent Workflow state templates before delegation, external actions, correction cycles, or long/multi-objective work.'
        output({'hookSpecificOutput':{'hookEventName':'SessionStart','additionalContext':msg}}); return
    if event=='PreToolUse':
        if not state_exists:
            output({'hookSpecificOutput':{'hookEventName':'PreToolUse','permissionDecision':'allow'}}); return
        phase=str(state.get('phase') or '').lower(); name=data.get('tool_name',''); inp=data.get('tool_input') or {}
        in_audit=phase in {'root-cause-challenge','root_cause_challenge','pre-action-audit','pre_action_audit','early-audit','early_audit','final-audit','final_audit'}
        if in_audit and is_write_tool(name):
            output({'hookSpecificOutput':{'hookEventName':'PreToolUse','permissionDecision':'deny','permissionDecisionReason':f'Agent Workflow phase {phase} is read-only; candidate/target edits are forbidden during audit.'}}); return
        cmd=normalize_command(inp)
        if in_audit and cmd:
            if command_is_obviously_mutating(cmd):
                output({'hookSpecificOutput':{'hookEventName':'PreToolUse','permissionDecision':'deny','permissionDecisionReason':f'Mutating terminal command blocked during read-only audit phase {phase}.'}}); return
            if not command_is_obviously_readonly(cmd):
                output({'hookSpecificOutput':{'hookEventName':'PreToolUse','permissionDecision':'ask','permissionDecisionReason':f'Audit phase {phase}: terminal command is not proven read-only; manual approval required.'}}); return
        output({'hookSpecificOutput':{'hookEventName':'PreToolUse','permissionDecision':'allow'}}); return
    if event=='SubagentStart':
        if state_exists:
            jobs=load_json(jobs_path,{'jobs':{}}); aid=data.get('agent_id') or 'unknown'
            jobs.setdefault('jobs',{})[aid]={'agentType':data.get('agent_type'),'status':'running','startedAt':now()}
            write_json(jobs_path,jobs)
        output({'hookSpecificOutput':{'hookEventName':'SubagentStart','additionalContext':'This VS Code subagent invocation is stateless. Follow only the supplied invocation lease and role boundary; do not assume prior attempts.'}}); return
    if event=='SubagentStop':
        if state_exists:
            jobs=load_json(jobs_path,{'jobs':{}}); aid=data.get('agent_id') or 'unknown'; rec=jobs.setdefault('jobs',{}).setdefault(aid,{})
            rec.update({'agentType':data.get('agent_type'),'status':'completed','stoppedAt':now()}); write_json(jobs_path,jobs)
        output({'continue':True}); return
    if event=='PreCompact':
        if state_exists:
            ck=d/'checkpoints'; ck.mkdir(parents=True,exist_ok=True)
            stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
            shutil.copy2(state_path, ck/f'state-{stamp}.json')
        output({'continue':True}); return
    if event=='Stop':
        open_claims=state.get('mandatoryOpenClaims') or [] if state_exists else []
        if open_claims:
            output({'continue':True,'systemMessage':f'Agent Workflow stopped with {len(open_claims)} mandatory claim(s) still open. Do not report completion unless they are explicitly resolved or user-approved exceptions exist.'}); return
        output({'continue':True}); return
    output({'continue':True})

if __name__=='__main__': main()
