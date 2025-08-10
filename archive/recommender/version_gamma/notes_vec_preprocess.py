home = '../../'
path_data = home + 'data/'

from recommender_notes_func import *

df_persian = pd.read_csv(path_data + 'Persian_Data.csv')

language = 0
if language == 0:
    df_fra = pd.read_csv(path_data + 'fra_cleaned.csv', sep=';', encoding='latin-1')
    perf_overlap = find_overlap(df_persian, df_fra, language)
    perf_names, vec_top, vec_mid, vec_base = notes_vec_prep(perf_overlap, df_fra, language)
elif language == 1:
    df_aromo = pd.read_csv(path_data + 'aromo_ru.csv', sep=';', dtype=object)
    perf_overlap = find_overlap(df_persian, df_aromo, language)
    perf_names, vec_top, vec_mid, vec_base = notes_vec_prep(perf_overlap, df_aromo, language)

perf_names.to_csv('{}cleaned_perf_names_{}.csv'.format(path_data, language))
vec_top.to_csv('{}cleaned_vec_top_{}.csv'.format(path_data, language))
vec_mid.to_csv('{}cleaned_vec_mid_{}.csv'.format(path_data, language))
vec_base.to_csv('{}cleaned_vec_base_{}.csv'.format(path_data, language))