import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

def LoadSettings():
    with open('settings.json', encoding='utf-8') as json_file:
        settings = json.load(json_file)
        return settings

def LoadKeywords():
    with open('keywords.json', encoding='utf-8') as json_file:
        keywords = json.load(json_file)
        return keywords

def WaitPageSteady(browser, wait_element_id):
    delay = 10 # seconds
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, wait_element_id)))
        # print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")
        exit()

def Login():
    print("Hello from a function")