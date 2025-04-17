import streamlit as st 
import pandas as pd 
import numpy as np 

user_frame = pd.read_csv('./input.csv', header=None)
user_frame.columns = ["Perfume Name", "Sentiment"]

sentiment_list = ['I like it!', "I don't like it."]

st.title('TotallyMakeScents')

# st.text('What’s it smell like in the rain, at the end of a hiking trail full of blossoms?')
# st.text('What fragrance would a wizard wear in a magical world?')
# st.text('Looking for a bittersweet scent for a farewell party.')
st.text("What’s it smell like in the rain, at the end of a hiking trail full of blossoms? What fragrance would a wizard wear in a magical world? Looking for a bittersweet scent for a farewell party. ")

input_left_column_0, input_right_column_0 = st.columns(2)
client_perfume_0 = input_left_column_0.selectbox(
    'Tell us about your story:',
    user_frame['Perfume Name'],
    key='client_perfume_0')
client_sentiemnt_0 = input_right_column_0.selectbox(
    '',
    sentiment_list,
    key='client_sentiemnt_0')

input_left_column_1, input_right_column_1 = st.columns(2)
client_perfume_1 = input_left_column_1.selectbox(
    '',
    user_frame['Perfume Name'],
    key='client_perfume_1')
client_sentiemnt_1 = input_right_column_1.selectbox(
    '',
    sentiment_list,
    key='client_sentiemnt_1')

input_left_column_2, input_right_column_2 = st.columns(2)
client_perfume_2 = input_left_column_2.selectbox(
    '',
    user_frame['Perfume Name'],
    key='client_perfume_2')
client_sentiemnt_2 = input_right_column_2.selectbox(
    '',
    sentiment_list,
    key='client_sentiemnt_2')

input_left_column_3, input_right_column_3 = st.columns(2)
client_perfume_3 = input_left_column_3.selectbox(
    '',
    user_frame['Perfume Name'],
    key='client_perfume_3')
client_sentiemnt_3 = input_right_column_3.selectbox(
    '',
    sentiment_list,
    key='client_sentiemnt_3')

input_left_column_4, input_right_column_4 = st.columns(2)
client_perfume_4 = input_left_column_4.selectbox(
    '',
    user_frame['Perfume Name'],
    key='client_perfume_4')
client_sentiemnt_4 = input_right_column_4.selectbox(
    '',
    sentiment_list,
    key='client_sentiemnt_4')

side_slider = st.sidebar.select_slider(
    'Your MBTI',
    options = [
        'Extreme Extrovert',
        'Extrovert',
        'Just A Little E',
        'Neutral',
        'Just A Little I',
        'Introvert', 
        'Extreme Introvert'],
    value = ('Neutral'),
    key='side_slider',
    help='I'
)

down_slider = st.select_slider(
    'Your MBTI',
    options = [
        'Extreme Extrovert',
        'Extrovert',
        'Just A Little E',
        'Neutral',
        'Just A Little I',
        'Introvert', 
        'Extreme Introvert'],
    value = ('Neutral'),
    key='down_slider',
    help='I'
)

st.button('Make Scents!')