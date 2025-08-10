# Standard libraries
import streamlit as st
import pandas as pd
import numpy as np

path_total = 'https://raw.githubusercontent.com/juntongsu/totallymakescents/refs/heads/main/'
path_image = path_total + 'app/images/'

st.logo(image = path_image + 'tms-logo.png',
        size = 'large')

# Pages
pages = {
    'Find Scents': [
        st.Page('pages/tms_home.py', title = 'TotallyMakeScents', icon = ':material/travel_explore:'),
        st.Page('pages/tms_lite.py', title = 'TotallyMakeScents Lite', icon = ':material/search:'),
        st.Page('pages/tms_pro.py', title = 'TotallyMakeScents Pro', icon = ':material/database_search:')
    ],
    'Explore': [
        st.Page('pages/explore_exhibition.py', title = 'Exhibition Room', icon = ':material/wall_art:'),
        st.Page('pages/explore_potd.py', title = 'Perfume of the Day', icon = ':material/calendar_today:'),
        st.Page('pages/explore_tableau.py', title = 'Our Data', icon = ':material/table_chart_view:'),
    ],
    'About': [
        st.Page('pages/about_us.py', title = 'Meet the Team', icon = ':material/person:'),
        st.Page('pages/about_readme.py', title = 'README', icon = ':material/menu_book:'),
        st.Page('pages/about_help.py', title = 'Help', icon = ':material/help:'),
    ]
}


pg = st.navigation(pages)
pg.run()