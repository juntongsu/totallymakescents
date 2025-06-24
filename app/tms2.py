import streamlit as st 
import pandas as pd
import numpy as np

import requests
import pathlib
import sys
import time


# To add a page, add it here following the format below.
# Finally, add the page to the st.navigation list at the end.

# Home page (recommender)
home_page = st.Page(
    'tms2.py',                  #filename that creates this page
    title = 'Find Scents',      # page title
    icon = ':material/search:'  # emoji icons 
)

# About us page
about_us = st.Page(
    'pages/about_us.py',
    title = 'About Us'
)



#---------------------------------------------------------
# List all pages on the list below
pg = st.navigation([home_page, about_us])
pg.run()