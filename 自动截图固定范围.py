from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from PIL import Image
import time
import os
import io
import base64

# 指定 ChromeDriver 的路径
service = Service(r'C:\Program Files\Google\Chrome\Application\driver\chromedriver.exe')  # 替换为实际路径
driver = webdriver.Chrome(service=service)

# 创建一个保存截图的文件夹
output_folder = "screenshots"
os.makedirs(output_folder, exist_ok=True)

# 链接列表
links = ['https://www.baidu.com', 'https://www.sohu.com']

# 定义截图范围 (左上角 x, 左上角 y, 宽度, 高度)
crop_area = (100, 100, 800, 600)  # 替换为你的范围

for index, link in enumerate(links):
    driver.get(link)  # 打开链接
    time.sleep(3)  # 等待页面加载

    # 截取整个页面截图为 base64
    screenshot_base64 = driver.get_screenshot_as_base64()

    # 解析 base64 数据并加载为图像
    screenshot_data = base64.b64decode(screenshot_base64)
    screenshot_image = Image.open(io.BytesIO(screenshot_data))

    # 裁剪指定范围
    cropped_image = screenshot_image.crop(crop_area)

    # 保存裁剪后的截图
    screenshot_name = os.path.join(output_folder, f'screenshot_{index + 1}.png')
    cropped_image.save(screenshot_name)
    print(f'Screenshot saved at {screenshot_name}')

driver.quit()
