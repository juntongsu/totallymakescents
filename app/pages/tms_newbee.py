import streamlit as st 

path_total = 'https://raw.githubusercontent.com/juntongsu/totallymakescents/refs/heads/main/'
path_app = path_total + 'app/'
path_image = path_app + 'images/'

st.set_page_config(
    page_title='Exhibition Room',
    layout="centered",
    initial_sidebar_state="auto"  # optional
)

col1, col2 = st.columns([2, 6])
with col1:
    # Logo
    # -------------------------------------------------------------------------
    st.image(image = path_image + 'tms-logo.png',
            width = 320,
            use_container_width = False)
with col2:
    st.title('Exhibition Room')

# with st.expander('Suggested Search'):
with st.container(border=True):
    st.link_button('blossoms', '')
    st.link_button('bittersweet farewell party', '')
    st.link_button('wizard and witchcraft ', '')

with st.container(border=True):
# with st.expander('Try These Scents'):
    st.link_button('citrus', '')
    st.link_button('extinguished candles', '')
    st.link_button('wood and forest', '')