@echo off
pip install pyperclip 2>nul

echo Recherche de Python...
for /f "delims=" %%i in ('where pythonw.exe 2^>nul') do set PYTHONW=%%i
for /f "delims=" %%i in ('where python.exe 2^>nul') do set PYTHONDIR=%%i

if "%PYTHONW%"=="" (
    echo Python introuvable dans le PATH. Recherche manuelle...
    for /d %%i in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
        if exist "%%i\pythonw.exe" (
            set PYTHONW=%%i\pythonw.exe
            set PYTHONDIR=%%i
        )
    )
)

if "%PYTHONW%"=="" (
    echo ERREUR: Python est introuvable. Veuillez installer Python depuis https://www.python.org
    pause
    exit /b 1
)

echo Python trouve : %PYTHONDIR%

echo Ajout de Python au PATH utilisateur...
for %%i in ("%PYTHONW%") do set PYTHONDIR=%%~dpi
set PYTHONSCRIPTS=%PYTHONDIR%Scripts
powershell -Command "$p = [Environment]::GetEnvironmentVariable('Path','User'); if ($p -notlike '*%PYTHONDIR%*') { [Environment]::SetEnvironmentVariable('Path', $p + ';%PYTHONDIR%;%PYTHONSCRIPTS%', 'User') }"

echo Installation de pyperclip...
"%PYTHONDIR%\python.exe" -m pip install pyperclip

echo Association de .pyw avec pythonw...
ftype Python.NoConFile="%PYTHONW%" "%%1" %%*
assoc .pyw=Python.NoConFile

echo Creation du raccourci sur le bureau...
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\WriteHelper.lnk'); $s.TargetPath = '%PYTHONW%'; $s.Arguments = '\"%~dp0gui.pyw\"'; $s.WorkingDirectory = '%~dp0'; $s.IconLocation = '%PYTHONW%,0'; $s.Save()"

echo.
echo Installation terminee ! Raccourci cree sur le bureau.
pause
