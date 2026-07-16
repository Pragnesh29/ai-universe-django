@echo off
chcp 65001 >nul
title AI Universe — Deploy Script

echo.
echo ==========================================
echo   AI Universe — Deploy to GitHub + Server
echo ==========================================
echo.

:: Config
set SSH_KEY=C:\Users\pagup\Desktop\Code\Django\ssh-key-2026-07-15.key
set SERVER=ubuntu@157.151.152.144
set PROJECT_DIR=C:\Users\pagup\Desktop\Code\Django

:: Project folder mai jao
cd /d %PROJECT_DIR%

:: ----------------------------------------
:: STEP 1: Commit message lo
:: ----------------------------------------
echo Kya badlav kiya? (Commit message likhein):
set /p COMMIT_MSG=">> "

if "%COMMIT_MSG%"=="" (
    set COMMIT_MSG=Minor update
)

:: ----------------------------------------
:: STEP 2: GitHub pe push karo
:: ----------------------------------------
echo.
echo [1/3] GitHub pe push kar raha hoon...
echo.

git add .
git commit -m "%COMMIT_MSG%"
git push origin main

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] GitHub push fail hua! Check karo aur dobara try karo.
    pause
    exit /b 1
)

echo.
echo [✓] GitHub push successful!

:: ----------------------------------------
:: STEP 3: Server pe update karo
:: ----------------------------------------
echo.
echo [2/3] Server pe update deploy kar raha hoon...
echo.

:: SSH key permissions fix karo (Windows ke liye)
icacls "%SSH_KEY%" /inheritance:r /grant:r "%USERNAME%:R" >nul 2>&1

ssh -i "%SSH_KEY%" -o StrictHostKeyChecking=no %SERVER% "bash /home/ubuntu/ai-universe-django/update_server.sh"

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Server update fail hua! SSH check karo.
    pause
    exit /b 1
)

:: ----------------------------------------
:: STEP 4: Done!
:: ----------------------------------------
echo.
echo [3/3] Sab ho gaya!
echo.
echo ==========================================
echo   Deploy Complete!
echo   GitHub: https://github.com/Pragnesh29/ai-universe-django
echo   Live:   http://157.151.152.144
echo ==========================================
echo.
pause
