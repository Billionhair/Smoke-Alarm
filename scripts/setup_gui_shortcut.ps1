$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $MyInvocation.MyCommand.Path
$gui = Join-Path $repo '..\gui'

Push-Location $gui
if (-not (Test-Path node_modules)) {
  npm install | Out-Null
} else {
  npm install | Out-Null
}
Pop-Location

$desktop = [Environment]::GetFolderPath('Desktop')
$target = Join-Path $repo 'start_gui.bat'
$shortcutPath = Join-Path $desktop 'Smoke Alarm GUI.lnk'
$wsh = New-Object -ComObject WScript.Shell
$shortcut = $wsh.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $target
$shortcut.WorkingDirectory = Split-Path $target
$shortcut.Save()
Write-Output "Created Windows shortcut at $shortcutPath"
