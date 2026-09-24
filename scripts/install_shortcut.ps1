# Creates a one-click "VoiceDoc" shortcut on the desktop (and optionally in Startup to launch with Windows).
# Usage:  powershell -ExecutionPolicy Bypass -File scripts\install_shortcut.ps1 [-Startup]
param([switch]$Startup)

$root = Split-Path -Parent $PSScriptRoot
$pythonw = Join-Path $root ".venv\Scripts\pythonw.exe"
if (-not (Test-Path $pythonw)) { throw "Not found: $pythonw (create the venv first)" }

$shell = New-Object -ComObject WScript.Shell
$targets = @([Environment]::GetFolderPath("Desktop"))
if ($Startup) { $targets += [Environment]::GetFolderPath("Startup") }

foreach ($dir in $targets) {
    $lnk = $shell.CreateShortcut((Join-Path $dir "VoiceDoc.lnk"))
    $lnk.TargetPath = $pythonw
    $lnk.Arguments = "-m voicedoc"
    $lnk.WorkingDirectory = $root
    $lnk.Description = "Live Tamil/Tanglish dictation into English Markdown (tray app)"
    $lnk.IconLocation = "$env:SystemRoot\System32\SHELL32.dll,168"   # microphone-like icon
    $lnk.Save()
    Write-Output "Created $($lnk.FullName)"
}
