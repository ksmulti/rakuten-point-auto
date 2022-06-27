from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from common_lib import CommonCore
import time
import json

class RakutenKujiCore(CommonCore):
    def __init__(self):
        self._name = __name__
        CommonCore.__init__(self)
        self._browser.set_window_size(1300,1040)
        self.__delay = 10
        self.__kuji_sites = self.LoadKujiSites()
        self.__settings = self.LoadSettings()
        
        self.SwitchToPopupWindow()
        self._browser.close()
        self.SwitchToMainWindow()
    
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
        self._browser.get(url)

    def WaitElementSteady(self, element, wait_by = By.ID, is_stop = True):
        try:
            WebDriverWait(self._browser, self.__delay).until(EC.presence_of_element_located((By.ID, element)))
            # print("Page is ready!")
        except TimeoutException:
            print("WaitElementSteady: Loading took too much time!")
            if is_stop:
                exit()

    def GoLoginPage(self):
        # 楽天ログインページに移動
        url = "https://grp01.id.rakuten.co.jp/rms/nid/vc?__event=login&service_id=top"
        self._browser.get(url)
        self.WaitPageSteady('loginInner_u')
    
    def Login(self):
        # 楽天にログイン
        edit_user = self._browser.find_element_by_id("loginInner_u")
        edit_password = self._browser.find_element_by_id("loginInner_p")
        edit_user.send_keys(self.__settings["account"])
        edit_password.send_keys(self.__settings["password"])

        btn_login = self._browser.find_element_by_name("submit")
        btn_login.click()
        self.WaitPageSteady('common-header-search-input')

    def OpenRakutenLuckyKuji(self, URL):
        try:
            self._browser.get(URL) # 楽天くじURLを開く
            #time.sleep(5)
            self.WaitPageSteady("//*[@id='entry']", By.XPATH, False)
            self._browser.find_element_by_xpath("//*[@id='entry']").click() # Startボタン
            time.sleep(20) # ルーレットくじの待ち時間
        except NoSuchElementException:
            print("- NoSuchElementException: Next step")

    def Kuji(self):
        for site in self.__kuji_sites:
            self.OpenRakutenLuckyKuji(self.__kuji_sites[site])

