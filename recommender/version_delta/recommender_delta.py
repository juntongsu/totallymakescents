home = '../../'
path_data = home + 'data/'

from recommender_func import *

persian_data_frame_clean = pd.read_csv('{}cleaned_persian.csv'.format(path_data))

df_input = pd.read_csv('input.csv', header=None)
client_perfume = df_input.iloc[:, 0].to_list()
client_sentiment = df_input.iloc[:, 1].to_numpy()

df_input.columns = ["Perfume Name","Sentiment"]

client_id = 0 
df_input = add_user_id(df_input)
language = 0
perf_names = pd.read_csv('{}cleaned_perf_names_{}.csv'.format(path_data, language))
vec_top = pd.read_csv('{}cleaned_vec_top_{}.csv'.format(path_data, language))
vec_mid = pd.read_csv('{}cleaned_vec_mid_{}.csv'.format(path_data, language))
vec_base = pd.read_csv('{}cleaned_vec_base_{}.csv'.format(path_data, language))  

if len(client_sentiment) == 0:
    df_rec_list = recommender_newbie(path_data)
elif len(client_sentiment) < 5:
    user_recommendation_list = lazy_recommender(client_id, df_input, persian_data_frame_clean)
    user_rec_list = user_recommendation_list['Perfume Name'].reset_index(drop=True)
    
    client_top, client_mid, client_base = user_vec_prep(client_perfume, client_sentiment, perf_names, vec_top, vec_mid, vec_base)
    temperature = np.array((1, 2, 1, 1.5), dtype=float)
    note_recommendation_list = recommender_notes(perf_names, vec_top, vec_mid, vec_base, client_perfume, client_top, client_mid, client_base, temperature)
    note_rec_list = note_recommendation_list['Perfume'].reset_index(drop=True)
    df_rec_list = pd.concat([user_rec_list, note_rec_list], axis=1)
else:
    user_recommendation_list = recommender_users(client_id, df_input, persian_data_frame_clean)
    user_rec_list = user_recommendation_list['Perfume Name'].reset_index(drop=True)
    
    client_top, client_mid, client_base = user_vec_prep(client_perfume, client_sentiment, perf_names, vec_top, vec_mid, vec_base)
    temperature = np.array((1, 2, 1, 1.5), dtype=float)
    note_recommendation_list = recommender_notes(perf_names, vec_top, vec_mid, vec_base, client_perfume, client_top, client_mid, client_base, temperature)
    note_rec_list = note_recommendation_list['Perfume'].reset_index(drop=True)
    df_rec_list = pd.concat([user_rec_list, note_rec_list], axis=1)

#####
# n_recs: total number of recommendation expected by the client, default 20
# sliders: portion of the user recommemdation list in the full list, overlap excluded, randomly selected 0.6
#####
n_recs = 20
slider = 0.6

recommendation_list = combine_rec_lists(user_rec_list, note_rec_list, n_recs, slider)
print(recommendation_list)