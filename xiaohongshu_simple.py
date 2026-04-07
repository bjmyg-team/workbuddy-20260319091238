"""
小红书自动发布 - 简化版
"""
from appium import webdriver
import time

# 配置
CAPS = {
    'platformName': 'Android',
    'deviceName': 'emxghabe8dfi69kn',
    'appPackage': 'com.xingin.xhs',
    'appActivity': '.index.v2.IndexActivityV2',
    'noReset': True,
    'fullReset': False,
}

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
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', CAPS)
    time.sleep(5)
    
    print("小红书已打开!")
    size = driver.get_window_size()
    w, h = size['width'], size['height']
    
    # 1. 点击发布按钮（底部中间）
    print("点击发布按钮...")
    driver.tap([(w//2, h - 150)])
    time.sleep(3)
    
    # 2. 选择图文
    print("选择图文...")
    driver.tap([(w//2, h//2)])
    time.sleep(3)
    
    # 3. 打开相册
    print("打开相册...")
    driver.tap([(w//2, h - 300)])
    time.sleep(2)
    
    print("\n" + "="*50)
    print("已打开图片选择界面")
    print("请手动选择图片，然后我会帮你填写内容")
    print("="*50)
    
    input("选择完图片后按回车继续...")
    
    # 4. 填写标题（点击屏幕上方区域）
    print("填写标题...")
    driver.tap([(w//2, 200)])
    time.sleep(1)
    
    # 输入标题
    driver.set_value(driver.find_element_by_android_uiautomator(
        'new UiSelector().text("")'
    ), TITLE)
    time.sleep(2)
    
    print("\n✅ 脚本已完成基本操作")
    print("请在手机上完成以下步骤：")
    print("1. 确认图片已选择")
    print("2. 在标题框输入标题")
    print("3. 在正文框输入内容")
    print("4. 点击发布")
    
    driver.quit()

if __name__ == "__main__":
    main()
