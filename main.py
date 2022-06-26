from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import requests

driver = webdriver.Chrome()
driver.quit()

BASE_URL = "https://eduold.uk.ac.ir/forms/authenticateuser/main.htm"
USERNAME = "98405062"
PASSWORD = "3210079927"


def start():
    global driver

    # open site
    driver = webdriver.Chrome()
    driver.get(BASE_URL)

    sleep(5)

    login()


def frame_switch_id(id):
    global driver
    driver.switch_to.frame(driver.find_element(By.ID, id))


def frame_switch_name(name):
    global driver
    driver.switch_to.frame(driver.find_element(By.NAME, name))


def login():
    global driver

    # js = 'function enterCaptcha(){if(window.location.host.match(/eduold\.uk\.ac\.ir/)){var e=setInterval((function(){if(document.getElementById("Faci1")?.contentDocument?.getElementsByName?.("Master")?.[0]?.contentDocument?.getElementsByName?.("Form_Body")?.[0]?.contentDocument?.getElementById?.("imgCaptcha")){clearInterval(e);let n=document.getElementById("Faci1")?.contentDocument?.getElementsByName?.("Master")?.[0]?.contentDocument?.getElementsByName?.("Form_Body")?.[0]?.contentDocument?.getElementById?.("imgCaptcha"),o=n.src;const c=e=>fetch(e).then((e=>e.blob())).then((e=>new Promise(((t,n)=>{const o=new FileReader;o.onloadend=()=>t(o.result),o.onerror=n,o.readAsDataURL(e)}))));function t(e){c(e).then((e=>{const t=new FormData;t.set("img",e.replace("data:image/gif;base64,","")),fetch("https://captcha.mdhi.dev/edu",{method:"POST",body:t}).then((e=>e.json())).then((e=>{var t=document?.getElementById?.("Faci1")?.contentDocument?.getElementsByName?.("Master")?.[0]?.contentDocument?.getElementsByName?.("Form_Body")?.[0]?.contentDocument?.getElementById?.("F51701");t.value=e.captcha||""})).catch((e=>console.error(e)))}))}t(o),observer=new MutationObserver((e=>{e.forEach((e=>{e.attributeName.includes("src")&&"https://eduold.uk.ac.ir/_images/webbusy.gif"!==n.src&&t(n.src)}))})),observer.observe(n,{attributes:!0})}}),100);setTimeout((function(){clearInterval(e)}),3e4)}}enterCaptcha();'
    js = 'function enterCaptcha(){if(window.location.host.match(/eduold\.uk\.ac\.ir/)){var e=setInterval((function(){if(document.getElementById("Faci1")?.contentDocument?.getElementsByName?.("Master")?.[0]?.contentDocument?.getElementsByName?.("Form_Body")?.[0]?.contentDocument?.getElementById?.("imgCaptcha")){clearInterval(e);let n=document.getElementById("Faci1")?.contentDocument?.getElementsByName?.("Master")?.[0]?.contentDocument?.getElementsByName?.("Form_Body")?.[0]?.contentDocument?.getElementById?.("imgCaptcha"),c=n.src;const o=e=>fetch(e).then((e=>e.blob())).then((e=>new Promise(((t,n)=>{const c=new FileReader;c.onloadend=()=>t(c.result),c.onerror=n,c.readAsDataURL(e)}))));function t(e){o(e).then((e=>{const t=new FormData;t.set("img",e.replace("data:image/gif;base64,","")),fetch("https://captcha.mdhi.dev/edu",{method:"POST",body:t}).then((e=>e.json())).then((e=>{var t=document?.getElementById?.("Faci1")?.contentDocument?.getElementsByName?.("Master")?.[0]?.contentDocument?.getElementsByName?.("Form_Body")?.[0]?.contentDocument?.getElementById?.("F51701");t.value=e.captcha||"",document.getElementById("Faci1")?.contentDocument?.getElementsByName?.("Master")?.[0]?.contentDocument?.getElementsByName?.("Form_Body")?.[0]?.contentDocument?.getElementById?.("btnLog").click()})).catch((e=>{}))}))}t(c),observer=new MutationObserver((e=>{e.forEach((e=>{e.attributeName.includes("src")&&"https://eduold.uk.ac.ir/_images/webbusy.gif"!==n.src&&t(n.src)}))})),observer.observe(n,{attributes:!0})}}),1000);setTimeout((function(){clearInterval(e)}),3e4)}}enterCaptcha();'
    driver.execute_script(js)

    frame_switch_id("Faci1")
    frame_switch_name("Master")
    frame_switch_name("Form_Body")
    print(driver.page_source)

    # login
    usernameFiled = driver.find_element(By.ID, "F80351")
    usernameFiled.send_keys(USERNAME)
    passwordFiled = driver.find_element(By.ID, "F80401")
    passwordFiled.send_keys(PASSWORD)

    print("Logged in :)")
    return True


if __name__ == '__main__':
    start()
