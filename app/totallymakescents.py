import streamlit as st 
import pandas as pd 
import numpy as np 
import sys 
sys.path.append('../')

path_total = 'https://raw.githubusercontent.com/juntongsu/totallymakescents/refs/heads/main/'
path_app = path_total + 'app/'
path_data = path_total + 'data/'
path_rec = path_total + 'recommender/'

from recommender.version_gamma.recommender_notes_func import *
from recommender.version_gamma.recommender_users_func import *

# user_frame = pd.read_csv('{}input.csv'.format(path_app), header=None)
# user_frame.columns = ["Perfume Name", "Sentiment"]

st.title('TotallyMakeScents')

# st.text('What’s it smell like in the rain, at the end of a hiking trail full of blossoms?')
# st.text('What fragrance would a wizard wear in a magical world?')
# st.text('Looking for a bittersweet scent for a farewell party.')
# st.subheader('Tell us about your stroy, and we MAKESCENTS.')
st.write("What’s it smell like in the rain, at the end of a hiking trail full of blossoms? What fragrance would a wizard wear in a magical world? Looking for a bittersweet scent for a farewell party. Tell us about your stroy, and we MAKESCENTS.")

language = 0
df_perf_names = pd.read_csv('{}cleaned_perf_names_{}.csv'.format(path_data, language))
perf_names = df_perf_names['Perfume']
sentiment_list = ['I like it!', "I don't like it."]

# input_left_column_0, input_right_column_0 = st.columns(2)
client_perfume_0 = st.multiselect(
    'You like these perfumes:',
    perf_names,
    placeholder='Type to search in the library',
    help='I like it!',
    key='client_perfume_0')
# client_sentiemnt_0 = input_right_column_0.selectbox(
#     '',
#     sentiment_list,
#     key='client_sentiemnt_0')

input_left_column_1, input_right_column_1 = st.columns(2)
client_perfume_1 = input_left_column_1.multiselect(
    'You avoid these perfumes',
    perf_names,
    placeholder='Type to search in the library',
    help='Allergy help',
    key='client_perfume_1')
client_allergy_switch = input_right_column_1.toggle('You have allergy to one or more of these.')
if client_allergy_switch:
    client_sentiemnt_1 = input_right_column_1.multiselect(
        '',
        client_perfume_1,
        placeholder='Please specify',
        key='client_sentiemnt_1')

EI_slider = st.select_slider(
    'Your MBTI',
    options = [
        'Extremely Extraverted (E)',
        'Extraverted',
        'Just A Little E',
        'Neutral',
        'Just A Little I',
        'Introverted', 
        'Extremely Introverted (I)'],
    value = ('Neutral'),
    key='ei_slider',
    help='Popularity slider. Placeholder slider. The real note-user slider. Placeholder slider.'
)

ns_slider = st.select_slider(
    'Your MBTI',
    options = [
        'Extremely Intuitive (N)',
        'Intuitive (N)',
        'Just A Little N',
        'Neutral',
        'Just A Little S',
        'Observant (S)', 
        'Extremely Observant (S)'],
    value = ('Neutral'),
    key='ns_slider',
    label_visibility='collapsed',
    help='This is a placeholder slider.'
)

tf_slider = st.select_slider(
    'Your MBTI',
    options = [
        'Extremely Thinking (T)',
        'Thinking (T)',
        'Just A Little T',
        'Neutral',
        'Just A Little F',
        'Feeling (F)', 
        'Extremely Feeling (F)'],
    value = ('Neutral'),
    key='tf_slider',
    label_visibility='collapsed',
    help='This is the real note-user slider.'
)

jp_slider = st.select_slider(
    'Your MBTI',
    options = [
        'Extremely Judging (J)',
        'Judging (J)',
        'Just A Little J',
        'Neutral',
        'Just A Little P',
        'Prospecting (P)', 
        'Extremely Prospecting (P)'],
    value = ('Neutral'),
    key='jp_slider',
    label_visibility='collapsed',
    help='This is a placeholder slider.'
)

button_left_column, button_mid_column, button_right_column = st.columns(3)
button_mid_column.button(
    'Totally Make Scents!',
    type='primary')