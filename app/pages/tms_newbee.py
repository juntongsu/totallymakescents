import streamlit as st 

st.title('Totally New to Perfumes')

with st.expander('Suggested Search'):
    st.link_button('blossoms', '')
    st.link_button('bittersweet farewell party', '')
    st.link_button('wizard and witchcraft ', '')

with st.expander('Try These Scents'):
    st.link_button('citrus', '')
    st.link_button('extinguished candles', '')
    st.link_button('wood and forest', '')