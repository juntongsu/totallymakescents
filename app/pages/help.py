import streamlit as st 

path_total = 'https://raw.githubusercontent.com/juntongsu/totallymakescents/refs/heads/main/'

st.title('Help')

st.link_button('README', '{}README.md'.format(path_total))
st.link_button('Project Github', 'https://github.com/juntongsu/totallymakescents')
st.link_button('I Need REAL Help!', '')