import streamlit as st 
import pandas as pd 
import numpy as np 
import sys 
import pathlib
import time
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))
# path_total = '../'

path_total = 'https://raw.githubusercontent.com/juntongsu/totallymakescents/refs/heads/main/'
path_app = path_total + 'app/'
path_data = path_total + 'data/'
path_rec = path_total + 'recommender/'

from recommender.version_delta.recommender_func import *

st.title('Perfume of the Day')

df_fra_standard = pd.read_csv('{}fra_standard.csv'.format(path_data))

potd = df_fra_standard.sample(1)

potd

st.subheader('{}'.format(potd['Perfume'].values))
st.text('Brand: {}'.format(potd['Brand'].values))
st.text('Top Notes: {}'.format(potd['Top'].values))
st.text('Middle Notes: {}'.format(potd['Middle'].values))
st.text('Base Notes: {}'.format(potd['Base'].values))
st.text('Main Accords: {} {} {}'.format(potd['mainaccord1'].values, potd['mainaccord2'].values, potd['mainaccord3'].values))
# st.link_button('Info and Reviews', '{}'.format(potd['url'].values))