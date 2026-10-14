# Lanza un Edge headless desacoplado (WMI) con el puerto CDP 9335 y un perfil propio; se queda abierto entre comandos.
# Uso: powershell -File lanzar_edge.ps1
$edge = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
$perfil = Join-Path $env:TEMP 'remix-edge-perfil'
# Un Edge previo en el mismo puerto reutilizaría la sesión anterior: se cierra antes.
Get-CimInstance Win32_Process -Filter "Name='msedge.exe'" |
    Where-Object { $_.CommandLine -match 'remote-debugging-port=9335' } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
Start-Sleep -Seconds 1
Remove-Item -Recurse -Force $perfil -ErrorAction SilentlyContinue
$linea = "`"$edge`" --headless --disable-gpu --no-first-run --no-default-browser-check --window-size=1440,900 --remote-debugging-port=9335 --user-data-dir=`"$perfil`" about:blank"
$r = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{ CommandLine = $linea }
Write-Output "ReturnValue=$($r.ReturnValue) PID=$($r.ProcessId)"
Start-Sleep -Seconds 3
try { (Invoke-RestMethod 'http://127.0.0.1:9335/json/version').Browser } catch { Write-Output "CDP no responde: $_" }
