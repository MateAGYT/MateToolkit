::  __  __       _          _    ____ 
:: |  \/  | __ _| |_ ___   / \  / ___|
:: | |\/| |/ _` | __/ _ \ / _ \| |  _ 
:: | |  | | (_| | ||  __// ___ \ |_| |
:: |_|  |_|\__,_|\__\___/_/   \_\____|
::
:: © Copyright 2026 - MateAG
:: All rights reserved. Any copy without 
:: consent of this code will be reported.
::

@echo off
title Mate-Toolkit - PLEASE BE PATIENT, THIS MAY TAKE A WHILE
setlocal

if "%~1"=="" (
    start "" "%~f0" -invisible
    exit /b
)

net session >nul 2>&1
if %errorlevel%==0 goto :code

powershell -Command "Start-Process -FilePath '%~f0' -ArgumentList '-invisible' -Verb RunAs"
exit /b

:code
cd /d "%~dp0"
pushd "%~dp0"
echo Installing dependencies...


:: for some reason, the following command doesn't work, so i had to add the individual dependencies as commands.
rem pip install -r requirements.txt


python -m pip install --upgrade pip
pip install PyQt6>=6.6.0
pip install requests>=2.31.0
pip install pillow>=10.0.0
pip install pyyaml>=6.0
pip install sqlmap>=1.8
pip install yt-dlp>=2024.1.1
pip install pyinstaller>=6.3.0

cls
echo Dependencies installed successfully!
echo.
echo Toolkit has been started!
py main.py