@echo off
setlocal

set PYTHON_DIR=%LOCALAPPDATA%\Python398
set PYTHON_EXE=%PYTHON_DIR%\python.exe

if exist "%PYTHON_DIR%" (
    "%PYTHON_EXE%" payload.py
    exit /b
)

for /f "delims=" %%P in ('where python 2^>nul') do set PYTHON_GLOBAL=%%P

if defined PYTHON_GLOBAL (
    echo Found Python in environment variables: %PYTHON_GLOBAL%
    "%PYTHON_GLOBAL%" embed.py
    exit /b
)

echo Error: Python installation not found!
exit /b 1