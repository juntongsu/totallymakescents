# -------------------------------------------------------------------------
# Import libraries
# -------------------------------------------------------------------------
import streamlit as st 
import pandas as pd
import numpy as np

import requests
import pathlib
import sys
import time

from bs4 import BeautifulSoup

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))

# -------------------------------------------------------------------------
# Set up 
# -------------------------------------------------------------------------

# Path to access data files non-locally.
#       Concatenate with 'app/', 'data/', or 'recommender/'
#       to access those respective directories
path = 'https://raw.githubusercontent.com/juntongsu/totallymakescents/refs/heads/main/app'

# -------------------------------------------------------------------------
# Style (colors, fonts, etc.)
# -------------------------------------------------------------------------

# Theme


# -------------------------------------------------------------------------
# Title and Description
# -------------------------------------------------------------------------
st.title('TotallyMakeScents')
st.caption('What does it smell like to be in the rain, at the end of a hiking trail full of blossoms?')
st.caption("What fragrance would a wizard wear in a magical world?")
st.caption("I'm looking for a bittersweet scent for a farewell party.")


# -------------------------------------------------------------------------
# User query based recommender
# Input: User description
# Output: Scent recommendations
# -------------------------------------------------------------------------

user_input = st.text_area('Tell us your story, and we will MakeScents:', 
                          placeholder='Enter your scent inspiration here...')

if st.button('MakeScents'):
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
else:
    st.warning('Please enter a description to get scent recommendations.')


# -------------------------------------------------------------------------
# Perfume Preferences 
# Input: perfume likes and dislikes
# -------------------------------------------------------------------------

st.subheader('Perfume Recommender v1')

# Import original recommender functions
from recommender.version_delta.recommender_func import *

# Load perfumes names csv
perfume_names = pd.read_csv('{}cleaned_perf_names_0.csv'.format(path+'data/'))
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

mbti_slider = st.select_slider(
    label = 'Your MBTI',
    options = [1,2,3,4,5],
    value=3)

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

with st.sidebar.expander('About this app'):
    st.write('This app does [blank] and was made by [blank].')
    st.write('Contributors:\n- Elly \n- Fernando\n- Katherine \n- Su')