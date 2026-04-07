"""
小红书自动发布脚本 - 使用Playwright连接已打开的小红书
"""
from playwright.sync_api import sync_playwright
import time
import os

# 图片目录
IMAGE_DIR = "c:/Users/Administrator/WorkBuddy/20260319091238/images"
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

def post_to_xiaohongshu():
    with sync_playwright() as p:
        # 连接已打开的浏览器（小红书是Electron应用，基于Chromium）
        print("正在连接小红书...")
        
        try:
            # 尝试连接小红书
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            print("已连接到浏览器")
        except Exception as e:
            print(f"无法连接: {e}")
            print("尝试启动新浏览器...")
            browser = p.chromium.launch(
                executable_path="C:/Program Files (x86)/xiaohongshu/小红书.exe",
                headless=False
            )

        contexts = browser.contexts
        if not contexts:
            print("没有找到打开的浏览器上下文")
            return

        page = contexts[0].new_page()
        
        # 获取图片列表
        images = [f"{IMAGE_DIR}/{f}" for f in os.listdir(IMAGE_DIR) if f.endswith('.png')]
        print(f"找到 {len(images)} 张图片: {images}")

        print("\n请在浏览器中手动操作完成发布")
        print("完成后按回车键...")
        input()
        
        browser.close()
        print("完成!")

if __name__ == "__main__":
    post_to_xiaohongshu()
