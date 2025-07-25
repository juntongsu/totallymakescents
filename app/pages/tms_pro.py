import streamlit as st 
import pandas as pd 
import numpy as np 
import sys 
import pathlib
import time
from pandas.api.types import (
    is_categorical_dtype,
    is_numeric_dtype,
)

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent))
# path_total = '../'

path_total = 'https://raw.githubusercontent.com/juntongsu/totallymakescents/refs/heads/main/'
path_app = path_total + 'app/'
path_data = path_total + 'data/'
path_rec = path_total + 'recommender/'

from recommender.version_epsilon.recommender_func import *

# user_frame = pd.read_csv('{}input_pro.csv'.format(path_app), header=None)
# user_frame.columns = ["Perfume Name", "Sentiment"]

st.title('TotallyMakeScents')
st.write("What’s it smell like in the rain, at the end of a hiking trail full of blossoms? What fragrance would a wizard wear in a magical world? Looking for a bittersweet scent for a farewell party. Tell us about your story, and we MAKESCENTS.")

df_search = pd.read_parquet('{}search_filter.parquet'.format(path_data))
df_search = df_search.drop(columns=['url'])
filter_columns = pd.Series(['Gender', 'Year', 'Country'], dtype='string')
search_columns = pd.Series(['Perfume', 'Brand', 'Top', 'Middle', 'Base', 'Accords'])

def filter_dataframe(df_search):
    df_filtered = df_search.copy()

    filtering_container = st.container()
    with filtering_container:
        to_filter_columns = st.multiselect('Filter Perfumes on ', filter_columns, key='filter_columns')
        for column in to_filter_columns:
            left_col, right_col = st.columns([1, 20])
            left_col.write(':material/subdirectory_arrow_right:')
            if is_categorical_dtype(df_filtered[column]) or df_filtered[column].nunique() < 10:
                user_cat_input = right_col.multiselect(
                    f"Values for {column}",
                    df_filtered[column].unique(),
                    default=list(df_filtered[column].unique()),
                    key='filter_columns_cat',
                )
                df_filtered = df_filtered[df_filtered[column].isin(user_cat_input)]
            elif is_numeric_dtype(df_filtered[column]):
                _min = int(df_filtered[column].min())
                _max = int(df_filtered[column].max())
                step = 1#(_max - _min) / 100
                user_num_input = right_col.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df_filtered = df_filtered[df_filtered[column].between(*user_num_input)]
            else:
                user_text_input = right_col.text_input(
                    f"Search in {column}",
                )
                if user_text_input:
                    df_filtered = df_filtered[df_filtered[column].astype(str).str.contains(user_text_input, case=False)]
        
        search = st.checkbox('Further Search ', key='search')
        if not search:
            return df_filtered
        
        searching_container = st.container()
        with searching_container:
            to_search_columns = st.multiselect('Search Perfumes on ', search_columns, key='search_columns')
            for column in to_search_columns:
                left_col, right_col = st.columns([1, 20])
                left_col.write(':material/subdirectory_arrow_right:')
                user_text_input = right_col.text_input(
                    f"Search in {column}",
                )
                if user_text_input:
                    df_filtered = df_filtered[df_filtered[column].astype(str).str.contains(user_text_input, case=False)]
    return df_filtered

client_perfume_0 = st.multiselect(
    'Add scents that you enjoy:',
    df_search['Perfume'],
    placeholder='Type to search in the library',
    help='I like it!',
    key='client_perfume_0')

filter_0 = st.checkbox('Select with Filters', key='filter_0')
if filter_0:
    df_filtered_0 = filter_dataframe(df_search)
    df_filtered_selection_0 = st.dataframe(df_filtered_0, on_select='rerun', selection_mode='multi-row', hide_index=False)
    client_perfume_0 = df_filtered_0.iloc[df_filtered_selection_0['selection']['rows']]
    client_perfume_0 = client_perfume_0['Perfume'].to_list()

client_perfume_1 = st.multiselect(
    'You avoid these perfumes',
    df_search['Perfume'][~df_search['Perfume'].isin(client_perfume_0)],
    placeholder='Type to search in the library',
    help='Allergy help',
    key='client_perfume_1')

# filter_1 = st.checkbox('Select with Filters', key='filter_1')
# if filter_1:
#     df_filtered_1 = filter_dataframe(df_search.drop(index=client_perfume_0.index))
#     df_filtered_selection_1 = st.dataframe(df_filtered_1, on_select='rerun', selection_mode='multi-row', hide_index=False)
#     client_perfume_1 = df_filtered_1.iloc[df_filtered_selection_1['selection']['rows']]

client_allergy_switch = st.toggle('You have allergy to one or more of these.')
if client_allergy_switch:
    client_allergy = st.multiselect(
        '',
        client_perfume_1,
        placeholder='Please specify',
        key='client_allergy')

ei_slider = st.select_slider(
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
    help='Reorder.'
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
make_button = button_mid_column.button(
    'Totally Make Scents!',
    type='primary')

persian_data_frame_clean = pd.read_csv('{}cleaned_persian.csv'.format(path_data))
perf_names = pd.read_parquet('{}perf_names.parquet'.format(path_data))
vec_top = pd.read_parquet('{}vec_top.parquet'.format(path_data))
vec_mid = pd.read_parquet('{}vec_mid.parquet'.format(path_data))
vec_base = pd.read_parquet('{}vec_base.parquet'.format(path_data))
vec_accords = pd.read_parquet('{}vec_accords.parquet'.format(path_data))


dict_slider = {'Extremely Thinking (T)': 0., 'Thinking (T)': 0.2, 'Just A Little T': 0.4, 
            'Neutral': 0.5, 
            'Just A Little F': 0.6, 'Feeling (F)': 0.8, 'Extremely Feeling (F)': 1.}

n_recs = 20

if make_button:
    make_progress_bar = st.progress(0, text='Making Scents...')
    client_perfume = pd.Series((client_perfume_0 + client_perfume_1), dtype='string', name='Perfume Name')
    client_sentiment = pd.Series((np.concatenate((np.ones(len(client_perfume_0), dtype=int), np.ones(len(client_perfume_1), dtype=int)*(-1)))), dtype='int', name='Sentiment')
    df_client = pd.concat([client_perfume, client_sentiment], axis=1)
    client_id = 0 
    client_frame = add_user_id(df_client)
    make_progress_bar.progress(30, text='Making Scents from Users Like You...')

    if len(client_sentiment) == 0:
        recommendation_list = recommender_newbie(path_data)
    elif len(client_perfume_0) == 0:
        make_progress_bar.progress(70, text='Making Scents from the Notes You Like...')
        client_top, client_mid, client_base, user_accords = user_vec_prep(client_perfume, client_sentiment, perf_names, vec_top, vec_mid, vec_base, vec_accords)
        temperature = np.array((1, 2, 1, 1.5), dtype=float)
        note_recommendation_list = recommender_notes(perf_names, vec_top, vec_mid, vec_base, client_perfume, client_top, client_mid, client_base, temperature)
        recommendation_list = note_recommendation_list['Perfume'].reset_index(drop=True)
    elif len(client_sentiment) < 5:
        # user_recommendation_list = lazy_recommender(client_id, client_frame, persian_data_frame_clean)
        user_recommendation_list = recommender_newbie(path_data)
        user_rec_list = user_recommendation_list['Perfume Name'].reset_index(drop=True)
        
        make_progress_bar.progress(70, text='Making Scents from the Notes You Like...')
        client_top, client_mid, client_base, user_accords = user_vec_prep(client_perfume, client_sentiment, perf_names, vec_top, vec_mid, vec_base, vec_accords)
        temperature = np.array((1, 2, 1, 1.5), dtype=float)
        note_recommendation_list = recommender_notes(perf_names, vec_top, vec_mid, vec_base, client_perfume, client_top, client_mid, client_base, temperature)
        note_rec_list = note_recommendation_list['Perfume'].reset_index(drop=True)
        df_rec_list = pd.concat([user_rec_list, note_rec_list], axis=1)

        slider = pd.Series((tf_slider)).replace(dict_slider).values
        recommendation_list = combine_rec_lists(user_rec_list, note_rec_list, n_recs, slider)
    else:
        # user_recommendation_list = recommender_users(client_id, client_frame, persian_data_frame_clean)
        user_recommendation_list = recommender_newbie(path_data)
        user_rec_list = user_recommendation_list['Perfume Name'].reset_index(drop=True)
        
        make_progress_bar.progress(70, text='Making Scents from the Notes You Like...')
        client_top, client_mid, client_base, user_accords = user_vec_prep(client_perfume, client_sentiment, perf_names, vec_top, vec_mid, vec_base, vec_accords)
        temperature = np.array((1, 2, 1, 1.5), dtype=float)
        note_recommendation_list = recommender_notes(perf_names, vec_top, vec_mid, vec_base, client_perfume, client_top, client_mid, client_base, temperature)
        note_rec_list = note_recommendation_list['Perfume'].reset_index(drop=True)
        df_rec_list = pd.concat([user_rec_list, note_rec_list], axis=1)

        slider = pd.Series((tf_slider)).replace(dict_slider).values
        recommendation_list = combine_rec_lists(user_rec_list, note_rec_list, n_recs, slider)
    
    if client_allergy_switch and (len(client_allergy) > 0):
        make_progress_bar.progress(90, text='Checking Allergy...')
        df_fra_standard = df_search
        client_allergy = pd.Series(client_allergy, dtype='string')
        client_allergy_note, rec_list_note, rec_list_allergy_bool = client_allergy_finder(client_perfume, client_allergy, recommendation_list, df_fra_standard)
        output = pd.concat([recommendation_list, rec_list_allergy_bool], axis=1)
    else:
        output = recommendation_list
    
    output
    make_progress_bar.progress(100, text='We Made Some Scents for You')

    time.sleep(1)
    make_progress_bar.empty()