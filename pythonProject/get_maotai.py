# coding=utf-8
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from get_sliding_distance import get_distance,get_edges,gen_move_track
from image_process import base64_2_picture,get_block_w_h_JD
import time

driver = webdriver.Chrome()
driver.set_window_size(900, 600)
# driver.maximize_window()
driver.get('https://www.jd.com')

def log_in(username, password):
    user = driver.find_element(By.ID, 'loginname')
    user.send_keys(username)
    passw = driver.find_element(By.ID, 'nloginpwd')
    passw.send_keys(password)
    submit = driver.find_element(By.ID, 'loginsubmit')
    submit.click()


# 登陆用：
if driver.find_element(by=By.PARTIAL_LINK_TEXT, value='你好，请登录'):
    driver.find_element(by=By.PARTIAL_LINK_TEXT, value='你好，请登录').click()

user = 'haonan发财'
pwd = 'jingdong$$666'
log_in(user, pwd)
time.sleep(5)
if driver.find_element(by=By.CLASS_NAME, value='JDJRV-suspend-slide'):
    #登陆界面与验证界面不在同一位置，需要切换frame，京东滑块并不在一个新的frame中，此处不需要切换
    # driver.switch_to.frame(driver.find_element(by=By.ID, value='JDJRV-wrap-loginsubmit'))
    #寻找图片并下载到本地，对其进行处理求解移动距离：
    image = driver.find_element(By.XPATH,'/html/body/div[4]/div/div')
    print('找到image')
    #获取图片缺陷链接
    url_big_image = driver.find_element(By.XPATH,'/html/body/div[4]/div/div/div/div[1]/div[2]/div[1]/img').get_attribute('src')
    #此处获取到的一个 Base64 编码的图片数据，不能用request库来请求下载：采用别base64库，详情请看函数
    image_binary=base64_2_picture(url_big_image)#需要进行边缘识别的图像
    image_path= '/Users/haonan/Desktop/image.png'
    image_binary.save(image_path)#需要先将其保存为图像
    image_edge = get_edges(image_path)
    # image.save(save_path+'image.png')#将图片保存到本地
    # image1_edge.save
    #图上小方块的width，经过边缘检测算法得到距离后减去其width后即时移动的距离distance
    slid_block_string =driver.find_element(By.XPATH,'/html/body/div[4]/div/div/div/div[1]/div[2]/div[2]').get_attribute('style')
    w,h= get_block_w_h_JD(slid_block_string)
    #获取滑动距离：
    distance = get_distance(image_path,w,h)
    #获得滑动的轨迹
    drag_track = gen_move_track(distance)
    #找到我们的拖动目标,此处由于嵌套太多，所以需要通过xpath来寻找，Google浏览器开发者模式可以一键复制完整xpath
    drag_target = driver.find_element(by=By.XPATH,value='/html/body/div[4]/div/div/div/div[2]/div[3]')
    #按住鼠标,按住拖动目标：遍历轨迹列表，将其做为水平偏移量
    action =ActionChains(driver)
    action.click_and_hold(drag_target)
    for x in drag_track:
        action.move_by_offset(x,0)
    action.release().perform()#释放鼠标
    print('验证成功')
time.sleep(2)

# 释放环境资源
driver.quit()
