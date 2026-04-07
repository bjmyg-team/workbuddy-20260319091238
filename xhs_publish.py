# -*- coding: utf-8 -*-
# 小红书自动发布脚本 - 最终版
import sys
import os
import time
sys.stdout.reconfigure(encoding='utf-8')

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ====== 配置 ======
APPIUM_URL = "http://127.0.0.1:4723"
DEVICE_ID  = "emxghabe8dfi69kn"
ANDROID_VER = "13"
PKG  = "com.xingin.xhs"
ACT  = ".index.activity.MainActivity"
WD   = r"C:\Users\Administrator\WorkBuddy\20260319091238"

TITLE = "中小企业必看！企业资质申报全攻略"
BODY  = """3分钟搞懂资质申报，轻松拿下项目门槛

常见资质类型：
- 营业执照、税务登记（必备）
- ISO认证（招投标加分项）
- 高新企业认定（享税收优惠）
- 创新型企业（政府补贴加持）

申报全流程5步走：
1. 了解需求，明确目标资质
2. 准备材料，避免反复补件
3. 提交申请，专业团队把关
4. 审核评审，全程跟踪进度
5. 领取证书，企业资质到手

为什么找专业代办？
专业团队通过率高，省时省力更省心

#企业资质 #资质申报 #创业必看 #中小企业 #营业执照"""

# 手机上的图片路径
PHONE_IMAGES = [
    "/sdcard/Pictures/xhs_post_01.png",
    "/sdcard/Pictures/xhs_post_02.png",
    "/sdcard/Pictures/xhs_post_03.png",
    "/sdcard/Pictures/xhs_post_04.png",
]

SCREENSHOTS = os.path.join(WD, "screenshots")
os.makedirs(SCREENSHOTS, exist_ok=True)

def snap(driver, name):
    path = os.path.join(SCREENSHOTS, f"{name}.png")
    driver.save_screenshot(path)
    print(f"  [截图] {name}.png")
    return path

def find_el(driver, wait, selectors, label="元素"):
    for by, val in selectors:
        try:
            el = wait.until(EC.presence_of_element_located((by, val)))
            print(f"  [找到] {label}: {val[:60]}")
            return el
        except:
            continue
    return None

print("="*50)
print("小红书自动发布脚本启动")
print("="*50)

# ====== 连接 Appium ======
print("\n[1] 连接 Appium + 启动小红书...")
options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = DEVICE_ID
options.platform_version = ANDROID_VER
options.app_package = PKG
options.app_activity = ACT
options.no_reset = True
options.auto_grant_permissions = True
options.new_command_timeout = 300
options.uiautomator2_server_launch_timeout = 90000

driver = webdriver.Remote(APPIUM_URL, options=options)
wait = WebDriverWait(driver, 25)
print("  连接成功！等待小红书完全启动...")
time.sleep(6)
snap(driver, "01_launched")

# ====== 点击发布(+)按钮 ======
print("\n[2] 寻找并点击发布按钮...")
publish_selectors = [
    (AppiumBy.ACCESSIBILITY_ID, "发布"),
    (AppiumBy.ID, "com.xingin.xhs:id/tab_add"),
    (AppiumBy.XPATH, '//android.widget.LinearLayout[@content-desc="发布"]'),
    (AppiumBy.XPATH, '//*[@content-desc="发布"]'),
    (AppiumBy.XPATH, '//*[contains(@resource-id,"publish") or contains(@resource-id,"add_btn") or contains(@resource-id,"tab_add")]'),
]
pub_btn = find_el(driver, wait, publish_selectors, "发布按钮")
if not pub_btn:
    snap(driver, "02_no_publish_btn")
    # 尝试从页面源码找
    src = driver.page_source
    with open(os.path.join(WD, "page_home.xml"), "w", encoding="utf-8") as f:
        f.write(src)
    print("  [警告] 未找到发布按钮，已保存页面源码 page_home.xml")
    driver.quit()
    sys.exit(1)

pub_btn.click()
print("  点击发布按钮成功")
time.sleep(3)
snap(driver, "02_after_publish_click")

# ====== 选择"图文"类型 ======
print("\n[3] 选择图文发布类型...")
tuwen_selectors = [
    (AppiumBy.XPATH, '//*[@text="图文"]'),
    (AppiumBy.XPATH, '//*[@content-desc="图文"]'),
    (AppiumBy.XPATH, '//android.widget.TextView[@text="图文"]'),
]
tuwen_btn = find_el(driver, wait, tuwen_selectors, "图文按钮")
if tuwen_btn:
    tuwen_btn.click()
    print("  选择图文成功")
    time.sleep(3)
else:
    print("  [提示] 未找到图文按钮，可能已在图文上传页面")
snap(driver, "03_tuwen_selected")

# ====== 选择图片 ======
print("\n[4] 选择图片...")
# 查找相册/添加图片按钮
photo_selectors = [
    (AppiumBy.XPATH, '//*[contains(@text,"相册") or contains(@text,"选择图片") or contains(@text,"从相册")]'),
    (AppiumBy.XPATH, '//*[contains(@content-desc,"相册") or contains(@content-desc,"选择")]'),
    (AppiumBy.XPATH, '//*[contains(@resource-id,"album") or contains(@resource-id,"photo") or contains(@resource-id,"gallery")]'),
    (AppiumBy.XPATH, '//*[contains(@resource-id,"add_image") or contains(@resource-id,"select_photo")]'),
]

# 小红书通常在发布页直接显示相册，检查是否有图片格子可以点击
photo_grid_selectors = [
    (AppiumBy.XPATH, '//android.widget.GridView'),
    (AppiumBy.XPATH, '//android.widget.RecyclerView'),
    (AppiumBy.XPATH, '//*[contains(@resource-id,"recycler") or contains(@resource-id,"grid")]'),
]

src = driver.page_source
with open(os.path.join(WD, "page_publish.xml"), "w", encoding="utf-8") as f:
    f.write(src)
print("  已保存发布页面源码 page_publish.xml")

photo_btn = find_el(driver, wait, photo_selectors, "相册按钮")
if photo_btn:
    photo_btn.click()
    time.sleep(2)
    snap(driver, "04_album_opened")
else:
    print("  [提示] 未找到相册按钮，检查是否已显示图片网格")
    snap(driver, "04_check_grid")

# 查找并点击图片（从相册选图）
print("\n[5] 从相册中选择图片...")
# 小红书显示相册时，通常第一行是最新的图片
# 我们推送的图片应该在最前面
img_selectors = [
    (AppiumBy.XPATH, '(//android.widget.ImageView)[1]'),
    (AppiumBy.XPATH, '(//android.widget.CheckBox)[1]'),
    (AppiumBy.XPATH, '//*[contains(@resource-id,"thumbnail") or contains(@resource-id,"photo_item")]'),
]

# 尝试选择4张图片
selected = 0
for i in range(4):
    snap(driver, f"05_select_photo_{i+1}")
    img = find_el(driver, wait, img_selectors, f"第{i+1}张图片")
    if img:
        img.click()
        print(f"  选择第{i+1}张图片成功")
        selected += 1
        time.sleep(1)
    else:
        print(f"  [警告] 未找到第{i+1}张图片")
        break

print(f"  共选择了{selected}张图片")

# 点击"完成"/"下一步"
print("\n[6] 点击完成/下一步...")
next_selectors = [
    (AppiumBy.XPATH, '//*[@text="完成" or @text="下一步" or @text="确定"]'),
    (AppiumBy.XPATH, '//*[contains(@resource-id,"next") or contains(@resource-id,"done") or contains(@resource-id,"confirm")]'),
]
next_btn = find_el(driver, wait, next_selectors, "下一步按钮")
if next_btn:
    next_btn.click()
    time.sleep(3)
    snap(driver, "06_after_next")
else:
    snap(driver, "06_no_next_btn")
    print("  [警告] 未找到下一步按钮，已截图")

# ====== 填写标题 ======
print("\n[7] 填写标题...")
snap(driver, "07_before_title")
title_selectors = [
    (AppiumBy.XPATH, '//*[contains(@hint,"标题") or contains(@text,"标题")]'),
    (AppiumBy.XPATH, '//*[@hint="填写标题会有更多赞哦~" or @hint="添加标题"]'),
    (AppiumBy.XPATH, '//android.widget.EditText[1]'),
    (AppiumBy.ID, "com.xingin.xhs:id/et_title"),
]
title_input = find_el(driver, wait, title_selectors, "标题输入框")
if title_input:
    title_input.click()
    time.sleep(0.5)
    title_input.clear()
    title_input.send_keys(TITLE)
    print(f"  标题填写: {TITLE}")
    time.sleep(1)
else:
    print("  [警告] 未找到标题输入框")
    src = driver.page_source
    with open(os.path.join(WD, "page_editor.xml"), "w", encoding="utf-8") as f:
        f.write(src)
    print("  已保存编辑页源码 page_editor.xml")

# ====== 填写正文 ======
print("\n[8] 填写正文内容...")
body_selectors = [
    (AppiumBy.XPATH, '//*[contains(@hint,"正文") or contains(@hint,"内容")]'),
    (AppiumBy.XPATH, '//android.widget.EditText[2]'),
    (AppiumBy.XPATH, '//*[contains(@resource-id,"content") or contains(@resource-id,"body") or contains(@resource-id,"desc")]'),
]
body_input = find_el(driver, wait, body_selectors, "正文输入框")
if body_input:
    body_input.click()
    time.sleep(0.5)
    body_input.clear()
    # 用剪贴板方式输入（避免中文输入问题）
    import subprocess
    ps_cmd = f'Set-Clipboard -Value @"\n{BODY}\n"@'
    subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True)
    time.sleep(0.5)
    # 长按粘贴
    body_input.click()
    time.sleep(0.5)
    body_input.long_click(1)
    time.sleep(1)
    paste_btn = find_el(driver, wait, [(AppiumBy.XPATH, '//*[@text="粘贴"]')], "粘贴按钮")
    if paste_btn:
        paste_btn.click()
        print("  正文粘贴成功")
    else:
        # 直接输入
        driver.set_clipboard_text(BODY)
        time.sleep(0.3)
        driver.execute_script("mobile: shell", {"command": "input", "args": ["keyevent", "279"]})
        print("  正文发送成功")
    time.sleep(1)
else:
    print("  [警告] 未找到正文输入框")

snap(driver, "08_content_filled")

# ====== 点击发布 ======
print("\n[9] 点击最终发布按钮...")
final_publish_selectors = [
    (AppiumBy.XPATH, '//*[@text="发布笔记" or @text="发布" or @text="完成发布"]'),
    (AppiumBy.XPATH, '//*[contains(@resource-id,"publish") or contains(@resource-id,"post")]'),
]
final_btn = find_el(driver, wait, final_publish_selectors, "最终发布按钮")
if final_btn:
    snap(driver, "09_before_publish")
    final_btn.click()
    print("  点击发布成功！")
    time.sleep(5)
    snap(driver, "10_published")
    print("\n发布完成！")
else:
    snap(driver, "09_no_publish_btn")
    print("  [警告] 未找到发布按钮，请查看截图 09_no_publish_btn.png")

print("\n" + "="*50)
print("脚本执行完成")
print(f"截图保存在: {SCREENSHOTS}")
print("="*50)

driver.quit()
