SET MyProcess=flair.exe
ECHO "%MyProcess%"
TASKLIST | FINDSTR /I "%MyProcess%"
IF ERRORLEVEL 1 (start %~dp0/%MyProcess%)
timeout 10