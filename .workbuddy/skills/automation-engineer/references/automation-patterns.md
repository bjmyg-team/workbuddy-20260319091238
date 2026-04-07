# 自动化开发模式参考

## 一、无人值守发布流程设计

### 标准流程
```
生成内容 → 生成图片 → 登录检测 → 发布 → 结果验证 → 日志记录
```

### Cookie持久化登录
```python
import pickle
from pathlib import Path

def save_cookies(context, path="cookies.pkl"):
    cookies = context.cookies()
    with open(path, "wb") as f:
        pickle.dump(cookies, f)

def load_cookies(context, path="cookies.pkl"):
    if Path(path).exists():
        with open(path, "rb") as f:
            cookies = pickle.load(f)
        context.add_cookies(cookies)
        return True
    return False
```

### 登录状态检测
```python
def is_logged_in(page):
    """检测是否已登录"""
    try:
        page.wait_for_selector(".user-avatar", timeout=3000)
        return True
    except:
        return False
```

## 二、重试机制标准实现

```python
import time
import logging
from functools import wraps

def retry(max_attempts=3, delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    logging.warning(f"第{attempt+1}次尝试失败: {e}，{delay}秒后重试")
                    time.sleep(delay)
        return wrapper
    return decorator

# 使用方式
@retry(max_attempts=3, delay=2)
def upload_image(page, image_path):
    ...
```

## 三、多账号管理方案

```python
# accounts.json（不要提交到Git）
[
    {"username": "account1", "cookie_file": "cookies_1.pkl"},
    {"username": "account2", "cookie_file": "cookies_2.pkl"}
]

# 轮换账号发布
def get_next_account(accounts, last_used_idx):
    return accounts[(last_used_idx + 1) % len(accounts)]
```

## 四、日志规范

```python
import logging
from datetime import datetime

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # 文件日志
    fh = logging.FileHandler(f"logs/{name}_{datetime.now():%Y%m%d}.log", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    
    # 控制台日志
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
```

## 五、反检测策略（仅用于合法自动化）

```python
# 随机延迟模拟人工操作
import random
def human_delay(min_sec=0.5, max_sec=2.0):
    time.sleep(random.uniform(min_sec, max_sec))

# Playwright 初始化时隐藏自动化特征
context = browser.new_context(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...",
    viewport={"width": 1920, "height": 1080},
)
page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
```
