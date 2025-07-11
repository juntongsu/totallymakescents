import streamlit as st

pages = {
    'Find Scents': [
        st.Page('pages/tms1.py', title = 'TotallyMakeScents', icon = ':material/search:'),
        st.Page('pages/tms_newbee.py', title = 'Totally New'),
        st.Page('pages/tms_potd.py', title = 'POTD'),
    ],
    'About': [
        st.Page('pages/about_us.py', title = 'Meet the Team'),
        st.Page('pages/help.py', title = 'Help'),
    ]
}

pg = st.navigation(pages, position='top')
pg.run()