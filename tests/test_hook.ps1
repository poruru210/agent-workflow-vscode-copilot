$ErrorActionPreference = 'Stop'
$root = Join-Path $env:RUNNER_TEMP ('agent-workflow-hook-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Force -Path (Join-Path $root '.agent-workflow') | Out-Null
@{ phase='early-audit'; activeObjective='OBJ-1'; mandatoryOpenClaims=@('C1') } |
  ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 (Join-Path $root '.agent-workflow/state.json')
$hook = Join-Path $env:GITHUB_WORKSPACE 'workflow/agent-workflow/scripts/workflow_hook.ps1'

function Invoke-Hook([string]$payload) {
  $output = $payload | & pwsh -NoProfile -File $hook
  if ($LASTEXITCODE -ne 0) { throw "hook process failed with exit code $LASTEXITCODE" }
  return ($output | ConvertFrom-Json)
}

$payload = @{ hook_event_name='PreToolUse'; cwd=$root; session_id='ci'; tool_name='edit'; tool_input=@{path='x.txt'} } | ConvertTo-Json -Depth 10 -Compress
$r = Invoke-Hook $payload
if ($r.hookSpecificOutput.permissionDecision -ne 'deny') { throw "expected edit denial in early-audit; got: $($r | ConvertTo-Json -Depth 10 -Compress)" }

$payload = @{ hook_event_name='PreToolUse'; cwd=$root; session_id='ci'; tool_name='execute'; tool_input=@{command='git status'} } | ConvertTo-Json -Depth 10 -Compress
$r = Invoke-Hook $payload
if ($r.hookSpecificOutput.permissionDecision -ne 'allow') { throw "expected git status allow in early-audit; got: $($r | ConvertTo-Json -Depth 10 -Compress)" }

Write-Host 'PowerShell hook behavior PASS'
