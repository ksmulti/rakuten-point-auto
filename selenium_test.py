from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import json
import rakuten_search_lib as RSL

delay = 10 # seconds
settings = RSL.LoadSettings()

browser = webdriver.Chrome()    #open chrome browser
# rakuten index page
browser.get("https://websearch.rakuten.co.jp/")

btn_login = browser.find_element_by_link_text("ログイン")
btn_login.click()

# rakuten login page
try:
    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'loginInner_u')))
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")

edit_user = browser.find_element_by_id("loginInner_u")
edit_password = browser.find_element_by_id("loginInner_p")
edit_user.send_keys(settings["account"])
edit_password.send_keys(settings["password"])

btn_login = browser.find_element_by_name("submit")
btn_login.click()

# rakuten index page
try:
    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'search-input')))
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")

edit_search_input = browser.find_element_by_id("search-input")

with open('keywords.json', encoding='utf-8') as json_file:
    keywords = json.load(json_file)

#for key in keywords['keywords']:
#    print(key)
