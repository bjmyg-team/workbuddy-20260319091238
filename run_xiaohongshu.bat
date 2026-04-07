@echo off
echo 启动Appium服务...
start "Appium" cmd /k "appium -a 127.0.0.1 -p 4723 --allow-cors"

echo 等待Appium启动...
timeout /t 8 /nobreak

echo 设置环境变量并运行脚本...
set ANDROID_HOME=C:\Android\android-sdk
set ANDROID_SDK_ROOT=C:\Android\android-sdk
python xiaohongshu_v3.py

pause
