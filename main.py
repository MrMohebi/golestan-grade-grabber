from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import requests

driver = webdriver.Firefox()
driver.quit()

BASE_URL = "https://eduold.uk.ac.ir/forms/authenticateuser/main.htm"
USERNAME = "98405062"
PASSWORD = "testPassword"


def start():
    global driver

    # open site
    driver = webdriver.Firefox()
    driver.get(BASE_URL)
    driver.maximize_window()
    sleep(10)

    login()


def frame_switch_id(id):
    global driver
    driver.switch_to.frame(driver.find_element_by_id(id))


def frame_switch_name(name):
    global driver
    driver.switch_to.frame(driver.find_element_by_name(name))


def login():
    global driver

    frame_switch_id("Faci1")
    frame_switch_name("Master")
    frame_switch_name("Form_Body")
    print(driver.page_source)

    # login
    usernameFiled = driver.find_element_by_id("F80351")
    usernameFiled.send_keys(USERNAME)
    passwordFiled = driver.find_element_by_id("F80401")
    passwordFiled.send_keys(PASSWORD)

    captchaImg = driver.find_element_by_id("imgCaptcha")
    captchaImgBase64 = captchaImg.screenshot_as_base64
    print(captchaImgBase64)

    response = requests.get(captchaImg.get_attribute("src"))
    print(response.content)


    captchaFiled = driver.find_element_by_id("F51701")
    captchaFiled.send_keys("aaaaa")

if __name__ == '__main__':
    start()
