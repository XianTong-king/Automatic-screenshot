from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# 指定 ChromeDriver 的路径
service = Service(r'C:\Program Files\Google\Chrome\Application\driver\chromedriver.exe')  # 替换为你实际的 chromedriver 路径

# 初始化 WebDriver
driver = webdriver.Chrome(service=service)

links = ['https://www.baidu.com',]  # 链接列表

for index, link in enumerate(links):
    driver.get(link)  # 打开链接
    time.sleep(3)  # 等待页面加载

    # 截图
    screenshot_name = f'screenshot_{index + 1}.png'
    driver.save_screenshot(screenshot_name)
    print(f'Screenshot saved as {screenshot_name}')

driver.quit()
