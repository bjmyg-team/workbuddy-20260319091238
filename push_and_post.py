#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书自动发布脚本
手机: 小米 21091116UC, Android 13
小红书包名: com.xingin.xhs
"""

import subprocess
import os
import time
import glob

# ===== 第一步: 推送图片到手机 =====
images_dir = r"C:\Users\Administrator\WorkBuddy\20260319091238\images"
image_files = sorted(glob.glob(os.path.join(images_dir, "*.png")))

print(f"找到 {len(image_files)} 张图片:")
for f in image_files:
    print(f"  {os.path.basename(f)}")

phone_paths = []
for i, img in enumerate(image_files):
    dest = f"/sdcard/Pictures/xhs_post_{i+1:02d}.png"
    print(f"\n推送图片 {i+1}/{len(image_files)}: {os.path.basename(img)} -> {dest}")
    result = subprocess.run(
        ["adb", "push", img, dest],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"  ✅ 成功")
        phone_paths.append(dest)
    else:
        print(f"  ❌ 失败: {result.stderr}")

# 刷新媒体库
print("\n刷新手机媒体库...")
subprocess.run(["adb", "shell", "am", "broadcast", "-a", 
                "android.intent.action.MEDIA_SCANNER_SCAN_FILE",
                "-d", "file:///sdcard/Pictures/"], capture_output=True)
time.sleep(2)

print(f"\n✅ 已推送 {len(phone_paths)} 张图片到手机")
print("图片保存在: /sdcard/Pictures/xhs_post_01.png ~ xhs_post_04.png")

# ===== 第二步: 启动 Appium 服务 =====
print("\n启动 Appium 服务...")
appium_proc = subprocess.Popen(
    ["appium", "-a", "127.0.0.1", "-p", "4723", "--allow-cors"],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    creationflags=subprocess.CREATE_NO_WINDOW
)
print("等待 Appium 启动 (8秒)...")
time.sleep(8)

# ===== 第三步: Appium 自动化发布 =====
try:
    from appium import webdriver
    from appium.options.android import UiAutomator2Options

    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "emxghabe8dfi69kn"
    options.platform_version = "13"
    options.app_package = "com.xingin.xhs"
    options.app_activity = ".index.activity.MainActivity"
    options.no_reset = True          # 保留登录状态
    options.auto_grant_permissions = True
    options.new_command_timeout = 120
    options.uiautomator2_server_launch_timeout = 60000

    print("\n连接 Appium...")
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    print("✅ 连接成功！小红书已启动")
    time.sleep(5)

    from appium.webdriver.common.appiumby import AppiumBy
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    wait = WebDriverWait(driver, 20)

    # 点击底部"+"发布按钮
    print("\n寻找发布按钮...")
    try:
        # 尝试多种方式找到发布按钮
        publish_btn = None
        
        # 方式1: 通过content-desc
        try:
            publish_btn = wait.until(EC.presence_of_element_located(
                (AppiumBy.ACCESSIBILITY_ID, "发布")
            ))
            print("通过accessibility找到发布按钮")
        except:
            pass
        
        # 方式2: 通过资源ID
        if not publish_btn:
            try:
                publish_btn = driver.find_element(AppiumBy.ID, "com.xingin.xhs:id/tab_add")
                print("通过ID找到发布按钮")
            except:
                pass
        
        # 方式3: 通过XPath找底部加号
        if not publish_btn:
            try:
                publish_btn = driver.find_element(
                    AppiumBy.XPATH, 
                    '//*[@content-desc="发布" or @text="+" or contains(@resource-id,"add") or contains(@resource-id,"publish")]'
                )
                print("通过XPath找到发布按钮")
            except:
                pass
        
        # 方式4: 截图调试
        if not publish_btn:
            print("未找到按钮，截图查看当前界面...")
            driver.save_screenshot(r"C:\Users\Administrator\WorkBuddy\20260319091238\debug_screen.png")
            print("截图已保存: debug_screen.png")
            
            # 获取页面源码
            page_source = driver.page_source
            with open(r"C:\Users\Administrator\WorkBuddy\20260319091238\debug_page.xml", "w", encoding="utf-8") as f:
                f.write(page_source)
            print("页面源码已保存: debug_page.xml")
            
            print("\n请查看截图，手动告知我发布按钮的位置")
            driver.quit()
            appium_proc.terminate()
            exit(1)
        
        publish_btn.click()
        print("✅ 点击了发布按钮")
        time.sleep(3)

    except Exception as e:
        print(f"找发布按钮出错: {e}")
        driver.save_screenshot(r"C:\Users\Administrator\WorkBuddy\20260319091238\debug_screen.png")
        driver.quit()
        appium_proc.terminate()
        exit(1)

    # 选择"图文"选项
    print("选择图文发布...")
    try:
        # 截图看看当前状态
        driver.save_screenshot(r"C:\Users\Administrator\WorkBuddy\20260319091238\after_plus.png")
        
        # 找图文按钮
        tuwen_btn = None
        try:
            tuwen_btn = wait.until(EC.presence_of_element_located(
                (AppiumBy.XPATH, '//*[@text="图文" or @content-desc="图文"]')
            ))
        except:
            pass
        
        if tuwen_btn:
            tuwen_btn.click()
            print("✅ 选择了图文")
        else:
            print("未找到图文按钮，截图已保存")
            
        time.sleep(3)
        
    except Exception as e:
        print(f"选择图文出错: {e}")

    # 保存截图用于调试
    driver.save_screenshot(r"C:\Users\Administrator\WorkBuddy\20260319091238\step_tuwen.png")
    
    # 选择图片
    print("选择图片...")
    try:
        # 找相册/选择图片按钮
        select_photo_btn = None
        
        selectors = [
            (AppiumBy.XPATH, '//*[@text="从相册选择" or @text="相册" or @text="从手机相册选择"]'),
            (AppiumBy.XPATH, '//*[contains(@text,"相册") or contains(@content-desc,"相册")]'),
            (AppiumBy.XPATH, '//*[contains(@resource-id,"photo") or contains(@resource-id,"album") or contains(@resource-id,"gallery")]'),
        ]
        
        for by, selector in selectors:
            try:
                select_photo_btn = driver.find_element(by, selector)
                print(f"找到相册按钮: {selector[:50]}")
                break
            except:
                continue
        
        if not select_photo_btn:
            driver.save_screenshot(r"C:\Users\Administrator\WorkBuddy\20260319091238\step_select_photo.png")
            print("未找到相册按钮，截图已保存到 step_select_photo.png")
        else:
            select_photo_btn.click()
            time.sleep(2)
            
    except Exception as e:
        print(f"选择图片出错: {e}")
    
    driver.save_screenshot(r"C:\Users\Administrator\WorkBuddy\20260319091238\step_album.png")
    print("\n当前步骤截图已保存")
    print("请检查以下截图文件查看进度:")
    print("  debug_screen.png  - 初始界面")
    print("  after_plus.png    - 点击+后")
    print("  step_tuwen.png    - 选择图文后")
    print("  step_album.png    - 当前状态")
    
    # 输出当前页面所有可点击元素
    page_source = driver.page_source
    with open(r"C:\Users\Administrator\WorkBuddy\20260319091238\current_page.xml", "w", encoding="utf-8") as f:
        f.write(page_source)
    print("  current_page.xml  - 当前页面元素")
    
    input("\n按Enter继续或Ctrl+C退出...")
    
    driver.quit()
    
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保已安装: pip install Appium-Python-Client")
except Exception as e:
    print(f"Appium错误: {e}")
    import traceback
    traceback.print_exc()
finally:
    try:
        appium_proc.terminate()
        print("\nAppium 服务已关闭")
    except:
        pass
