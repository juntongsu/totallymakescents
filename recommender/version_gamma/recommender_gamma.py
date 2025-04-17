home = '../../'
path_data = home + 'data/'

from recommender_users_func import *
from recommender_notes_func import *

# df_persian = pd.read_csv(path_data + 'Persian_Data.csv')
# df_persian_new = df_persian[['User ID', 'Perfume Name','Perfume ID', 'Sentiment']]
# df_persian_new = df_persian_new.dropna()

# ##Remove perfumes with same name and different ids
# black_list = {15195,9500,15615}
# df_persian_new = df_persian_new.loc[(~df_persian_new["Perfume ID"].isin(black_list))][['User ID','Perfume Name','Sentiment']]

# user_ids = df_persian_new['User ID'].unique()
# user_frame = pd.DataFrame({'User ID':user_ids})
# user_samp = user_frame.sample(frac=0.80, random_state=13)
# selection = user_samp["User ID"]
# persian_data_frame_clean = df_persian_new.loc[(df_persian_new['User ID'].isin(selection) )]
# persian_data_frame_clean.update(persian_data_frame_clean["Sentiment"].apply(enum_ratings))

persian_data_frame_clean = pd.read_csv('{}cleaned_persian.csv'.format(path_data))

user_frame = pd.read_csv('input.csv', header=None)
user_frame.columns = ["Perfume Name","Sentiment"]

user_id = 0 
user_frame = add_user_id(user_frame)
user_recommendation_list = recommender_users(user_id, user_frame, persian_data_frame_clean)









language = 0
# if language == 0:
#     df_fra = pd.read_csv(path_data + 'fra_cleaned.csv', sep=';', encoding='latin-1')
#     perf_overlap = find_overlap(df_persian, df_fra, language)
#     perf_names, vec_top, vec_mid, vec_base = notes_vec_prep(perf_overlap, df_fra, language)
# elif language == 1:
#     df_aromo = pd.read_csv(path_data + 'aromo_ru.csv', sep=';', dtype=object)
#     perf_overlap = find_overlap(df_persian, df_aromo, language)
#     perf_names, vec_top, vec_mid, vec_base = notes_vec_prep(perf_overlap, df_aromo, language)

perf_names = pd.read_csv('{}cleaned_perf_names_{}.csv'.format(path_data, language))
vec_top = pd.read_csv('{}cleaned_vec_top_{}.csv'.format(path_data, language))
vec_mid = pd.read_csv('{}cleaned_vec_mid_{}.csv'.format(path_data, language))
vec_base = pd.read_csv('{}cleaned_vec_base_{}.csv'.format(path_data, language))

nUsers = 1
for i in range(nUsers):
    user_perfume, user_sentiment = input_perfume()
    user_top, user_mid, user_base = user_vec_prep(user_perfume, user_sentiment, perf_names, vec_top, vec_mid, vec_base)
    temperature = np.array((1, 2, 1, 1.5), dtype=int)
    note_recommendation_list = recommender_notes(perf_names, vec_top, vec_mid, vec_base, user_perfume, user_top, user_mid, user_base, temperature)












if language == 0:
    user_rec_list = user_recommendation_list['Perfume Name'].reset_index(drop=True)
    note_rec_list = note_recommendation_list['Perfume'].reset_index(drop=True)
    df_rec_list = pd.concat([user_rec_list, note_rec_list], axis=1)
elif language == 1:
    user_rec_list = user_recommendation_list['Perfume Name'].reset_index(drop=True)
    note_rec_list = note_recommendation_list['Perfume'].reset_index(drop=True)
    df_rec_list = pd.concat([user_rec_list, note_rec_list], axis=1)


#####
# n_recs: total number of recommendation expected by the client, default 20
# slider: portion of the user recommemdation list in the full list, overlap excluded, randomly selected 0.6
#####
n_recs = 20
slider = 0.6

# no overlap
if df_rec_list.value_counts().values[0] == 1:
    n_user_rec = int(n_recs * slider)
    n_note_rec = n_recs - n_user_rec
    user_rec_list = user_rec_list[user_rec_list.index <= n_user_rec]
    note_rec_list = note_rec_list[note_rec_list.index <= n_note_rec]

    if n_user_rec == n_note_rec:
        for s in range(n_user_rec):
            if s == 0:
                recommendation_list = ', '.join([user_rec_list[s], note_rec_list[s]])
            else:
                recommendation_list = ', '.join([recommendation_list, user_rec_list[s], note_rec_list[s]])
    elif n_user_rec > n_note_rec:
        for s in range(n_note_rec):
            if s == 0:
                recommendation_list = ', '.join([user_rec_list[s], note_rec_list[s]])
            else:
                recommendation_list = ', '.join([recommendation_list, user_rec_list[s], note_rec_list[s]])
        recommendation_list = ', '.join([recommendation_list, ', '.join(user_rec_list[n_note_rec+1:].values)])
    else:
        for s in range(n_user_rec):
            if s == 0:
                recommendation_list = ', '.join([user_rec_list[s], note_rec_list[s]])
            else:
                recommendation_list = ', '.join([recommendation_list, user_rec_list[s], note_rec_list[s]])
        recommendation_list = ', '.join([recommendation_list, ', '.join(user_rec_list[n_user_rec+1:].values)])
    recommendation_list = recommendation_list.split(', ')

### overlap
else:
    n_common = len(df_rec_list.value_counts().values[df_rec_list.value_counts().values > 1])
    n_common = 2
    recommendation_list = df_rec_list.value_counts().index[0:n_common].to_list()

    n_user_rec = int((n_recs - n_common) * slider)
    n_note_rec = (n_recs - n_common) - n_user_rec
    user_rec_list = user_rec_list[~user_rec_list.values.isin(recommendation_list)].reset_index(drop=True)
    user_rec_list = user_rec_list[user_rec_list.index <= n_user_rec]
    note_rec_list[~note_rec_list.values.isin(recommendation_list)].reset_index(drop=True)
    note_rec_list = note_rec_list[note_rec_list.index <= n_note_rec]

    recommendation_list = ', '.join(recommendation_list)

    if n_user_rec == n_note_rec:
        for s in range(n_user_rec):
            recommendation_list = ', '.join([recommendation_list, user_rec_list[s], note_rec_list[s]])
    elif n_user_rec > n_note_rec:
        for s in range(n_note_rec):
            recommendation_list = ', '.join([recommendation_list, user_rec_list[s], note_rec_list[s]])
        recommendation_list = ', '.join([recommendation_list, ', '.join(user_rec_list[n_note_rec+1:].values)])
    else:
        for s in range(n_user_rec):
            recommendation_list = ', '.join([recommendation_list, user_rec_list[s], note_rec_list[s]])
        recommendation_list = ', '.join([recommendation_list, ', '.join(user_rec_list[n_user_rec+1:].values)])
    recommendation_list = recommendation_list.split(', ')

print(recommendation_list)