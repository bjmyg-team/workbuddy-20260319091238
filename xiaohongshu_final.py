"""
小红书自动发布 - 最终版
"""
from appium import webdriver
from appium.options.android import UiAutomator2Options
import time

# 配置
options = UiAutomator2Options()
options.platform_name = 'Android'
options.device_name = 'emxghabe8dfi69kn'
options.app_package = 'com.xingin.xhs'
options.app_activity = '.index.v2.IndexActivityV2'
options.no_reset = True

TITLE = "中小企业必看！企业资质申报全攻略"
CONTENT = """3分钟搞懂资质申报，轻松拿下项目门槛👇

📋 常见资质类型：
• 营业执照、税务登记（必备）
• ISO认证（招投标加分）
• 高新企业（税收优惠）
• 创新型企业（政府补贴）

📝 申报流程：
1. 了解需求
2. 准备材料
3. 提交申请
4. 审核评审
5. 领取证书

💡 为什么找代办？
• 省时省力
• 通过率更高
• 安全可靠

#企业资质 #申报指南 #创业必看"""

def main():
    print("="*50)
    print("小红书自动发布")
    print("="*50)
    
    # 连接手机
    print("正在连接小红书...")
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', options=options)
    time.sleep(5)
    
    print("✅ 小红书已打开!")
    size = driver.get_window_size()
    w, h = size['width'], size['height']
    print(f"屏幕尺寸: {w}x{h}")
    
    # 1. 点击发布按钮
    print("\n步骤1: 点击发布按钮...")
    driver.tap([(w//2, h - 150)])
    time.sleep(3)
    
    # 2. 选择图文
    print("步骤2: 选择图文...")
    driver.tap([(w//2, h//2)])
    time.sleep(3)
    
    # 3. 打开相册
    print("步骤3: 打开相册...")
    driver.tap([(w//2, h - 300)])
    time.sleep(2)
    
    print("\n" + "="*50)
    print("已打开图片选择界面")
    print("请手动选择图片后告诉我")
    print("="*50)
    
    input("\n选择完图片后按回车继续...")
    
    # 4. 填写标题
    print("\n步骤4: 填写标题...")
    try:
        # 尝试找到标题输入框
        title_elem = driver.find_element("id", "com.xingin.xhs:id/edt_title")
        title_elem.send_keys(TITLE)
        print("✅ 标题已填写")
    except:
        print("⚠️ 无法自动填写标题，请手动填写")
    
    time.sleep(2)
    
    # 5. 填写正文
    print("步骤5: 填写正文...")
    try:
        content_elem = driver.find_element("id", "com.xingin.xhs:id/edt_content")
        content_elem.send_keys(CONTENT)
        print("✅ 正文已填写")
    except:
        print("⚠️ 无法自动填写正文，请手动填写")
    
    time.sleep(2)
    
    print("\n" + "="*50)
    print("✅ 内容已填写完毕!")
    print("请检查并点击发布按钮")
    print("="*50)
    
    input("\n发布完成后按回车退出...")
    driver.quit()
    print("\n发布成功！🎉")

if __name__ == "__main__":
    main()
