@echo off
chcp 65001 > nul
echo =====================================================
echo   UzRetro.uz - GitHub'ga Yuklash
echo =====================================================
echo.

cd /d C:\Users\QWERT\Desktop\uzretro.uz

echo Kodlar GitHub'ga yuborilmoqda...
echo Agar brauzerda ruxsat oynasi chiqsa, "Authorize" yoki tasdiqlashni bosing!
echo.

git push -u origin main

echo.
echo =====================================================
if %ERRORLEVEL% equ 0 (
    echo [MUVAFFAQIYATLI] Sayt kodi GitHub'ga yuklandi!
) else (
    echo [DIQQAT] Xatolik yuz berdi, iltimos yuqoridagi yozuvni tekshiring.
)
echo =====================================================
pause
