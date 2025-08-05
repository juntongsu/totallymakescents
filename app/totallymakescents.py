# Standard libraries
import streamlit as st
import pandas as pd
import numpy as np

# Pages
pages = {
    'Find Scents': [
        st.Page('pages/tms1.py', title = 'TotallyMakeScents Lite', icon = ':material/search:'),
        st.Page('pages/tms_pro.py', title = 'TotallyMakeScents Pro', icon = ':material/database_search:'),
        st.Page('pages/home.py', title = 'TotallyMakeScents Max', icon = ':material/travel_explore:'),
    ],
    'Explore': [
        st.Page('pages/tms_newbee.py', title = 'Totally New', icon = ':material/psychology_alt:'),
        st.Page('pages/tms_potd.py', title = 'POTD', icon = ':material/calendar_today:'),
    ],
    'About': [
        st.Page('pages/about_us.py', title = 'Meet the Team', icon = ':material/person:'),
        st.Page('pages/help.py', title = 'Help', icon = ':material/help:'),
    ]
}

pg = st.navigation(pages)
pg.run()