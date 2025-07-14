import streamlit as st

pages = {
    'Find Scents': [
        st.Page('pages/tms1.py', title = 'TotallyMakeScents', icon = ':material/search:'),
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