import time
from selenium import webdriver
from PIL import Image
from aip import AipOcr
import random
from imooc_selenium.find_element import FindElement

class RegisterFunction():
    def __init__(self, url, i):
        self.driver = self.get_driver(url, i)

    def get_driver(self, url, i):
        if i == 0:
            driver = webdriver.Chrome()
        else:
            driver = webdriver.Firefox()
        driver.get(url)
        driver.maximize_window()
        return driver

    def get_random_user(self):
        user_info = ''.join(random.sample('1234567890abcdefghijklmnopqrstuvwxyz', 8))
        return user_info

    def get_user_element(self, key):
        find_element = FindElement(self.driver)
        element = find_element.get_element(key)
        return element

    def type_user_element(self, key, value):
        self.get_user_element(key).send_keys(value)

    #获取验证码截图
    def get_image_and_save(self, filename):
        self.driver.save_screenshot(filename)
        code_element = self.get_user_element("code_image")
        left = code_element.location['x']
        top = code_element.location['y']
        right = code_element.size['width'] + left
        height = code_element.size['height'] + top
        im = Image.open(filename)
        img = im.crop((left, top, right, height))
        image = img.resize((1900,400), Image.ANTIALIAS)
        image.save(filename)

    # Read Image
    def get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    #解析验证码
    def code_online(self, filename=None):
        if filename == None:
            filename = 'E:/www/seleniumPython/image/imooc.png'
        self.get_image_and_save(filename)
        APP_ID = '21484995'
        API_KEY = '5bHi4LYSISAKUfkhhHicnGuT'
        SECRET_KEY = 'rQxyec9kLPpAuXIOtQNxwhlUwasG4KQ7'
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        # Call usual ocr interface
        result = client.basicAccurate(self.get_file_content(filename))
        words = (result['words_result'])
        if len(words) != 0:
            words = words[0]['words']
            if ' ' in words:
                words = words.replace(' ', '')
        return words

    def run_main(self):
        user_info = self.get_random_user()
        user_email = user_info + '@163.com'
        self.type_user_element('user_email', user_email)
        self.type_user_element('user_name', user_info)
        self.type_user_element('password', '11111')
        flag = True
        while flag == True:
            code_text = self.code_online()
            self.type_user_element('code_text', code_text)
            self.get_user_element('register_button').click()
            code_text_error = self.get_user_element('captcha_code-error')
            if code_text_error == None:
                flag = False
            else:
                flag = True
                self.get_user_element('code_text').clear()
                self.get_user_element('code_image').click()
                time.sleep(2)

        time.sleep(5)
        self.driver.close()

if __name__ == '__main__':
    for i in range(2):
        register_function = RegisterFunction('http://www.5itest.cn/register', i)
        register_function.run_main()