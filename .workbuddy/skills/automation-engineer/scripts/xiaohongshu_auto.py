"""
小红书自动发布 - 使用pyautogui鼠标键盘自动化
"""
import pyautogui
import time
import os
import subprocess

# 配置
IMAGE_DIR = r"c:\Users\Administrator\WorkBuddy\20260319091238\images"
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

# 获取图片列表
images = [os.path.join(IMAGE_DIR, f) for f in os.listdir(IMAGE_DIR) if f.endswith('.png')]
print(f"找到 {len(images)} 张图片")

# 设置安全参数
pyautogui.PAUSE = 1  # 每次操作后等待1秒
pyautogui.FAILSAFE = True  # 鼠标移到左上角停止

def find_and_click(image_name, confidence=0.8):
    """查找图片并点击"""
    try:
        location = pyautogui.locateCenterOnScreen(image_name, confidence=confidence)
        if location:
            pyautogui.click(location)
            print(f"点击: {image_name}")
            return True
    except Exception as e:
        print(f"未找到: {image_name}")
    return False

def main():
    print("="*50)
    print("小红书自动发布开始")
    print("="*50)
    
    # 等待用户确认小红书已打开
    print("\n请确认小红书已打开并登录")
    print("准备好后按回车键继续...")
    input()
    
    print("\n开始自动化操作...")
    
    # 1. 点击发布按钮（需要用户在界面上找到位置）
    # 先获取屏幕尺寸
    screen_width, screen_height = pyautogui.size()
    print(f"屏幕尺寸: {screen_width}x{screen_height}")
    
    # 点击屏幕中央附近的发布按钮区域（小红书通常在底部中间）
    # 这是一个估计的位置，用户可能需要调整
    publish_x = screen_width // 2
    publish_y = screen_height - 100
    
    print(f"点击发布按钮位置: ({publish_x}, {publish_y})")
    pyautogui.click(publish_x, publish_y)
    time.sleep(2)
    
    # 选择图文
    print("点击图文选项...")
    pyautogui.click(publish_x, publish_y + 100)
    time.sleep(2)
    
    # 点击上传图片区域
    print("点击上传图片区域...")
    upload_x = screen_width // 2
    upload_y = screen_height // 2
    pyautogui.click(upload_x, upload_y)
    time.sleep(2)
    
    # 这里会打开文件选择对话框
    # 我们需要输入图片路径
    print("输入图片路径...")
    
    # 由于图片有多张，这里演示第一张
    if images:
        print(f"上传第一张图片: {images[0]}")
        pyautogui.write(images[0])
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(2)
    
    print("\n" + "="*50)
    print("已打开图片上传对话框")
    print("请手动完成以下操作:")
    print("1. 选择所有4张图片")
    print("2. 点击打开")
    print("="*50)
    
    input("完成后按回车继续...")
    
    # 填写标题
    print("填写标题...")
    pyautogui.write(TITLE)
    time.sleep(1)
    
    # 按Tab切换到正文
    pyautogui.press('tab')
    time.sleep(0.5)
    
    # 填写正文
    print("填写正文...")
    pyautogui.write(CONTENT)
    time.sleep(1)
    
    # 添加话题标签
    print("添加话题标签...")
    pyautogui.press('enter')
    pyautogui.write('#企业资质')
    pyautogui.press('enter')
    pyautogui.write('#申报指南')
    pyautogui.press('enter')
    pyautogui.write('#创业必看')
    
    print("\n" + "="*50)
    print("内容已填写完毕")
    print("请检查并点击发布按钮")
    print("="*50)
    
    input("发布完成后按回车退出...")

if __name__ == "__main__":
    main()
