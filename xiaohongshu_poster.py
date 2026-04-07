"""
小红书自动发布脚本
使用方式: python xiaohongshu_poster.py
"""
from playwright.sync_api import sync_playwright
import time

# 配置
XIAOHONGSHU_URL = "https://creator.xiaohongshu.com/"
HTML_FILE = "file:///c:/Users/Administrator/WorkBuddy/20260319091238/xiaohongshu-zizhi.html"

def post_to_xiaohongshu():
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print("正在打开小红书创作者中心...")
        page.goto(XIAOHONGSHU_URL)
        page.wait_for_load_state("networkidle")

        print("\n" + "="*50)
        print("请在浏览器中完成以下操作：")
        print("1. 登录你的小红书账号")
        print("2. 登录成功后，点击'发布笔记'")
        print("3. 选择'图文'类型")
        print("4. 上传4张图片（先截取HTML页面的图）")
        print("5. 填写标题和正文")
        print("="*50)
        print("\n按回车键继续...")
        input()

        print("正在获取页面内容...")
        page.goto(HTML_FILE)
        page.wait_for_timeout(2000)

        # 截图保存
        page.screenshot(path="xiaohongshu_cover.png", full_page=True)
        print("已保存截图到: xiaohongshu_cover.png")

        print("\n操作完成！")
        browser.close()

if __name__ == "__main__":
    post_to_xiaohongshu()
