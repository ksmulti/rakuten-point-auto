from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import json

class RakutenKujiCore:
    def __init__(self):
        chop = webdriver.ChromeOptions()
        chop.add_extension("rakuten_extension.crx")
        self.__browser = webdriver.Chrome(chrome_options=chop)    #open chrome browser
        self.__browser.set_window_size(1300,1040)
        self.__delay = 10
        self.__kuji_sites = self.LoadKujiSites()
        self.__settings = self.LoadSettings()
    
    def LoadKujiSites(self):
        with open('rakuten_kuji_sites.json', encoding='utf-8') as json_file:
            kuji_sites = json.load(json_file)
            return kuji_sites
    
    def LoadSettings(self):
        with open('settings.json', encoding='utf-8') as json_file:
            settings = json.load(json_file)
            return settings

    def Index(self):
        url = "https://www.rakuten.co.jp"
        self.__browser.get(url)

    def WaitPageSteady(self, wait_element_id):
        try:
            WebDriverWait(self.__browser, self.__delay).until(EC.presence_of_element_located((By.ID, wait_element_id)))
            # print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")
            exit()

    def GoLoginPage(self):
        # 楽天ログインページに移動
        url = "https://grp01.id.rakuten.co.jp/rms/nid/vc?__event=login&service_id=top"
        self.__browser.get(url)
        self.WaitPageSteady('loginInner_u')
    
    def Login(self):
        # 楽天にログイン
        edit_user = self.__browser.find_element_by_id("loginInner_u")
        edit_password = self.__browser.find_element_by_id("loginInner_p")
        edit_user.send_keys(self.__settings["account"])
        edit_password.send_keys(self.__settings["password"])

        btn_login = self.__browser.find_element_by_name("submit")
        btn_login.click()
        self.WaitPageSteady('sitem')

    def OpenRakutenLuckyKuji(self, URL):
        try:
            self.__browser.get(URL) # 楽天くじURLを開く
            time.sleep(5)
            self.__browser.find_element_by_xpath("//*[@id='entry']").click() # Startボタン
            time.sleep(20) # ルーレットくじの待ち時間
        except NoSuchElementException:
            print("- NoSuchElementException: Next step")

    def Kuji(self):
        for site in self.__kuji_sites:
            self.OpenRakutenLuckyKuji(self.__kuji_sites[site])

