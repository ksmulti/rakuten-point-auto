from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import json
import rakuten_search_lib as RSL


settings = RSL.LoadSettings()
keywords = RSL.LoadKeywords()

#for key in keywords['keywords']:
#    print(key)

browser = webdriver.Chrome()    #open chrome browser
# rakuten index page
browser.get("https://websearch.rakuten.co.jp/")

btn_login = browser.find_element_by_link_text("ログイン")
btn_login.click()
RSL.WaitPageSteady(browser, 'loginInner_u')

edit_user = browser.find_element_by_id("loginInner_u")
edit_password = browser.find_element_by_id("loginInner_p")
edit_user.send_keys(settings["account"])
edit_password.send_keys(settings["password"])

btn_login = browser.find_element_by_name("submit")
btn_login.click()
RSL.WaitPageSteady(browser, 'search-input')

edit_search_input = browser.find_element_by_id("search-input")


