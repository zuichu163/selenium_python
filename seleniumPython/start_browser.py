from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import time
from PIL import Image
from ShowapiRequest import ShowapiRequest

driver = webdriver.Chrome()
driver.get("http://www.5itest.cn/register")
time.sleep(2)
driver.find_element_by_id("register_email").send_keys("sywangjue@163.com")
driver.find_element_by_name("nickname").send_keys("aecto")
driver.find_element_by_xpath("//*[@id='register_password']").send_keys("123456")

driver.save_screenshot('E:/www/seleniumPython/imooc.png')
code_element = driver.find_element_by_id("getcode_num")
left = code_element.location['x']
top = code_element.location['y']
right = code_element.size['width'] + left
height = code_element.size['height'] + top
im = Image.open("E:/www/seleniumPython/imooc.png")
img = im.crop((left, top, right, height))
path = "E:/www/seleniumPython/imooc1.png" # 图片文件路径，必须输入！
img.save(path)

r = ShowapiRequest("http://route.showapi.com/1274-2","62626","d61950be50dc4dbd99691741b8e730f5" )
r.addBodyPara("typeId", "35")
r.addBodyPara("convert_to_jpg", "0")
r.addFilePara("image", path)
res = r.post()
print(res.text) # 返回信息
driver.close()
