# -------------------------------------------------------------------------
# Import libraries
# -------------------------------------------------------------------------
import streamlit as st 
import pandas as pd
import numpy as np

# For scraping
from selenium import webdriver
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import time

# Extras
#from streamlit_autorefresh import st_autorefresh
from streamlit_extras.let_it_rain import rain
from streamlit_extras.grid import grid
from streamlit.components.v1 import html

# import requests
import pathlib
import sys


from bs4 import BeautifulSoup

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent))

# -------------------------------------------------------------------------
# Set up 
# -------------------------------------------------------------------------

# Path to access data files non-locally.
#       Concatenate with 'app/', 'data/', or 'recommender/'
#       to access those respective directories
path = 'https://raw.githubusercontent.com/juntongsu/totallymakescents/refs/heads/main/'

# -------------------------------------------------------------------------
# Testing
# -------------------------------------------------------------------------

# rain(emoji="👃",font_size=54,falling_speed=5,animation_length="10",)




# -------------------------------------------------------------------------
# Style (colors, fonts, etc.)
# -------------------------------------------------------------------------

# Theme


# -------------------------------------------------------------------------
# Title and Description
# -------------------------------------------------------------------------
st.title('TotallyMakeScents')
#st.caption('What does it smell like to be in the rain, at the end of a hiking trail full of blossoms?')
#st.caption("What fragrance would a wizard wear in a magical world?")
#st.caption("I'm looking for a bittersweet scent for a farewell party.")

# -------------------------------------------------------------------------
# Rotating Subheaders
# -------------------------------------------------------------------------
subheaders = ['What does it smell like to be in the rain, at the end of a hiking trail full of blossoms?',
            "What fragrance would a wizard wear in a magical world?",
            "I'm looking for a bittersweet scent for a farewell party."]

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

html(css, height=30)


# -------------------------------------------------------------------------
# User query based recommender
# Input: User description
# Output: Scent recommendations
# -------------------------------------------------------------------------
st.markdown('<p style="margin:0 0 4px 0; font-size:1.1em;">Tell us your story, and we will...</p>',
            unsafe_allow_html=True
)
user_input = st.text_area(label='', 
                          placeholder='Enter your scent inspiration here...',
                          label_visibility='hidden',
                          height=68)

generate_recommendations = st.button('MakeScents')

if generate_recommendations:
    # 
    #
    #  Recommender code goes here
    #
    #
    fake_data = {
        'Image': ['img A', 'img B', 'img C'],
        'Perfume Name': ['Perfume A', 'Perfume B', 'Perfume C'],
        'Description': ['A floral scent with hints of jasmine.',
                        'A woody fragrance with notes of cedar.',
                        'A citrusy aroma with a touch of bergamot.']
    }
    st.dataframe(data=pd.DataFrame(fake_data),
                 width=None,
                 height=None,
                 hide_index=True,
                 key=None)

# -------------------------------------------------------------------------
# Perfume Preferences 
# Input: perfume likes and dislikes
# -------------------------------------------------------------------------

st.subheader('Perfume Recommender v1')

# Import original recommender functions
from recommender.version_delta.recommender_func import *

# Load perfumes names csv
perfume_names = pd.read_csv('{}archive/cleaned_perf_names_0.csv'.format(path+'data/'))
perfume_names = perfume_names['Perfume']

# Change multiselect tag color to gray
st.markdown("""<style> span[data-baseweb="tag"] 
            {background-color: gray !important;}
            </style>""", unsafe_allow_html=True)

# Add  multiselect for user likes and dislikes
user_likes, user_dislikes = st.columns(2)

user_likes_multiselect = user_likes.multiselect(
    ':green-background[Add scents that you enjoy:]',
    perfume_names,
    placeholder='Type to search',
    help='''Use the search bar to add your favorite perfumes.
            Add at least 5 scents to get more personalized recommendations.''',
    key='user_likes')

user_dislikes_multiselect = user_dislikes.multiselect(
    ':red-background[Add scents that you avoid:]',
    perfume_names[~perfume_names.isin(user_likes_multiselect)],
    placeholder='Type to search',
    help='Use the search bar to add perfumes you don\'t like.',
    key='user_dislikes')


user_allergy_multiselect = user_dislikes.multiselect(
    ':orange-background[Add scents that you have allergies to:]',
    perfume_names,
    placeholder='Type to search',
    help='Use the search bar to add perfumes you are allergic to.',
    key='user_allergies')


# -------------------------------------------------------------------------
# Fragrantica Perfume Finder 
#   Input: Fragrantica URL, 
#   Output: Image and name of perfume
# -------------------------------------------------------------------------

st.subheader('Fragrantica Perfume Finder')

def get_img_fragrantica(input_url):
    """
    Get image from a Fragrantica URL.
    Input: 
        https://www.fragrantica.com/perfume/brand-name/perfume-name-{perfume_id}.html
    Output:
        'https://fimgs.net/mdimg/perfume-thumbs/375x500.{perfume_id}.jpg'
    """
    perfume_id = input_url.split('-')[-1].split('.')[0]
    image = f'https://fimgs.net/mdimg/perfume-thumbs/375x500.{perfume_id}.jpg'
    return image

def get_name_fragrantica(input_url):
    """
    Get name from a Fragrantica URL.
    Input: 
        https://www.fragrantica.com/perfume/brand-name/perfume-name-123456.html
    Output:
        ('brand-name', 'perfume-name')
    """
    # Get list with ['brand-name', 'perfume-name-123456.html']
    full_name = input_url.split('/')[-2:]   
    # Get brand name
    brand = full_name[0].replace('-', ' ')
    # Get perfume name
    perfume_name = ' '.join(full_name[1].split('.')[0].split('-')[:-1])
    return brand, perfume_name

def print_fragrantica_url_info(input_url):
    """
    Runs get_img_fragrantica and get_name_fragrantica
    and prints them to the screen
    when user adds a valid Fragrantica URL.
    Input: 
        https://www.fragrantica.com/perfume/brand-name/perfume-name-123456.html
    Output:
        None (displays image and text in app)
    """
    img_col, txt_col = st.columns(2)
    with img_col:
        image = get_img_fragrantica(input_url)
        st.image(image)
    with txt_col:
        brand, name = get_name_fragrantica(url)
        st.write('Brand:',brand)
        st.write('Perfume:', name)
        st.write('Potency:')
        st.write('Duration:')
        st.write('Notes:')

# Ask user for url
url = st.text_input('Paste a Fragrantica URL:', placeholder='paste URL here')

# Generates image and information about the perfume
if url.startswith('https://www.fragrantica.com/perfume'):
    print_fragrantica_url_info(url)   
else:
    st.error('Invalid URL. Please check the format and try again.')




# -------------------------------------------------------------------------
# Sidebar - Credits / About Us
# -------------------------------------------------------------------------

# with st.sidebar.expander('About this app'):
#     st.write('This app does [blank] and was made by [blank].')
#     st.write('Contributors:\n- Elly \n- Fernando\n- Katherine \n- Su')