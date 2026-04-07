"""
生成小红书图文笔记图片
"""
from playwright.sync_api import sync_playwright
import os

# HTML文件路径
HTML_FILE = "file:///c:/Users/Administrator/WorkBuddy/20260319091238/xiaohongshu-zizhi.html"
OUTPUT_DIR = "c:/Users/Administrator/WorkBuddy/20260319091238/images"

def generate_images():
    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 420, "height": 600}
        )
        page = context.new_page()

        print("正在加载HTML页面...")
        page.goto(HTML_FILE)
        page.wait_for_load_state("networkidle")

        # 截取4张图片
        # 封面
        print("正在生成封面图...")
        page.set_viewport_size({"width": 420, "height": 520})
        page.screenshot(path=f"{OUTPUT_DIR}/01_封面.png", full_page=False)

        # 内页1 - 常见资质类型
        print("正在生成第1张内页...")
        page.screenshot(path=f"{OUTPUT_DIR}/02_常见资质类型.png", full_page=True)

        # 内页2 - 申报流程
        print("正在生成第2张内页...")
        page.screenshot(path=f"{OUTPUT_DIR}/03_申报流程.png", full_page=True)

        # 内页3 - 服务优势
        print("正在生成第3张内页...")
        page.screenshot(path=f"{OUTPUT_DIR}/04_服务优势.png", full_page=True)

        print(f"\n图片已保存到: {OUTPUT_DIR}")
        print("生成的文件:")
        for f in os.listdir(OUTPUT_DIR):
            print(f"  - {f}")

        browser.close()

if __name__ == "__main__":
    generate_images()
