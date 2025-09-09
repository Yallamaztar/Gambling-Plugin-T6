@echo off

echo Copying .gsc scripts to %LOCALAPPDATA%\Plutonium\storage\t6\scripts\mp
xcopy /y .\scripts\mp\gsc-events.gsc "%LOCALAPPDATA%\Plutonium\storage\t6\scripts\mp\"
xcopy /y .\scripts\mp\gambling-ignore.gsc "%LOCALAPPDATA%\Plutonium\storage\t6\scripts\mp\"

echo:
echo Setting up environment variables...
echo.

REM IW4M/IW4MAdmin Configuration (REQUIRED)
if not defined IW4M_URL (
    echo Please set IW4M_URL environment variable
    echo Example: set IW4M_URL=http://127.0.0.1:1624
    pause
    exit /b 1
)

if not defined IW4M_ID (
    echo Please set IW4M_ID environment variable
    echo Example: set IW4M_ID=193231601884988
    pause
    exit /b 1
)

if not defined IW4M_HEADER (
    echo Please set IW4M_HEADER environment variable
    echo Example: set IW4M_HEADER=.AspNetCore.Cookies=YOUR_COOKIE_HERE
    pause
    exit /b 1
)

REM Optional: Discord Bot Configuration
if not defined BOT_TOKEN (
    echo BOT_TOKEN not set - Discord bot will be disabled
    echo To enable: set BOT_TOKEN=your_discord_bot_token
)

REM Optional: API Configuration
if not defined API_ENABLED (
    echo API_ENABLED not set - API will be disabled
    echo To enable: set API_ENABLED=true
    echo API_HOST=0.0.0.0
    echo API_PORT=5000
    echo API_DEBUG=false
    echo API_ADMIN_KEY=your_secure_admin_key
)

echo:
echo Configuration loaded successfully!
echo.

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
