# Builds VoiceDoc.exe (a small launcher for the tray app) and installs Start-menu + desktop shortcuts.
#   powershell -ExecutionPolicy Bypass -File scripts\build_app.ps1            # build + install shortcuts
#   powershell -ExecutionPolicy Bypass -File scripts\build_app.ps1 -Uninstall # remove shortcuts (notes/models kept)
param([switch]$Uninstall, [switch]$Startup)
$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$py = Join-Path $root ".venv\Scripts\python.exe"
$exe = Join-Path $root "VoiceDoc.exe"
$desktopLnk = Join-Path ([Environment]::GetFolderPath("Desktop")) "VoiceDoc.lnk"
$menuDir = Join-Path ([Environment]::GetFolderPath("Programs")) "VoiceDoc"
$startupLnk = Join-Path ([Environment]::GetFolderPath("Startup")) "VoiceDoc.lnk"

if ($Uninstall) {
    foreach ($p in @($desktopLnk, $menuDir, $startupLnk)) { if (Test-Path $p) { Remove-Item $p -Recurse -Force; "Removed $p" } }
    "Shortcuts removed. Notes, models and the project folder were not touched."
    exit 0
}

# 1. Icon (same microphone drawing as the tray icon)
New-Item -ItemType Directory -Force (Join-Path $root "assets") | Out-Null
$ico = Join-Path $root "assets\voicedoc.ico"
& $py -c "import sys; sys.path.insert(0, r'$root'); from voicedoc.desktop import _tray_image; _tray_image('#1e8e3e').save(r'$ico', sizes=[(16,16),(32,32),(48,48),(64,64)])"
if ($LASTEXITCODE -ne 0) { throw "icon generation failed" }

# 2. Build the launcher exe (build/ and dist/ are scratch)
$work = Join-Path $root ".cache\pyinstaller"
& $py -m PyInstaller --noconfirm --onefile --windowed --name VoiceDoc --icon $ico `
    --distpath (Join-Path $work "dist") --workpath (Join-Path $work "build") --specpath $work `
    (Join-Path $root "launcher\voicedoc_launcher.py")
if ($LASTEXITCODE -ne 0) { throw "PyInstaller failed" }
Copy-Item (Join-Path $work "dist\VoiceDoc.exe") $exe -Force
"Built $exe ($([math]::Round((Get-Item $exe).Length / 1MB, 1)) MB)"

# 3. Shortcuts: Start menu + desktop
$shell = New-Object -ComObject WScript.Shell
New-Item -ItemType Directory -Force $menuDir | Out-Null
$targets = @(
    @{ Path = (Join-Path $menuDir "VoiceDoc.lnk"); Args = ""; Desc = "Speak Tamil/Tanglish, get English text live" },
    @{ Path = (Join-Path $menuDir "VoiceDoc - type at cursor.lnk"); Args = "--cursor"; Desc = "Start in type-at-cursor mode" },
    @{ Path = $desktopLnk; Args = ""; Desc = "Speak Tamil/Tanglish, get English text live" }
)
if ($Startup) { $targets += @{ Path = $startupLnk; Args = ""; Desc = "VoiceDoc: starts in the tray with Windows" } }
foreach ($t in $targets) {
    $l = $shell.CreateShortcut($t.Path)
    $l.TargetPath = $exe
    $l.Arguments = $t.Args
    $l.WorkingDirectory = $root
    $l.IconLocation = $ico
    $l.Description = $t.Desc
    $l.Save()
    "Shortcut: $($t.Path)"
}
