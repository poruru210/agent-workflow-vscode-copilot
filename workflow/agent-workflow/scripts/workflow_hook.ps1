$ErrorActionPreference = 'Stop'
$raw = [Console]::In.ReadToEnd()
try { $data = $raw | ConvertFrom-Json } catch { $data = [pscustomobject]@{} }
$cwd = if ($data.cwd) { [string]$data.cwd } else { (Get-Location).Path }
$root = [System.IO.Path]::GetFullPath($cwd)
$stateDir = Join-Path $root '.agent-workflow'
$statePath = Join-Path $stateDir 'state.json'
$auditPath = Join-Path $stateDir 'audit\events.jsonl'
$jobsPath = Join-Path $stateDir 'jobs-runtime.json'
function Now-Iso { (Get-Date).ToUniversalTime().ToString('o') }
function Read-Json($p,$fallback) { if(Test-Path $p){ try { return (Get-Content $p -Raw | ConvertFrom-Json) } catch { return $fallback } }; return $fallback }
function Write-Json($p,$obj){ New-Item -ItemType Directory -Force -Path (Split-Path -Parent $p)|Out-Null; $obj|ConvertTo-Json -Depth 20|Set-Content $p -Encoding utf8 }
function Emit($obj){ [Console]::Out.Write(($obj|ConvertTo-Json -Depth 20 -Compress)) }
function Tool-IsWrite([string]$name){ $s=$name.ToLowerInvariant(); @('edit','replace','insert','create_file','createfile','deletefile','delete_file','writefile','write_file','applypatch','apply_patch','renamefile','movefile') | ForEach-Object { if($s.Contains($_)){return $true} }; return $false }
function Get-CommandText($inputObj){ if($null -eq $inputObj){return ''}; foreach($k in @('command','cmd','script','text')){ $p=$inputObj.PSObject.Properties[$k]; if($p -and $p.Value -is [string]){return $p.Value.Trim()} }; return '' }
function Cmd-ReadOnly([string]$cmd){ $c=$cmd.Trim().ToLowerInvariant(); if($c -match '[;&|]' -or $c.Contains([Environment]::NewLine) -or $c.Contains('$(')){return $false}; foreach($x in @('git status','git diff','git log','git show','git branch --show-current','git rev-parse','git ls-files','pwd','ls','dir ','get-childitem','get-content','type ','cat ','head ','tail ','grep ','rg ','findstr ','sha256sum','shasum','certutil -hashfile','pytest --collect-only')){if($c.StartsWith($x)){return $true}}; return $false }
function Cmd-Mutating([string]$cmd){ $c=$cmd.ToLowerInvariant(); $patterns=@('\bgit\s+(commit|push|merge|rebase|reset|checkout|switch|clean|add|rm|mv)\b','\b(rm|del|erase|rmdir|mv|move|cp|copy|touch|mkdir|chmod|chown)\b','\bfind\b.*\b-delete\b','\b(remove-item|set-content|add-content|out-file|new-item|copy-item|move-item|rename-item|clear-content)\b','\bsed\s+-i\b','\btee\b','>>|(?<![<])>(?!>)','\b(npm|pnpm|yarn)\s+(install|add|remove|update|publish)\b','\b(pip|uv)\s+(install|uninstall)\b','\b(apt|apt-get|dnf|yum|brew)\s+(install|remove|upgrade)\b','\b(docker|kubectl|helm|terraform)\b.*\b(apply|delete|destroy|push|create|patch|replace|rollout)\b'); foreach($p in $patterns){if($c -match $p){return $true}}; return $false }
$stateExists = Test-Path $statePath
$state = if($stateExists){ Read-Json $statePath ([pscustomobject]@{}) } else { [pscustomobject]@{} }
$event = if($data.hook_event_name){[string]$data.hook_event_name}else{'Unknown'}
if($stateExists){ New-Item -ItemType Directory -Force -Path (Split-Path -Parent $auditPath)|Out-Null; @{at=(Now-Iso);event=$event;session=$data.session_id}|ConvertTo-Json -Compress|Add-Content $auditPath -Encoding utf8 }
if($event -eq 'SessionStart'){
  if($stateExists){$open=@($state.mandatoryOpenClaims).Count;$ctx="Agent Workflow durable state exists at $statePath. Active phase='$($state.phase)', objective='$($state.activeObjective)', open mandatory claims=$open. Re-enter from durable state before inferring completion or next steps from chat history."}
  else {$ctx='No .agent-workflow/state.json exists. Stay file-system-clean for a compact read-only answer. If the task enters the normal branch and durable state is warranted, initialize .agent-workflow/ from the Agent Workflow state templates before delegation, external actions, correction cycles, or long/multi-objective work.'}
  Emit @{hookSpecificOutput=@{hookEventName='SessionStart';additionalContext=$ctx}}; exit 0
}
if($event -eq 'PreToolUse'){
  if(-not $stateExists){Emit @{hookSpecificOutput=@{hookEventName='PreToolUse';permissionDecision='allow'}};exit 0}
  $phase=([string]$state.phase).ToLowerInvariant(); $tool=[string]$data.tool_name; $auditPhases=@('root-cause-challenge','root_cause_challenge','pre-action-audit','pre_action_audit','early-audit','early_audit','final-audit','final_audit'); $inAudit=$auditPhases -contains $phase
  if($inAudit -and (Tool-IsWrite $tool)){Emit @{hookSpecificOutput=@{hookEventName='PreToolUse';permissionDecision='deny';permissionDecisionReason="Agent Workflow phase $phase is read-only; candidate/target edits are forbidden during audit."}};exit 0}
  $cmd=Get-CommandText $data.tool_input
  if($inAudit -and $cmd){if(Cmd-Mutating $cmd){Emit @{hookSpecificOutput=@{hookEventName='PreToolUse';permissionDecision='deny';permissionDecisionReason="Mutating terminal command blocked during read-only audit phase $phase."}};exit 0};if(-not (Cmd-ReadOnly $cmd)){Emit @{hookSpecificOutput=@{hookEventName='PreToolUse';permissionDecision='ask';permissionDecisionReason="Audit phase $phase: terminal command is not proven read-only; manual approval required."}};exit 0}}
  Emit @{hookSpecificOutput=@{hookEventName='PreToolUse';permissionDecision='allow'}};exit 0
}
if($event -eq 'SubagentStart'){
  if($stateExists){$jobs=Read-Json $jobsPath ([pscustomobject]@{jobs=[pscustomobject]@{}}); if(-not $jobs.jobs){$jobs|Add-Member -NotePropertyName jobs -NotePropertyValue ([pscustomobject]@{}) -Force}; $aid=if($data.agent_id){[string]$data.agent_id}else{'unknown'}; $rec=[pscustomobject]@{agentType=$data.agent_type;status='running';startedAt=(Now-Iso)}; $jobs.jobs|Add-Member -NotePropertyName $aid -NotePropertyValue $rec -Force; Write-Json $jobsPath $jobs}
  Emit @{hookSpecificOutput=@{hookEventName='SubagentStart';additionalContext='This VS Code subagent invocation is stateless. Follow only the supplied invocation lease and role boundary; do not assume prior attempts.'}};exit 0
}
if($event -eq 'SubagentStop'){if($stateExists){$jobs=Read-Json $jobsPath ([pscustomobject]@{jobs=[pscustomobject]@{}});if(-not $jobs.jobs){$jobs|Add-Member -NotePropertyName jobs -NotePropertyValue ([pscustomobject]@{}) -Force};$aid=if($data.agent_id){[string]$data.agent_id}else{'unknown'};$p=$jobs.jobs.PSObject.Properties[$aid];if($p){$rec=$p.Value;$rec.status='completed';$rec|Add-Member -NotePropertyName stoppedAt -NotePropertyValue (Now-Iso) -Force}else{$rec=[pscustomobject]@{agentType=$data.agent_type;status='completed';stoppedAt=(Now-Iso)};$jobs.jobs|Add-Member -NotePropertyName $aid -NotePropertyValue $rec -Force};Write-Json $jobsPath $jobs};Emit @{continue=$true};exit 0}
if($event -eq 'PreCompact'){if($stateExists){$ck=Join-Path $stateDir 'checkpoints';New-Item -ItemType Directory -Force -Path $ck|Out-Null;$stamp=(Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ');Copy-Item $statePath (Join-Path $ck "state-$stamp.json") -Force};Emit @{continue=$true};exit 0}
if($event -eq 'Stop'){$open=if($stateExists){@($state.mandatoryOpenClaims).Count}else{0};if($open -gt 0){Emit @{continue=$true;systemMessage="Agent Workflow stopped with $open mandatory claim(s) still open. Do not report completion unless resolved or covered by explicit user-approved exceptions."};exit 0};Emit @{continue=$true};exit 0}
Emit @{continue=$true}
