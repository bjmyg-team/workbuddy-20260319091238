@echo off
chcp 65001 >nul
set ANDROID_HOME=C:\Android\android-sdk
set ANDROID_SDK_ROOT=C:\Android\android-sdk
echo Starting Appium with ANDROID_HOME=%ANDROID_HOME%
start /b cmd /c "set ANDROID_HOME=C:\Android\android-sdk && set ANDROID_SDK_ROOT=C:\Android\android-sdk && appium -a 127.0.0.1 -p 4723 --allow-cors"
echo Appium starting...
timeout /t 8 /nobreak >nul
echo Done!
