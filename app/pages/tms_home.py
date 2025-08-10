# -------------------------------------------------------------------------
# Import libraries
# -------------------------------------------------------------------------
import streamlit as st
from streamlit_extras.let_it_rain import rain

import numpy as np
import pandas as pd

import sys
import pathlib
import datetime

from streamlit_extras.let_it_rain import rain

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent))
# from pages.helper_funcs import *
from recommender.version_epsilon.helper_funcs import *

path_total = 'https://raw.githubusercontent.com/juntongsu/totallymakescents/refs/heads/main/'
path_image = path_total + 'app/images/'
path_data = path_total + 'data/'

#--------------------------HOME PAGE---------------------------------------------
st.set_page_config(
    page_title='TotallyMakeScents',
    layout="wide",                # ← enables full-width mode
    initial_sidebar_state="auto"  # optional
)
# -------------------------------------------------------------------------
# Logo and User Input
# -------------------------------------------------------------------------
col1, col2 = st.columns([2, 4])

with col1:
    # Logo
    # -------------------------------------------------------------------------
    st.image(image = path_image + 'tms-logo.png',
            width = 320,
            use_container_width = False)

with col2:
    # Title
    # -------------------------------------------------------------------------
    st.header('TotallyMakeScents.')

    # Rotating Subheaders
    # -------------------------------------------------------------------------
    subheaders = ['What does it smell like in the rain, at the end of a hiking trail full of blossoms?',
                "What fragrance would a wizard wear in a magical world?",
                "I'm looking for a bittersweet scent for a farewell party.",
                "What perfumes smell like a lake-side restaurant?",
                "What fragrances embody the smell of castle ruins?",
                "What olfactory notes would capture the feeling of an airy apothecary?",
                "Which perfumes best embody a romantic getaway?"]

    # total_duration = num_sentences * per_sentence_duration
    per_sentence_duration = 6  # seconds per sentence
    total_duration = len(subheaders) * per_sentence_duration

    # keyframe percentages for 1s fade-in, 2s hold, 1s fade-out:
    fade_in_pct_end = 100 * (per_sentence_duration - 3) / total_duration  # 1s fade-in
    hold_start = fade_in_pct_end
    hold_end = 100 * (per_sentence_duration - 1) / total_duration         # end of hold
    fade_out_pct_start = hold_end

    css = f"""
    <style>
    .rotator {{
    position: relative;
    height: 2em;
    overflow: hidden;
    }}
    .rotator span {{
    position: absolute;
    width: 100%;
    opacity: 0;
    color: grey;
    text-align: center;
    animation: rotate {total_duration}s ease-in-out infinite;
    }}
    {"".join(
        f".rotator span:nth-child({i+1}) {{ animation-delay: {i * per_sentence_duration}s; }}"
        for i in range(len(subheaders))
    )}
    @keyframes rotate {{
    0%, {fade_out_pct_start}%, 100% {{ opacity: 0; }}
    {(fade_in_pct_end/2):.3f}%, {fade_in_pct_end:.3f}% {{ opacity: 1; }}
    {hold_start:.3f}%, {hold_end:.3f}% {{ opacity: 1; }}
    {hold_end:.3f}%, {fade_out_pct_start:.3f}% {{ opacity: 0; }}
    }}
    </style>
    <div class="rotator">
    {''.join(f'<span>{s}</span>' for s in subheaders)}
    </div>
    """

    st.markdown(css, unsafe_allow_html=True)

    # User Input
    # -------------------------------------------------------------------------
    st.markdown('<p style="margin:0 0 4px 0; font-size:1.1em;">Tell us your story, and we will...</p>',
            unsafe_allow_html=True
    )
    user_input = st.text_area(label='input', 
                            placeholder='Enter your scent inspiration here...',
                            label_visibility='hidden',
                            height=68)

    generate_recommendations = st.button('MakeScents')



# -------------------------------------------------------------------------
# User query based recommender
# Input: User description
# Output: Scent recommendations
# -------------------------------------------------------------------------

if generate_recommendations:
    if user_input:
        rain(emoji="👃",font_size=54,falling_speed=3,animation_length="2")
        today_100 = datetime.date.today().replace(year=datetime.date.today().year - 100)

        st.markdown("Our models require much more resources than what Streamlit Cloud provides. ")
        st.markdown("Instead, we will show you the Perfume of the Day 100 years ago on this date: ")
        st.markdown(f':material/calendar_today: {today_100}')
        # today_100 = datetime.date.toordinal(today_100)
        df_fra_standard = pd.read_csv(f'{path_data}tms_lite/fra_standard.csv')
        index_potd = df_fra_standard.sample(1, random_state=datetime.date.toordinal(today_100)).index[0]
        potd = df_fra_standard.iloc[index_potd]

        accord_data = [ str(potd.get(f'mainaccord{i}', '')) for i in range(1, 6) ]
        # e.g. ['rose', 'woody', fruity, aromatic, floral]
        df_notes_accords = pd.read_csv(f'{path_total}generated_data/notes.csv')

        potd_all_notes = potd['Top'] + ', ' + potd['Middle'] + ', ' + potd['Base']
        potd_all_notes_series = pd.Series(potd_all_notes.split(', '), name='note')
        df_potd_notes_accords = pd.merge(left=potd_all_notes_series, right=df_notes_accords[['note_group', 'note']], how='left', on='note')
        potd_accords = df_potd_notes_accords['note_group'].value_counts()
        st.markdown(' ')

        col1, col2 = st.columns([1,10])
        with col1:
            img = get_img_fragrantica(potd['url'])
            st.image(image = img,
                    width = 100,
                    use_container_width = False)
        with col2:
            # Name, Brand, Link
            st.header(':material/fragrance: {name} by {brand}'.format(name=potd['Perfume'],brand=potd['Brand']))
            st.link_button(
                'Find more details and Reviews at Fragrantica.com :material/arrow_outward: ',
                f"{potd['url']}",
            )

        col1, col2= st.columns([4, 6])

        with col1:
            st.subheader(':material/ent: Accords')
            display_accords(potd_accords)
            
        with col2:
            st.subheader('𓏊 Notes')
            st.write(' ')
            st.write(f":material/clock_loader_10: Top: {potd['Top']}")
            st.write(f":material/clock_loader_40: Middle: {potd['Middle']}")
            st.write(f":material/clock_loader_90: Base: {potd['Base']}")
        
        st.divider()
        st.subheader("Can't get enough of :rainbow[TotallyMakeScents]?")
        st.page_link('pages/explore_exhibition.py', label='Check out some example searches in our Exhibition Room :material/arrow_outward: ', icon='🖼️')
    else:
        st.warning('Please enter a prompt.')