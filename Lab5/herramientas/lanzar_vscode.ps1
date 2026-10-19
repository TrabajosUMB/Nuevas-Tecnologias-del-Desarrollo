# Abre una ventana de VS Code con un perfil aislado (en %TEMP%\lab5-vscode-datos), sin extensiones y con el puerto de depuración 9340,
# para tomar capturas reales del editor con el proyecto del laboratorio. No toca el perfil normal del usuario.
# Uso: powershell -File lanzar_vscode.ps1
$raiz = Split-Path -Parent $PSScriptRoot                                 # ...\Lab5
$proyecto = Join-Path $raiz 'proyecto'
$datos = Join-Path $env:TEMP 'lab5-vscode-datos'
$codigo = Join-Path $env:LOCALAPPDATA 'Programs\Microsoft VS Code\Code.exe'

# Perfil aislado con ajustes sobrios para que las capturas se lean bien en el informe.
New-Item -ItemType Directory -Force (Join-Path $datos 'User') | Out-Null
$ajustes = @'
{
  "workbench.startupEditor": "none",
  "workbench.colorTheme": "Default Light Modern",
  "workbench.tips.enabled": false,
  "workbench.welcomePage.walkthroughs.openOnInstall": false,
  "security.workspace.trust.enabled": false,
  "telemetry.telemetryLevel": "off",
  "update.mode": "none",
  "extensions.autoUpdate": false,
  "extensions.ignoreRecommendations": true,
  "editor.minimap.enabled": false,
  "editor.fontSize": 13,
  "editor.lineHeight": 19,
  "editor.renderLineHighlight": "none",
  "editor.cursorBlinking": "solid",
  "editor.occurrencesHighlight": "off",
  "editor.selectionHighlight": false,
  "editor.matchBrackets": "never",
  "editor.lightbulb.enabled": "off",
  "editor.fontFamily": "Consolas, 'Courier New', monospace",
  "editor.renderWhitespace": "none",
  "editor.guides.indentation": false,
  "editor.wordWrap": "off",
  "breadcrumbs.enabled": false,
  "window.commandCenter": false,
  "chat.disableAIFeatures": true,
  "workbench.secondarySideBar.defaultVisibility": "hidden",
  "git.enabled": false,
  "window.restoreWindows": "none"
}
'@
Set-Content -Path (Join-Path $datos 'User\settings.json') -Value $ajustes -Encoding UTF8

# Cierra una instancia previa con el mismo puerto de depuración.
Get-CimInstance Win32_Process -Filter "Name='Code.exe'" | Where-Object { $_.CommandLine -match 'remote-debugging-port=9340' } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
Start-Sleep -Seconds 1

$argumentos = @("--user-data-dir=`"$datos`"", '--remote-debugging-port=9340', '--new-window', '--skip-release-notes', '--skip-welcome', '--disable-extensions', "`"$proyecto`"")
$linea = "`"$codigo`" " + ($argumentos -join ' ')
$r = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{ CommandLine = $linea }
Write-Output "ReturnValue=$($r.ReturnValue) PID=$($r.ProcessId)"
Start-Sleep -Seconds 12
try { (Invoke-RestMethod 'http://127.0.0.1:9340/json/version').Browser } catch { Write-Output "CDP no responde: $_" }
