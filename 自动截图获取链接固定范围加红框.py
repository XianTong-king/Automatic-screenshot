import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from PIL import Image, ImageDraw
import time
import os
import io
import base64

# 配置 ChromeDriver 路径
CHROMEDRIVER_PATH = r'C:\Program Files\Google\Chrome\Application\driver\chromedriver.exe'  # 替换为实际路径
TEXT_FILE_PATH = 'Links.txt'  # 替换为你的记事本文件路径
OUTPUT_FOLDER = 'screenshots_with_red_box'  # 截图保存文件夹

# 正则表达式匹配 URL
URL_PATTERN = r'(https?://[^\s,()<>]+)'

# 提取记事本中的链接
def extract_links(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return re.findall(URL_PATTERN, content)

# 在图片上添加红框
def add_red_box(image_path, output_path, box_coordinates, box_width=5):
    with Image.open(image_path) as img:
        draw = ImageDraw.Draw(img)
        # 绘制矩形红框
        for i in range(box_width):  # 添加框宽度
            draw.rectangle(
                [
                    (box_coordinates[0] - i, box_coordinates[1] - i), 
                    (box_coordinates[2] + i, box_coordinates[3] + i)
                ],
                outline="red"
            )
        img.save(output_path)

# 打开链接并截图
def capture_screenshots_with_red_box(links, output_folder, box_coordinates):
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
            
            # 保存原始截图
            original_screenshot_path = os.path.join(output_folder, f'screenshot_{index + 1}_original.png')
            screenshot_image.save(original_screenshot_path)

            # 添加红框并保存
            output_screenshot_path = os.path.join(output_folder, f'screenshot_{index + 1}_with_red_box.png')
            add_red_box(original_screenshot_path, output_screenshot_path, box_coordinates)
            print(f"Screenshot with red box saved: {output_screenshot_path}")
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
        # 定义红框位置 (左上角 x, 左上角 y, 右下角 x, 右下角 y)
        red_box_coordinates = (100, 100, 400, 300)  # 替换为你的红框坐标
        # 截图并添加红框
        capture_screenshots_with_red_box(links, OUTPUT_FOLDER, red_box_coordinates)
