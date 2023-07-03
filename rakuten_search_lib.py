import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.utils import ChromeType
from common_lib import CommonCore
import random
import time

class RakutenSearchCore(CommonCore):
    def __init__(self):
        self._name = __name__
        CommonCore.__init__(self)
        self._keywords = self.LoadKeywords()
        
        if self._settings["account"] == "":
            print("account is empty!!")
        if self._settings["password"] == "":
            print("password is empty!!")

        self.SwitchToPopupWindow()
        self._browser.close()
        self.SwitchToMainWindow()

    def LoadKeywords(self):
        with open('keywords.json', encoding='utf-8') as json_file:
            keywords = json.load(json_file)
            return keywords
    
    def Index(self):
        self._browser.get("https://grp03.id.rakuten.co.jp/rms/nid/login?service_id=r12&return_url=login?tool_id=1&tp=&id=")
        self.WaitPageSteady('loginInner_u')
        print("Loading index OK!")
    
    def GoLoginPage(self):
        btn_login = self._browser.find_element_by_link_text("ログイン")
        btn_login.click()
        self.WaitPageSteady('loginInner_u')
        print("GoLoginPage OK!")

    def Login(self):
        edit_user = self._browser.find_element_by_id("loginInner_u")
        edit_password = self._browser.find_element_by_id("loginInner_p")
        edit_user.send_keys(self._settings["account"])
        edit_password.send_keys(self._settings["password"])

        btn_login = self._browser.find_element_by_name("submit")
        btn_login.click()
        self.WaitPageSteady('search-input')
        print("Login OK!")

    def Search(self):
        edit_search = self._browser.find_element_by_id("search-input")
        edit_search.send_keys(random.choice(self._keywords['keywords']))
        btn_search = self._browser.find_element_by_id("search-submit")
        btn_search.click()
        self.WaitPageSteady('srchformtxt_qt')

        while True:
            time.sleep(2)
            text_count = self._browser.find_element_by_class_name("progressCounter1")
            print("Count Now: " + text_count.text)

            if int(text_count.text) < 30:
                print("Search" + text_count.text)
                edit_search = self._browser.find_element_by_id("srchformtxt_qt")
                edit_search.clear()
                edit_search.send_keys(random.choice(self._keywords['keywords']))
                btn_search = self._browser.find_element_by_id("searchBtn")
                btn_search.click()
                self.WaitPageSteady('srchformtxt_qt')
            else:
                break

        

        