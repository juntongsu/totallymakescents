# -------------------------------------------------------------------------
# Import libraries
# -------------------------------------------------------------------------
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

import time
import random
import re
import requests
import sys
import pathlib
import datetime
from pathlib import Path

from bs4 import BeautifulSoup
from selenium import webdriver            
#from splinter import Browser
#from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.chrome.service import Service as ChromeService
#from selenium.webdriver.chrome.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as GeckoService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.common.by import By 
#from selenium.webdriver.common.keys import Keys 
#from selenium_stealth import stealth

# from app.pages.helper_funcs import *
from recommender.version_epsilon.helper_funcs import *


sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent))
# path_total = '../'

path_total = 'https://raw.githubusercontent.com/juntongsu/totallymakescents/refs/heads/main/'
path_app = path_total + 'app/'
path_data = path_total + 'data/'

# -------------------------------------------------------------------------
# Title
# -------------------------------------------------------------------------
st.set_page_config(
    page_title='Perfume of the Day',
    layout="wide",                # ← uses the full width
    initial_sidebar_state="auto"  # optional
)

st.title('Perfume of the Day')

st.write(':material/calendar_today: ', datetime.date.today())

# -------------------------------------------------------------------------
# Load data and choose perfume of the day
# -------------------------------------------------------------------------
today = datetime.date.toordinal(datetime.date.today())
df_fra_standard = pd.read_csv(f'{path_data}fra_standard.csv')
index_potd = df_fra_standard.sample(1, random_state=today).index[0]
potd = df_fra_standard.iloc[index_potd]

# -------------------------------------------------------------------------
# Scrape perfume of the day
# -------------------------------------------------------------------------
accord_data, description, rating, longevity, sillage, fem_masc, price, environment = scrape_perfume(potd['url'])

# Compute scores
longevity_score = (100*np.dot(longevity,range(5))/5).round(2)
sillage_score   = (100*np.dot(sillage,range(4))/4).round(2)
gender_score    = (100*np.dot(fem_masc,range(5))/5).round(2)
price_score     = (100*np.dot(price,range(5))/5).round(2)
rating_score    = round(100.0*rating/5,2)

# -------------------------------------------------------------------------
# Display Perfume Information
# -------------------------------------------------------------------------

col1, col2 = st.columns([1,10])
with col1:
    img = get_img_fragrantica(potd['url'])
    st.image(image = img,
            width = 100,
            use_container_width = False)
with col2:
    # Name, Brand, Link
    st.header(':material/fragrance: {name} by {brand}'.format(name=potd['Perfume'],brand=potd['Brand']))
    st.link_button(
        'Find more details and Reviews at Fragrantica.com :material/arrow_outward: ',
        f"{potd['url']}",
    )

col1, col2, col3 = st.columns([2, 2, 2])

# Radar Chart
with col1:
    radar_chart(longevity_score, sillage_score, gender_score, price_score, rating_score)

# Accords and Notes
with col2:
    st.subheader('𓏊 Notes')
    st.write(f":material/clock_loader_10: Top: {potd['Top']}")
    st.write(f":material/clock_loader_40: Middle: {potd['Middle']}")
    st.write(f":material/clock_loader_90: Base: {potd['Base']}")
    st.subheader(':material/ent: Main Accords')
    display_accords(accord_data)

# Environment Information
with col3:
    environment_chart(environment)