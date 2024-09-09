import os
import time
import datetime
import re
import sys
import json
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
import selenium.common.exceptions

def save_screenshot(driver, tag):
    '''if the development env var is set, then store the screenshot'''
    if os.environ.get("SCREENSHOT_LOG") == "TRUE":
      driver.save_screenshot(f"/tmp/screenshots/{datetime.date.today()}-{tag}.png")

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def log(message: str, timestamp=True) -> None:
    '''global logging function'''
    if timestamp:
        d = datetime.date.today()
        inp = f'{d} - {message}.'
        eprint(inp)
    else:
        inp = f'{message}.'
        eprint(inp)


def update_esphome_via_selenium(esphometarget, query):

    log("Starting bin day scrape")
    opts = FirefoxOptions()
    opts.add_argument("--headless")

    with webdriver.Firefox(options=opts) as driver:

        driver.maximize_window()
        driver.get('https://'+esphometarget+'/BinSearch.aspx')

        try:
            time.sleep(2) #wait for page-load

            res = {}

            save_screenshot(driver, "1.load")
            #check if devices are up-to-date
            search_box = driver.find_element(By.NAME, "q").send_keys(query)
            search = driver.find_element(By.CLASS_NAME, "btn--feature").click()
            save_screenshot(driver, "2.search")
            time.sleep(1) 
            submit = driver.find_element(By.CLASS_NAME, "btn--full").click()
            time.sleep(1) 
            save_screenshot(driver, "3.submit")
            next_day = driver.find_element(By.CLASS_NAME, "alpha")
            log(next_day.text)
            res['next_day'] = next_day.text
            bin_type = driver.find_element(By.CLASS_NAME, "zero--top")
            for element in bin_type.find_elements(By.XPATH, ".//*"):
                if element.text.startswith("This is a"):
                    log(element.text)
                    res['bin_type'] = element.text

            print(json.dumps(res))


        except selenium.common.exceptions.NoSuchElementException as e:
            log("Some elements could not be found in page", e)
            log("ERROR: Scraping failed")
        return 0



def check_env():
    '''function checks the environment variables to be suitable for this code'''

    #check logging
    if os.environ.get("SCREENSHOT_LOG") == "TRUE":
        log("Logging screenshots")


if __name__ == "__main__":
    #check environment variables
    check_env()

    update_esphome_via_selenium('pre.southkesteven.gov.uk', 'marlvon')
