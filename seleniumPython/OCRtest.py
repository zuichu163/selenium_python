from selenium import webdriver
import time
from PIL import Image
from aip import AipOcr
import random
driver = webdriver.Chrome()

#初始化浏览器
def driver_init():
    driver.get("http://www.5itest.cn/register")
    driver.maximize_window()
    time.sleep(2)

#获取元素
def get_element(id):
    element = driver.find_element_by_id(id)
    return element

def get_random_user():
    user_info = ''.join(random.sample('1234567890abcdefghijklmnopqrstuvwxyz', 8))
    return user_info

#获取验证码截图
def get_image_and_save(filename):
    driver.save_screenshot(filename)
    code_element = get_element("getcode_num")
    left = code_element.location['x']
    top = code_element.location['y']
    right = code_element.size['width'] + left
    height = code_element.size['height'] + top
    im = Image.open(filename)
    img = im.crop((left, top, right, height))
    image = img.resize((1900,400), Image.ANTIALIAS)
    image.save(filename)

# Read Image
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

#解析验证码
def code_online(filename):
    APP_ID = '21484995'
    API_KEY = '5bHi4LYSISAKUfkhhHicnGuT'
    SECRET_KEY = 'rQxyec9kLPpAuXIOtQNxwhlUwasG4KQ7'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    # Call usual ocr interface
    result = client.basicAccurate(get_file_content(filename))
    words = (result['words_result'])
    if len(words) != 0:
        words = words[0]['words']
        if ' ' in words:
            words = words.replace(' ', '')
    return words

def run_main():
    filename = 'E:/www/seleniumPython/imooc.png'
    driver_init()
    user_info = get_random_user()
    user_email = user_info + '@163.com'
    get_element('register_email').send_keys(user_email)
    get_element('register_nickname').send_keys(user_info)
    get_element('register_password').send_keys('111111')
    get_image_and_save(filename)
    words = code_online(filename)
    print(words)
    get_element("captcha_code").send_keys(words)
    get_element('register-btn').click()
    time.sleep(5)
    driver.close()

run_main()

