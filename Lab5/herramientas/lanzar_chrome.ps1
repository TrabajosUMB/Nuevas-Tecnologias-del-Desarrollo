# Lanza Google Chrome desacoplado (WMI) con el puerto de depuración 9336 y un perfil propio. Chrome sirve el frontend de DevTools desde su propio
# paquete (http://127.0.0.1:9336/devtools/inspector.html), de modo que el panel Application se puede abrir y capturar sin salir a internet.
# Uso: powershell -File lanzar_chrome.ps1 [-Cabeza]   (-Cabeza abre una ventana visible en lugar de headless)
param([switch]$Cabeza)
$chrome = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
$perfil = Join-Path $env:TEMP 'lab5-chrome-perfil'
Get-CimInstance Win32_Process -Filter "Name='chrome.exe'" |
    Where-Object { $_.CommandLine -match 'remote-debugging-port=9336' } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
Start-Sleep -Seconds 1
Remove-Item -Recurse -Force $perfil -ErrorAction SilentlyContinue
$modo = if ($Cabeza) { '' } else { '--headless=new' }
$linea = "`"$chrome`" $modo --disable-gpu --no-first-run --no-default-browser-check --disable-extensions --window-size=1400,900 " +
         "--remote-debugging-port=9336 --remote-allow-origins=* --user-data-dir=`"$perfil`" about:blank"
$r = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{ CommandLine = $linea }
Write-Output "ReturnValue=$($r.ReturnValue) PID=$($r.ProcessId)"
Start-Sleep -Seconds 3
try { (Invoke-RestMethod 'http://127.0.0.1:9336/json/version').Browser } catch { Write-Output "CDP no responde: $_" }
