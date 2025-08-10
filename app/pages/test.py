"""Scrapes quotes from the given url.

The url is 'https://quotes.toscrape.com/'.
"""

import streamlit as st
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.core.os_manager import ChromeType
import subprocess
import shutil
import pandas as pd

def get_chromium_version() -> str:
    try:
        result = subprocess.run(['chromium', '--version'], capture_output=True, text=True)
        version = result.stdout.split()[1]
        return version
    except Exception as e:
        return str(e)

def get_chromedriver_version() -> str:
    try:
        result = subprocess.run(['chromedriver', '--version'], capture_output=True, text=True)
        version = result.stdout.split()[1]
        return version
    except Exception as e:
        return str(e)

def get_chromedriver_path() -> str:
    return shutil.which('chromedriver')

st.text('This is only for debugging purposes.\n'
        'Checking versions installed in environment:\n\n'
        f'- Chromedriver:  {get_chromedriver_version()}\n'
        f'- Chromium:      {get_chromium_version()}\n'
        f'- Chromedriver Path: {get_chromedriver_path()}'
        )

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1920x1080')
chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument("--browserVersion=114")
# 114.0.5735.90
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

url = 'https://quotes.toscrape.com/'

driver.get(url)

quotes = driver.find_elements('xpath', '//span[@class="text"]')

data = []
for q in quotes:
    data.append(q.text)
    
driver.quit()

df = pd.DataFrame(data, columns=['Quotes'])
st.dataframe(df)

st.text('This is only for debugging purposes.\n'
        'Checking versions installed in environment:\n\n'
        f'- Chromedriver:  {get_chromedriver_version()}\n'
        f'- Chromium:      {get_chromium_version()}\n'
        f'- Chromedriver Path: {get_chromedriver_path()}'
        )