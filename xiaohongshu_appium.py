"""
小红书自动发布脚本 - 使用Appium控制手机
"""
from appium import webdriver
import time
import subprocess

# 配置
CAPS = {
    'platformName': 'Android',
    'deviceName': 'emxghabe8dfi69kn',
    'appPackage': 'com.xingin.xhs',
    'appActivity': '.index.v2.IndexActivityV2',
    'noReset': True,
    'fullReset': False,
    'adbExecTimeout': 50000,
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
    print("小红书自动发布开始")
    print("="*50)
    
    # 启动Appium
    print("\n正在启动Appium服务...")
    appium_process = subprocess.Popen(
        ['appium', '-a', '127.0.0.1', '-p', '4723'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(5)  # 等待Appium启动
    
    try:
        # 连接手机
        print("正在连接小红书...")
        driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', CAPS)
        time.sleep(5)
        
        print("小红书已打开!")
        
        # 获取屏幕尺寸
        size = driver.get_window_size()
        width = size['width']
        height = size['height']
        print(f"屏幕尺寸: {width}x{height}")
        
        # 1. 点击首页的加号按钮发布笔记
        print("\n步骤1: 点击发布按钮...")
        # 小红书的发布按钮通常在底部中间
        driver.tap([(width//2, height - 150)])
        time.sleep(3)
        
        # 2. 选择图文发布
        print("步骤2: 选择图文...")
        # 尝试点击"图文"选项
        driver.tap([(width//2, height//2)])
        time.sleep(3)
        
        # 3. 选择图片
        print("步骤3: 选择图片...")
        # 点击相册按钮
        driver.tap([(width//2, height - 300)])
        time.sleep(2)
        
        # 4. 选择我们上传的图片（通常在图片选择界面）
        # 点击第一张图片
        driver.tap([(width//4, height//2)])
        time.sleep(1)
        driver.tap([(width//4*2, height//2)])
        time.sleep(1)
        driver.tap([(width//4*3, height//2)])
        time.sleep(1)
        driver.tap([(width//4, height//2 + 200)])
        time.sleep(1)
        
        # 5. 确认选择
        print("步骤4: 确认选择...")
        driver.tap([(width - 100, height - 100)])  # 确定按钮
        time.sleep(3)
        
        # 6. 填写标题
        print("步骤5: 填写标题...")
        # 点击标题输入框（通常在顶部）
        title_input = driver.find_element_by_id("com.xingin.xhs:id/title")
        title_input.send_keys(TITLE)
        time.sleep(2)
        
        # 7. 填写正文
        print("步骤6: 填写正文...")
        content_input = driver.find_element_by_id("com.xingin.xhs:id/content")
        content_input.send_keys(CONTENT)
        time.sleep(2)
        
        # 8. 发布
        print("步骤7: 发布笔记...")
        driver.tap([(width//2, height - 100)])  # 发布按钮
        time.sleep(5)
        
        print("\n" + "="*50)
        print("✅ 发布完成！")
        print("="*50)
        
    except Exception as e:
        print(f"出错: {e}")
        print("\n请手动完成剩余操作")
        
    finally:
        print("\n按回车键退出...")
        input()
        driver.quit()
        appium_process.terminate()

if __name__ == "__main__":
    main()
