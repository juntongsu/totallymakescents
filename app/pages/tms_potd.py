import streamlit as st 
import pandas as pd 
import numpy as np 
import sys 
import pathlib
import datetime
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent))
# path_total = '../'

path_total = 'https://raw.githubusercontent.com/juntongsu/totallymakescents/refs/heads/main/'
path_app = path_total + 'app/'
path_data = path_total + 'data/'
path_rec = path_total + 'recommender/'

from recommender.version_delta.recommender_func import *

st.title('Perfume of the Day')

df_fra_standard = pd.read_csv('{}fra_standard.csv'.format(path_data))

st.write(':material/calendar_today: ', datetime.date.today())

today = datetime.date.toordinal(datetime.date.today())
index_potd = df_fra_standard.sample(1, random_state=today).index[0]
potd = df_fra_standard.iloc[index_potd]

st.subheader(':material/fragrance: {}'.format(potd['Perfume']))
# st.write(':material/branding_watermark: Brand: {}'.format(potd['Brand']))

col1, col2 = st.columns([1,2])
with col1:
    st.write(':material/branding_watermark: Brand')
    st.write(':material/ent: Main Accords')
    st.write(':material/clock_loader_10: Top Notes')
    st.write(':material/clock_loader_40: Middle Notes')
    st.write(':material/clock_loader_90: Base Notes')
    
with col2:
    st.write('{}'.format(potd['Brand']))
    st.write('{}, {}, {}, {}, and {}'.format(potd['mainaccord1'], 
                                            potd['mainaccord2'], 
                                            potd['mainaccord3'], 
                                            potd['mainaccord4'], 
                                            potd['mainaccord5']))
    st.write('{}'.format(potd['Top']))
    st.write('{}'.format(potd['Middle']))
    st.write('{}'.format(potd['Base']))

# st.write('Top Notes: {}'.format(potd['Top']))
# st.write('Middle Notes: {}'.format(potd['Middle']))
# st.write('Base Notes: {}'.format(potd['Base']))
# st.write('Main Accords: {}, {}, {}, {}, and {}'.format(potd['mainaccord1'], potd['mainaccord2'], potd['mainaccord3'], potd['mainaccord4'], potd['mainaccord5']))
st.link_button('Details and Reviews on Fragrantica.com :material/arrow_outward: ', '{}'.format(potd['url']))