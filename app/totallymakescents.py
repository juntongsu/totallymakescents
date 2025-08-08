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
        st.Page('pages/tms_dl_v1.py', title = 'TotallyMakeScents Max', icon = ':material/travel_explore:'),
        st.Page('pages/tms1.py', title = 'TotallyMakeScents Lite', icon = ':material/search:'),
        st.Page('pages/tms_pro.py', title = 'TotallyMakeScents Pro', icon = ':material/database_search:')
    ],
    'Explore': [
        st.Page('pages/tms_newbee.py', title = 'Totally New', icon = ':material/psychology_alt:'),
        st.Page('pages/tms_potd.py', title = 'Perfume of the Day', icon = ':material/calendar_today:'),
    ],
    'About': [
        st.Page('pages/about_us.py', title = 'Meet the Team', icon = ':material/person:'),
        st.Page('pages/help.py', title = 'Help', icon = ':material/help:'),
    ]
}


pg = st.navigation(pages)
pg.run()