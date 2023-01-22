from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class Golestan:
    driver = None
    BaseURL = None
    USERNAME = None
    PASSWORD = None
    HasCaptcha = True

    CODES = {
        "wrong_pass": "WRONG_PASSWORD",
        "success": "SUCCESS",
        "try_later": "TRY_LATER"
    }

    def __init__(self, loginURL, username, password, hasCaptcha=True, iranProxy=None):
        self.BaseURL = loginURL
        self.USERNAME = username
        self.PASSWORD = password
        self.HasCaptcha = hasCaptcha
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        if iranProxy is not None:
            chrome_options.add_argument('--proxy-server=%s' % iranProxy)

        self.driver = webdriver.Chrome(options=chrome_options)

    def frame_switch_id(self, frameId):
        self.driver.switch_to.frame(self.driver.find_element(By.ID, frameId))

    def frame_switch_name(self, name):
        self.driver.switch_to.frame(self.driver.find_element(By.NAME, name))

    def getUserScores(self):
        print("opening site for: " + self.USERNAME)
        self.driver.get(self.BaseURL)
        sleep(10)
        loginRes = self.login(self.USERNAME, self.PASSWORD)
        if loginRes == self.CODES["success"]:
            self.main2TermPage(-1)
            scores = self.getScoresDic()
            self.driver.quit()
            return {"data": scores, "code": loginRes}

        elif loginRes == self.CODES["wrong_pass"]:
            return {"data": [], "code": loginRes}

        return {"data": [], "code": self.CODES["try_later"]}

    def login(self, username, password) -> str:
        self.driver.switch_to.default_content()
        if self.HasCaptcha:
            # js = 'function enterCaptcha(){if(window.location.host.match(/eduold\.uk\.ac\.ir/)){var e=setInterval((function(){if(document.getElementById("Faci1")?.contentDocument?.getElementsByName?.("Master")?.[0]?.contentDocument?.getElementsByName?.("Form_Body")?.[0]?.contentDocument?.getElementById?.("imgCaptcha")){clearInterval(e);let n=document.getElementById("Faci1")?.contentDocument?.getElementsByName?.("Master")?.[0]?.contentDocument?.getElementsByName?.("Form_Body")?.[0]?.contentDocument?.getElementById?.("imgCaptcha"),c=n.src;const o=e=>fetch(e).then((e=>e.blob())).then((e=>new Promise(((t,n)=>{const c=new FileReader;c.onloadend=()=>t(c.result),c.onerror=n,c.readAsDataURL(e)}))));function t(e){o(e).then((e=>{const t=new FormData;t.set("img",e.replace("data:image/gif;base64,","")),fetch("captcha-solver:8000/edu",{method:"POST",body:t}).then((e=>e.json())).then((e=>{var t=document?.getElementById?.("Faci1")?.contentDocument?.getElementsByName?.("Master")?.[0]?.contentDocument?.getElementsByName?.("Form_Body")?.[0]?.contentDocument?.getElementById?.("F51701");t.value=e.captcha||"",document.getElementById("Faci1")?.contentDocument?.getElementsByName?.("Master")?.[0]?.contentDocument?.getElementsByName?.("Form_Body")?.[0]?.contentDocument?.getElementById?.("btnLog").click()})).catch((e=>{}))}))}t(c),observer=new MutationObserver((e=>{e.forEach((e=>{e.attributeName.includes("src")&&"https://eduold.uk.ac.ir/_images/webbusy.gif"!==n.src&&t(n.src)}))})),observer.observe(n,{attributes:!0})}}),3000);setTimeout((function(){clearInterval(e)}),3e4)}}enterCaptcha();'
            js = 'function enterCaptcha(){if(window.location.host.match(/eduold\.uk\.ac\.ir/)){var e=setInterval((function(){if(document.getElementById("Faci1")?.contentDocument?.getElementsByName?.("Master")?.[0]?.contentDocument?.getElementsByName?.("Form_Body")?.[0]?.contentDocument?.getElementById?.("imgCaptcha")){clearInterval(e);let n=document.getElementById("Faci1")?.contentDocument?.getElementsByName?.("Master")?.[0]?.contentDocument?.getElementsByName?.("Form_Body")?.[0]?.contentDocument?.getElementById?.("imgCaptcha"),c=n.src;const o=e=>fetch(e).then((e=>e.blob())).then((e=>new Promise(((t,n)=>{const c=new FileReader;c.onloadend=()=>t(c.result),c.onerror=n,c.readAsDataURL(e)}))));function t(e){o(e).then((e=>{const t=new FormData;t.set("img",e.replace("data:image/gif;base64,","")),fetch("https://captcha.mdhi.dev/edu",{method:"POST",body:t}).then((e=>e.json())).then((e=>{var t=document?.getElementById?.("Faci1")?.contentDocument?.getElementsByName?.("Master")?.[0]?.contentDocument?.getElementsByName?.("Form_Body")?.[0]?.contentDocument?.getElementById?.("F51701");t.value=e.captcha||"",document.getElementById("Faci1")?.contentDocument?.getElementsByName?.("Master")?.[0]?.contentDocument?.getElementsByName?.("Form_Body")?.[0]?.contentDocument?.getElementById?.("btnLog").click()})).catch((e=>{}))}))}t(c),observer=new MutationObserver((e=>{e.forEach((e=>{e.attributeName.includes("src")&&"https://eduold.uk.ac.ir/_images/webbusy.gif"!==n.src&&t(n.src)}))})),observer.observe(n,{attributes:!0})}}),3000);setTimeout((function(){clearInterval(e)}),3e4)}}enterCaptcha();'
            self.driver.execute_script(js)

        self.frame_switch_id("Faci1")
        self.frame_switch_name("Master")
        self.frame_switch_name("Form_Body")

        # login
        usernameFiled = self.driver.find_element(By.ID, "F80351")
        usernameFiled.send_keys(username)
        passwordFiled = self.driver.find_element(By.ID, "F80401")
        passwordFiled.send_keys(password)

        self.driver.switch_to.default_content()

        maxTries = 10
        while len(self.driver.find_elements(By.ID, "Faci2")) < 1:

            self.frame_switch_id("Faci1")
            self.frame_switch_name("Message")

            print(self.driver.page_source.encode("utf-8"))

            if self.driver.find_element(By.ID, "errtxt").get_attribute("title") == "کد1 : شناسه کاربري يا گذرواژه اشتباه است.":
                print("Wrong password for " + username)
                return self.CODES['wrong_pass']

            sleep(7)
            print("try to login...")
            if maxTries < 0:
                print("couldn't login,something went wrong " + username)
                return self.CODES['try_later']

            maxTries -= 1
            self.driver.switch_to.default_content()

        # check page is loaded
        self.frame_switch_id("Faci2")
        self.frame_switch_name("Master")
        self.frame_switch_name("Form_Body")

        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//td[@f="12310"]')))

        print("Logged in :)")
        return self.CODES['success']

    def main2TermPage(self, termIndex):
        self.driver.switch_to.default_content()
        self.frame_switch_id("Faci2")
        self.frame_switch_name("Master")
        self.frame_switch_name("Form_Body")

        allStudentInfoMenuItem = self.driver.find_element(By.XPATH, '//td[@f="12310"]')
        allStudentInfoMenuItem.click()
        sleep(1)
        allStudentInfoMenuItem.click()

        sleep(2)

        self.driver.switch_to.default_content()
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, "Faci3")))
        self.frame_switch_id("Faci3")
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.NAME, "Master")))
        self.frame_switch_name("Master")
        self.frame_switch_name("Form_Body")

        table = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, "T01")))

        tbody = WebDriverWait(table, 30).until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))

        while len(tbody.find_elements(By.TAG_NAME, "tr")) < 2:
            sleep(1)

        tableRows = tbody.find_elements(By.TAG_NAME, "tr")

        # select last term
        tableRows[termIndex].click()
        sleep(2)

        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, "FrameNewForm")))

        self.frame_switch_id("FrameNewForm")

        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, "T02")))
        sleep(2)
        self.driver.switch_to.default_content()
        print("got to term " + str(termIndex) + " page")

    def getScoresDic(self):
        self.driver.switch_to.default_content()
        self.frame_switch_id("Faci3")
        self.frame_switch_name("Master")
        self.frame_switch_name("Form_Body")
        self.frame_switch_id("FrameNewForm")

        scoreTableRows = self.driver.find_element(By.ID, "T02").find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
        averageAll = self.driver.find_element(By.ID, "T01").find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")[4].find_elements(By.TAG_NAME, "td")[1].text
        allCourseCreditPassed = self.driver.find_element(By.ID, "T01").find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")[4].find_elements(By.TAG_NAME, "td")[2].text

        # first row is empty
        scoreTableRows.pop(0)
        scores = []
        for lessen in scoreTableRows:
            try:
                lessenInfos = lessen.find_elements(By.TAG_NAME, "td")
                scores.append({
                    "name": lessenInfos[5].get_attribute("title"),
                    "score": lessenInfos[8].text,
                    "courseCredit": lessenInfos[6].text,
                    "averageAll": averageAll,
                    "allCourseCreditPassed": allCourseCreditPassed,
                })
            except:
                pass

        weighted_sum = 0
        total_weight = 0
        for score in scores:
            if len(score['score']) > 0:
                weighted_sum += float(score['courseCredit']) * float(score['score'])
                total_weight += float(score['courseCredit'])

        termAverage = str(round(weighted_sum / total_weight, 2))
        for i in range(len(scores)):
            scores[i]["termAverage"] = termAverage

        print(scores)

        return scores
