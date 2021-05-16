import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
import random
import time
import os
from PIL import Image

class CommonCore:
    _name = "CommonCore"
    _browser = None
    _delay = None
    _settings = None
    _main_window_handle = None

    def __init__(self):
        print(self._name + " start")
        chop = webdriver.ChromeOptions()
        chop.add_argument("--no-sandbox")
        chop.add_argument("--disable-setuid-sandbox")
        chop.add_extension("rakuten_extension.crx")
        if os.name == 'nt':
            self._browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chop)    #open chrome browser
        else:
            chop.add_argument('--headless')
            chop.add_argument("--remote-debugging-port=9222")
            chop.add_argument("--single-process")
            self._browser = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(), options=chop)    #open chrome browser
        
        self._delay = 10
        self._settings = self.LoadSettings()
        self._main_window_handle = self._browser.current_window_handle

    def LoadSettings(self):
        with open('settings.json', encoding='utf-8') as json_file:
            settings = json.load(json_file)
            return settings

    def WaitPageSteady(self, wait_element_id, by = By.ID, quit_timeout = True):
        try:
            WebDriverWait(self._browser, self._delay).until(EC.presence_of_element_located((by, wait_element_id)))
            print(wait_element_id + " is ready!")
            time.sleep(1)
            if by == By.ID:
                return self._browser.find_element_by_id(wait_element_id)
            elif by == By.CLASS_NAME:
                return self._browser.find_element_by_class_name(wait_element_id)
            elif by == By.NAME:
                return self._browser.find_element_by_name(wait_element_id)
            elif by == By.LINK_TEXT:
                return self._browser.find_element_by_link_text(wait_element_id)
            elif by == By.PARTIAL_LINK_TEXT:
                return self._browser.find_element_by_partial_link_text(wait_element_id)
            elif by == By.TAG_NAME:
                return self._browser.find_element_by_tag_name(wait_element_id)
            elif by == By.XPATH:
                return self._browser.find_element_by_xpath(wait_element_id)
            else:
                return None
        except TimeoutException:
            print("Can not find " + wait_element_id + "!!!")
            if quit_timeout:
                self.Quit()
                exit()

    def Quit(self):
        self._browser.quit()
        print("Browser quit")

    def SwitchToPopupWindow(self):
        signin_window_handle = None
        while not signin_window_handle:
            for handle in self._browser.window_handles:
                if handle != self._main_window_handle:
                    signin_window_handle = handle
                    break
        self._browser.switch_to.window(signin_window_handle)

    def SwitchToMainWindow(self):
        self._browser.switch_to.window(self._main_window_handle)

    def get_captcha(self, element, path):
        # now that we have the preliminary stuff out of the way time to get that image :D
        location = element.location
        size = element.size
        # saves screenshot of entire page
        self._browser.save_screenshot(path)

        # uses PIL library to open image in memory
        image = Image.open(path)

        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']

        image = image.crop((left, top, right, bottom))  # defines crop points
        image.save(path, 'png')  # saves new cropped image

