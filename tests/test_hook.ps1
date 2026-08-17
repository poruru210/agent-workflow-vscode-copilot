$ErrorActionPreference = 'Stop'
$root = Join-Path $env:RUNNER_TEMP ('agent-workflow-hook-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Force -Path (Join-Path $root '.agent-workflow') | Out-Null
@{ phase='early-audit'; activeObjective='OBJ-1'; mandatoryOpenClaims=@('C1') } |
  ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 (Join-Path $root '.agent-workflow/state.json')
$hook = Join-Path $env:GITHUB_WORKSPACE 'workflow/agent-workflow/scripts/workflow_hook.ps1'

$tokens = $null
$parseErrors = $null
[void][System.Management.Automation.Language.Parser]::ParseFile($hook, [ref]$tokens, [ref]$parseErrors)
if ($parseErrors.Count -gt 0) {
  $message = ($parseErrors | ForEach-Object { $_.Message }) -join '; '
  Write-Host "::error title=PowerShell hook parse failure::$message"
  throw $message
}

function Invoke-Hook([string]$payload) {
  $psi = [System.Diagnostics.ProcessStartInfo]::new()
  $psi.FileName = (Get-Command pwsh).Source
  [void]$psi.ArgumentList.Add('-NoProfile')
  [void]$psi.ArgumentList.Add('-File')
  [void]$psi.ArgumentList.Add($hook)
  $psi.UseShellExecute = $false
  $psi.RedirectStandardInput = $true
  $psi.RedirectStandardOutput = $true
  $psi.RedirectStandardError = $true

  $process = [System.Diagnostics.Process]::new()
  $process.StartInfo = $psi
  [void]$process.Start()
  $process.StandardInput.Write($payload)
  $process.StandardInput.Close()
  $stdout = $process.StandardOutput.ReadToEnd()
  $stderr = $process.StandardError.ReadToEnd()
  $process.WaitForExit()

  if ($process.ExitCode -ne 0) {
    $message = "hook process failed with exit code $($process.ExitCode); stderr=$stderr; stdout=$stdout"
    Write-Host "::error title=PowerShell hook process failure::$message"
    throw $message
  }
  try {
    return ($stdout | ConvertFrom-Json)
  } catch {
    $message = "hook returned invalid JSON; stdout=$stdout; stderr=$stderr; error=$($_.Exception.Message)"
    Write-Host "::error title=PowerShell hook JSON failure::$message"
    throw $message
  }
}

$payload = @{ hook_event_name='PreToolUse'; cwd=$root; session_id='ci'; tool_name='edit'; tool_input=@{path='x.txt'} } | ConvertTo-Json -Depth 10 -Compress
$r = Invoke-Hook $payload
if ($r.hookSpecificOutput.permissionDecision -ne 'deny') {
  $message = "expected edit denial in early-audit; got: $($r | ConvertTo-Json -Depth 10 -Compress)"
  Write-Host "::error title=PowerShell hook edit-denial failure::$message"
  throw $message
}

$payload = @{ hook_event_name='PreToolUse'; cwd=$root; session_id='ci'; tool_name='execute'; tool_input=@{command='git status'} } | ConvertTo-Json -Depth 10 -Compress
$r = Invoke-Hook $payload
if ($r.hookSpecificOutput.permissionDecision -ne 'allow') {
  $message = "expected git status allow in early-audit; got: $($r | ConvertTo-Json -Depth 10 -Compress)"
  Write-Host "::error title=PowerShell hook read-only failure::$message"
  throw $message
}

Write-Host 'PowerShell hook behavior PASS'
