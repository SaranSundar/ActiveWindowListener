SET MyProcess=notepad.exe
ECHO "%MyProcess%"
TASKLIST | FINDSTR /I "%MyProcess%"
IF ERRORLEVEL 1 (start C:\Windows\System32\%MyProcess%)
timeout 5