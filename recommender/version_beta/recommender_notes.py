import os
import sys
import glob
import string
# import random
from recommender_notes_func import *

home = '../../'
# path_plots = home + 'totallymakescents/plots/'
path_data = home + 'data/'

df_persian = pd.read_csv(path_data + 'Persian_Data.csv')

#####
### language: the dataset we choose to use for the notes. 
# language == 0 : use Fragrantica dataset, and the notes are in English
# language == 1 : use Aromo dataset, and the notes are in Russian-English
#####
language = 1

# Read the datasets and find overlapping perfumes
if language == 0:
    df_fra = pd.read_csv(path_data + 'fra_cleaned.csv', sep=';', encoding='latin-1')
    perf_overlap = find_overlap(df_persian, df_fra, language)
elif language == 1:
    df_aromo = pd.read_csv(path_data + 'aromo_ru.csv', sep=';')#, dtype={'rating_values': np.int64, 'rating_counts': str})
    perf_overlap = find_overlap(df_persian, df_aromo, language)

#####
# Vectorization of the notes
### Top notes: 
# Duration: Shortest lasting, typically evaporating within minutes.
# Purpose: To create a first, captivating impression. 
### Middle notes:
# Duration: Last longer than top notes, often lasting for several hours.
# Purpose: To provide the core and character of the fragrance. 
### Base notes:
# Duration: Longest lasting, lingering for hours or even days.
# Purpose: To provide depth, longevity, and a foundation for the fragrance. 
#####
if language == 0:
    perf_names, vec_top, vec_mid, vec_base = notes_vec_prep(perf_overlap, df_fra, language)
elif language == 1:
        perf_names, vec_top, vec_mid, vec_base = notes_vec_prep(perf_overlap, df_aromo, language)


#####
# Get input from our client(s). For now this is our only devine client from input.csv
# Vectorization of the input
### temperature: the weight we give to different notes. 
# An array of length 4, with values carefully chosen by the product manager (me)
# Generate the list of perfumes
#####
nUsers = 1
for i in range(nUsers):
    user_perfume, user_sentiment = input_perfume()
    user_top, user_mid, user_base = user_vec_prep(user_perfume, user_sentiment, perf_names, vec_top, vec_mid, vec_base)
    temperature = np.array((1, 2, 1, 1.5), dtype=int)
    rec_list = recommender_notes(perf_names, vec_top, vec_mid, vec_base, user_perfume, user_top, user_mid, user_base, temperature)