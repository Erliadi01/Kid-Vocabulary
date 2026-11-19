@echo off
title Let's Learn English: Jungle Adventure
echo ========================================================
echo  LET'S LEARN ENGLISH: JUNGLE ADVENTURE 🌴🦁
echo  Aplikasi Edukasi Anak Interaktif Bahasa Inggris
echo ========================================================
echo.
echo Menjalankan aplikasi langsung dari virtual environment...
"%~dp0venv\Scripts\python.exe" "%~dp0main.py"
if %errorlevel% neq 0 (
    echo.
    echo Terjadi kendala saat menjalankan aplikasi.
    pause
)
