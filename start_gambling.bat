@echo off

echo Copying .gsc scripts to %LOCALAPPDATA%\Plutonium\storage\t6\scripts\mp
xcopy /y .\scripts\mp\gsc-events.gsc "%LOCALAPPDATA%\Plutonium\storage\t6\scripts\mp\"
xcopy /y .\scripts\mp\gambling-ignore.gsc "%LOCALAPPDATA%\Plutonium\storage\t6\scripts\mp\"

:start
echo:
echo Starting Gambling Plugin
start "GamblingPlugin" cmd /k python main.py

:loop
echo:
echo If Plugin Crashed Press Any Key To Restart It
pause
taskkill /FI "WINDOWTITLE eq GamblingPlugin*" /T /F
goto start
goto loop
