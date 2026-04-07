@echo off
chcp 65001 >nul
echo ==========================================
echo   美域高 - GitHub 归档备份脚本 v1.0
echo ==========================================
echo.

set BACKUP_DIR=C:\Users\Administrator\WorkBuddy\backups
set DATE_STR=%date:~0,4%-%date:~5,2%-%date:~8,2%
set TIME_STR=%time:~0,2%-%time:~3,2%-%time:~6,2%
set TIME_STR=%TIME_STR: =0%
set BACKUP_NAME=backup-%DATE_STR%-%TIME_STR%

echo [INFO] 创建备份目录...
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"
if not exist "%BACKUP_DIR%\%BACKUP_NAME%" mkdir "%BACKUP_DIR%\%BACKUP_NAME%"

echo [INFO] 复制项目文件...
xcopy "c:\Users\Administrator\WorkBuddy\20260319091238" "%BACKUP_DIR%\%BACKUP_NAME%" /E /I /Y /EXCLUDE:scripts\exclude.txt

echo [INFO] 创建归档...
cd "%BACKUP_DIR%"
powershell -command "Compress-Archive -Path '.\\%BACKUP_NAME%' -DestinationPath '.\\%BACKUP_NAME%.zip' -Force"
rmdir /S /Q "%BACKUP_DIR%\%BACKUP_NAME%"

echo.
echo ==========================================
echo   备份完成！
echo   备份位置：%BACKUP_DIR%\%BACKUP_NAME%.zip
echo ==========================================
pause
