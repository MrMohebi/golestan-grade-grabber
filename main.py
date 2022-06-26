from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep

driver = webdriver.Chrome()
driver.quit()

BASE_URL = "https://eduold.uk.ac.ir/forms/authenticateuser/main.htm"
USERNAME = "98405062"
PASSWORD = "3210079927"


def start():
    global driver

    # open site
    chrome_options = Options()
    chrome_options.headless = True
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(BASE_URL)

    sleep(5)
    login()
    sleep(5)
    main2TermPage(-1)
    sleep(5)
    scores = getScoresDic()


def frame_switch_id(id):
    global driver
    driver.switch_to.frame(driver.find_element(By.ID, id))


def frame_switch_name(name):
    global driver
    driver.switch_to.frame(driver.find_element(By.NAME, name))


def login():
    global driver

    js = 'function enterCaptcha(){if(window.location.host.match(/eduold\.uk\.ac\.ir/)){var e=setInterval((function(){if(document.getElementById("Faci1")?.contentDocument?.getElementsByName?.("Master")?.[0]?.contentDocument?.getElementsByName?.("Form_Body")?.[0]?.contentDocument?.getElementById?.("imgCaptcha")){clearInterval(e);let n=document.getElementById("Faci1")?.contentDocument?.getElementsByName?.("Master")?.[0]?.contentDocument?.getElementsByName?.("Form_Body")?.[0]?.contentDocument?.getElementById?.("imgCaptcha"),c=n.src;const o=e=>fetch(e).then((e=>e.blob())).then((e=>new Promise(((t,n)=>{const c=new FileReader;c.onloadend=()=>t(c.result),c.onerror=n,c.readAsDataURL(e)}))));function t(e){o(e).then((e=>{const t=new FormData;t.set("img",e.replace("data:image/gif;base64,","")),fetch("https://captcha.mdhi.dev/edu",{method:"POST",body:t}).then((e=>e.json())).then((e=>{var t=document?.getElementById?.("Faci1")?.contentDocument?.getElementsByName?.("Master")?.[0]?.contentDocument?.getElementsByName?.("Form_Body")?.[0]?.contentDocument?.getElementById?.("F51701");t.value=e.captcha||"",document.getElementById("Faci1")?.contentDocument?.getElementsByName?.("Master")?.[0]?.contentDocument?.getElementsByName?.("Form_Body")?.[0]?.contentDocument?.getElementById?.("btnLog").click()})).catch((e=>{}))}))}t(c),observer=new MutationObserver((e=>{e.forEach((e=>{e.attributeName.includes("src")&&"https://eduold.uk.ac.ir/_images/webbusy.gif"!==n.src&&t(n.src)}))})),observer.observe(n,{attributes:!0})}}),1000);setTimeout((function(){clearInterval(e)}),3e4)}}enterCaptcha();'
    driver.execute_script(js)

    frame_switch_id("Faci1")
    frame_switch_name("Master")
    frame_switch_name("Form_Body")

    # login
    usernameFiled = driver.find_element(By.ID, "F80351")
    usernameFiled.send_keys(USERNAME)
    passwordFiled = driver.find_element(By.ID, "F80401")
    passwordFiled.send_keys(PASSWORD)

    driver.switch_to.default_content()

    while len(driver.find_elements(By.ID, "Faci2")) < 1 :
        sleep(2)

    print("Logged in :)")
    return True


def main2TermPage(termIndex):
    global driver
    driver.switch_to.default_content()
    frame_switch_id("Faci2")
    frame_switch_name("Master")
    frame_switch_name("Form_Body")

    allStudentInfoMenuItem = driver.find_element(By.XPATH, '//td[@f="12310"]')
    allStudentInfoMenuItem.click()
    sleep(1)
    allStudentInfoMenuItem.click()

    sleep(5)

    driver.switch_to.default_content()
    frame_switch_id("Faci3")
    frame_switch_name("Master")
    frame_switch_name("Form_Body")

    table = driver.find_element(By.ID, "T01")

    tableRows = table.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")

    # select last term
    tableRows[termIndex].click()
    driver.switch_to.default_content()
    print("got to term " + str(termIndex) + " page")


def getScoresDic():
    global driver
    driver.switch_to.default_content()
    frame_switch_id("Faci3")
    frame_switch_name("Master")
    frame_switch_name("Form_Body")
    frame_switch_id("FrameNewForm")

    scoreTableRows = driver.find_element(By.ID, "T02").find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
    # first row is empty
    scoreTableRows.pop(0)
    scores = {}
    for lessen in scoreTableRows:
        try:
            lessenInfos = lessen.find_elements(By.TAG_NAME, "td")
            scores[lessenInfos[5].get_attribute("title")] = lessenInfos[8].text
        except:pass

    print(scores)

    return scores


if __name__ == '__main__':
    start()
