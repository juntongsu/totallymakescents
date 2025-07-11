import streamlit as st 

img_path = 'https://raw.githubusercontent.com/juntongsu/totallymakescents/refs/heads/main/app/images/'

st.title('About Us')

st.subheader('Elly')
img1,txt1 = st.columns(2)
img1.image(img_path+'elly.png')
txt1.write('(https://github.com/ellydo17)')
txt1.write('I like to travel!')

st.subheader('Fernando')
img2,txt2 = st.columns(2)
img2.image(img_path+'fernando.jpg')
txt2.write('(https://github.com/fernando-liu-lopez)')
txt2.write('[fill]')

st.subheader('Katherine')
img3,txt3 = st.columns(2)
img3.image(img_path+'katherine.jpg')
txt3.write('(https://github.com/kmerkl22)')
txt3.write('I enjoy reading and painting.')

st.subheader('Su')
img4,txt4 = st.columns(2)
img4.image(img_path+'su.jpg')
txt4.write('(https://juntongsu.github.io/#)')
txt4.write('Panda, an animal, eats shoots and leaves')