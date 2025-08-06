# -------------------------------------------------------------------------
# Import libraries
# -------------------------------------------------------------------------
import streamlit as st 
import numpy as np
import pandas as pd
import pathlib
import time
import sys

# Deep Learning
# -------------------------------------------------------------------------
import torch
# add

# Web Scraping
# -------------------------------------------------------------------------
from bs4 import BeautifulSoup
from selenium import webdriver


#from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.chrome.service import Service as ChromeService
#from webdriver_manager.firefox import GeckoDriverManager
#from selenium.webdriver.chrome.options import Options

from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as GeckoService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait

#from splinter import Browser
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.by import By
#from selenium_stealth import stealth


# Extras
# -------------------------------------------------------------------------
from streamlit_extras.let_it_rain import rain
from streamlit_extras.grid import grid
from streamlit.components.v1 import html

from pages.helper_funcs import *

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent))

# -------------------------------------------------------------------------
# Set up and Loading Models
# -------------------------------------------------------------------------

# Path to access data files non-locally.
#       Concatenate with 'app/', 'data/', or 'recommender/'
#       to access those respective directories
path = 'https://raw.githubusercontent.com/juntongsu/totallymakescents/refs/heads/main/'
path_image = path + 'app/images/'

st.set_page_config(
    page_title='TotallyMakeScents Max',
    layout="wide",                # ← enables full-width mode
    initial_sidebar_state="auto"  # optional
)

# add model loading


# -------------------------------------------------------------------------
# Logo and User Input
# -------------------------------------------------------------------------
col1, col2 = st.columns([2, 4])

with col1:
    # Logo
    # -------------------------------------------------------------------------
    st.image(image = path_image + 'tms-logo.png',
            width = 320,
            use_container_width = False)

with col2:
    # Title
    # -------------------------------------------------------------------------
    st.header('TotallyMakesScents.')

    # Rotating Subheaders
    # -------------------------------------------------------------------------
    subheaders = ['What does it smell like in the rain, at the end of a hiking trail full of blossoms?',
                "What fragrance would a wizard wear in a magical world?",
                "I'm looking for a bittersweet scent for a farewell party.",
                "What perfumes smell like a lake-side restaurant?",
                "What fragrances embody the smell of castle ruins?",
                "What olfactory notes would capture the feeling of an airy apothecary?",
                "Which perfumes best embody a romantic getaway?"]

    # total_duration = num_sentences * per_sentence_duration
    per_sentence_duration = 6  # seconds per sentence
    total_duration = len(subheaders) * per_sentence_duration

    # keyframe percentages for 1s fade-in, 2s hold, 1s fade-out:
    fade_in_pct_end = 100 * (per_sentence_duration - 3) / total_duration  # 1s fade-in
    hold_start = fade_in_pct_end
    hold_end = 100 * (per_sentence_duration - 1) / total_duration         # end of hold
    fade_out_pct_start = hold_end

    css = f"""
    <style>
    .rotator {{
    position: relative;
    height: 2em;
    overflow: hidden;
    }}
    .rotator span {{
    position: absolute;
    width: 100%;
    opacity: 0;
    color: white;
    text-align: center;
    animation: rotate {total_duration}s ease-in-out infinite;
    }}
    {"".join(
        f".rotator span:nth-child({i+1}) {{ animation-delay: {i * per_sentence_duration}s; }}"
        for i in range(len(subheaders))
    )}
    @keyframes rotate {{
    0%, {fade_out_pct_start}%, 100% {{ opacity: 0; }}
    {(fade_in_pct_end/2):.3f}%, {fade_in_pct_end:.3f}% {{ opacity: 1; }}
    {hold_start:.3f}%, {hold_end:.3f}% {{ opacity: 1; }}
    {hold_end:.3f}%, {fade_out_pct_start:.3f}% {{ opacity: 0; }}
    }}
    </style>
    <div class="rotator">
    {''.join(f'<span>{s}</span>' for s in subheaders)}
    </div>
    """

    html(css, height=25)

    # User Input
    # -------------------------------------------------------------------------
    st.markdown('<p style="margin:0 0 4px 0; font-size:1.1em;">Tell us your story, and we will...</p>',
            unsafe_allow_html=True
    )
    user_input = st.text_area(label='', 
                            placeholder='Enter your scent inspiration here...',
                            label_visibility='hidden',
                            height=68)

    generate_recommendations = st.button('MakeScents')



# -------------------------------------------------------------------------
# User query based recommender
# Input: User description
# Output: Scent recommendations
# -------------------------------------------------------------------------

if generate_recommendations:
    if user_input:
        rain(emoji="👃",font_size=54,falling_speed=3,animation_length="1")
        with st.spinner('Generating scents...'):
            st.write('Recommender goes here.')
    #       
    #
    #  Recommender code goes here
    #
    #
    else:
        st.warning('Please enter a prompt.')

# -------------------------------------------------------------------------
# Perfume Preferences 
# Input: perfume likes and dislikes
# -------------------------------------------------------------------------



# -------------------------------------------------------------------------
# Sidebar - Credits / About Us
# -------------------------------------------------------------------------

# with st.sidebar.expander('About this app'):
#     st.write('This app does [blank] and was made by [blank].')
#     st.write('Contributors:\n- Elly \n- Fernando\n- Katherine \n- Su')

# -------------------------------------------------------------------------
# Testing
# -------------------------------------------------------------------------

# rain(emoji="👃",font_size=54,falling_speed=5,animation_length="10")

