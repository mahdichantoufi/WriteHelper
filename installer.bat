@echo off
pip install pyperclip

echo Creation du raccourci sur le bureau...
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\WriteHelper.lnk'); $s.TargetPath = 'pythonw.exe'; $s.Arguments = '\"%~dp0gui.pyw\"'; $s.WorkingDirectory = '%~dp0'; $s.IconLocation = 'pythonw.exe,0'; $s.Save()"

echo.
echo Installation terminee ! Raccourci cree sur le bureau.
pause
