import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from PIL import Image
import time
import os
import io
import base64

# 配置 ChromeDriver 路径
CHROMEDRIVER_PATH = r'C:\Program Files\Google\Chrome\Application\driver\chromedriver.exe'  # 替换为实际路径
TEXT_FILE_PATH = 'Links.txt'  # 替换为你的记事本文件路径
OUTPUT_FOLDER = 'screenshots'  # 截图保存文件夹

# 正则表达式匹配 URL
URL_PATTERN = r'(https?://[^\s,()<>]+)'

# 提取记事本中的链接
def extract_links(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return re.findall(URL_PATTERN, content)

# 定义截图范围 (左上角 x, 左上角 y, 宽度, 高度)
crop_area = (100, 100, 800, 600)  # 替换为你的范围

# 打开链接并截图
def capture_screenshots(links, output_folder):
    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)
    
    # 设置 Selenium WebDriver
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    
    for index, link in enumerate(links):
        try:
            print(f"Opening {link}")
            driver.get(link)  # 打开链接
            time.sleep(3)  # 等待页面加载
            
            # 获取截图数据
            screenshot_base64 = driver.get_screenshot_as_base64()
            screenshot_data = base64.b64decode(screenshot_base64)
            screenshot_image = Image.open(io.BytesIO(screenshot_data))
            
            # 裁剪指定范围
            cropped_image = screenshot_image.crop(crop_area)

            # 保存截图
            screenshot_name = os.path.join(output_folder, f'screenshot_{index + 1}.png')
            cropped_image.save(screenshot_name)
            print(f"Screenshot saved: {screenshot_name}")
        except Exception as e:
            print(f"Failed to capture {link}: {e}")
    
    driver.quit()

# 主程序
if __name__ == '__main__':
    # 提取链接
    links = extract_links(TEXT_FILE_PATH)
    if not links:
        print("No links found in the file.")
    else:
        print(f"Found {len(links)} links.")
        # 截图并保存
        capture_screenshots(links, OUTPUT_FOLDER)

