@echo off
pip install pyperclip

echo Association de .pyw avec pythonw...
for /f "delims=" %%i in ('where pythonw.exe 2^>nul') do set PYTHONW=%%i
if "%PYTHONW%"=="" (
    for /f "delims=" %%i in ('where python.exe') do set PYTHONW=%%i
)
ftype Python.NoConFile="%PYTHONW%" "%%1" %%*
assoc .pyw=Python.NoConFile

echo Creation du raccourci sur le bureau...
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\WriteHelper.lnk'); $s.TargetPath = '%PYTHONW%'; $s.Arguments = '\"%~dp0gui.pyw\"'; $s.WorkingDirectory = '%~dp0'; $s.IconLocation = '%PYTHONW%,0'; $s.Save()"

echo.
echo Installation terminee ! Raccourci cree sur le bureau.
pause
