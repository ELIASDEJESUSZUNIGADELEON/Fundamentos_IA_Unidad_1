$ErrorActionPreference = 'Stop'
$taskWorkspace = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..\..')).Path
$taskTools = Join-Path $taskWorkspace '.herramientas-u1'
$env:OLLAMA_MODELS = Join-Path $taskTools 'modelos'
$env:OLLAMA_HOST = '127.0.0.1:11435'
$env:OLLAMA_CONTEXT_LENGTH = '8192'
$env:OLLAMA_NUM_PARALLEL = '1'
try {
    $taskVersion = Invoke-RestMethod -Uri 'http://127.0.0.1:11435/api/version' -TimeoutSec 2
    Write-Output "Ollama ya responde: $($taskVersion.version)"
} catch {
    Start-Process -FilePath (Join-Path $taskTools 'ollama\ollama.exe') -ArgumentList 'serve' -WindowStyle Hidden -RedirectStandardOutput (Join-Path $taskTools 'ollama-servidor.txt') -RedirectStandardError (Join-Path $taskTools 'ollama-servidor-error.txt')
    Write-Output 'Ollama iniciado en segundo plano en 127.0.0.1:11435.'
}
