home = '../../'
path_data = home + 'data/'

from recommender_users_func import *
from recommender_notes_func import *

df_persian = pd.read_csv(path_data + 'Persian_Data.csv')
# old = pd.read_csv('../../data/Persian_Data.csv')
df_persian_new = df_persian[['User ID', 'Perfume Name','Perfume ID', 'Sentiment']]
df_persian_new = df_persian_new.dropna()

##Remove perfumes with same name and different ids
black_list = {15195,9500,15615}
df_persian_new = df_persian_new.loc[(~df_persian_new["Perfume ID"].isin(black_list))][['User ID','Perfume Name','Sentiment']]

user_ids = df_persian_new['User ID'].unique()
user_frame = pd.DataFrame({'User ID':user_ids})
user_samp = user_frame.sample(frac=0.80, random_state=13)
selection = user_samp["User ID"]
persian_data_frame_clean = df_persian_new.loc[(df_persian_new['User ID'].isin(selection) )]
persian_data_frame_clean.update(persian_data_frame_clean["Sentiment"].apply(enum_ratings))

user_frame = pd.read_csv('input.csv', header=None)
user_frame.columns = ["Perfume Name","Sentiment"]

user_id = 0 
user_frame = add_user_id(user_frame)
user_recommendation_list = recommender_users(user_id, user_frame, persian_data_frame_clean)

language = 0
if language == 0:
    df_fra = pd.read_csv(path_data + 'fra_cleaned.csv', sep=';', encoding='latin-1')
    perf_overlap = find_overlap(df_persian, df_fra, language)
    perf_names, vec_top, vec_mid, vec_base = notes_vec_prep(perf_overlap, df_fra, language)
elif language == 1:
    df_aromo = pd.read_csv(path_data + 'aromo_ru.csv', sep=';', dtype=object)
    perf_overlap = find_overlap(df_persian, df_aromo, language)
    perf_names, vec_top, vec_mid, vec_base = notes_vec_prep(perf_overlap, df_aromo, language)

nUsers = 1
for i in range(nUsers):
    user_perfume, user_sentiment = input_perfume()
    user_top, user_mid, user_base = user_vec_prep(user_perfume, user_sentiment, perf_names, vec_top, vec_mid, vec_base)
    temperature = np.array((1, 2, 1, 1.5), dtype=int)
    note_recommendation_list_a = recommender_notes(perf_names, vec_top, vec_mid, vec_base, user_perfume, user_top, user_mid, user_base, temperature)

if language == 0:
    user_rec_list = user_recommendation_list['Perfume Name'].reset_index(drop=True)
    note_rec_list = note_recommendation_list_f['Perfume'].reset_index(drop=True)
    df_rec_list = pd.concat([user_rec_list, note_rec_list], axis=1)
elif language == 1:
    user_rec_list = user_recommendation_list['Perfume Name'].reset_index(drop=True)
    note_rec_list = note_recommendation_list_a['Perfume'].reset_index(drop=True)
    df_rec_list = pd.concat([user_rec_list, note_rec_list], axis=1)



n_recs = 20
slider = 0.6

