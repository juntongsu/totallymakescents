home = '../../'
path_data = home + 'data/'

from recommender_users_func import *
from recommender_notes_func import *
from recommender_lazy_func import *


language = 0

perf_names = pd.read_csv('{}cleaned_perf_names_{}.csv'.format(path_data, language))
vec_top = pd.read_csv('{}cleaned_vec_top_{}.csv'.format(path_data, language))
vec_mid = pd.read_csv('{}cleaned_vec_mid_{}.csv'.format(path_data, language))
vec_base = pd.read_csv('{}cleaned_vec_base_{}.csv'.format(path_data, language))



def input_perfume_2(frame):

    df_input = frame
    user_perfume = df_input.iloc[:, 0].to_list()
    user_sentiment = df_input.iloc[:, 1].to_numpy()
    
    return user_perfume, user_sentiment

def recommender_gamma(test_user, test_user_frame, comparison_frame, perf_names, vec_top, vec_mid, vec_base, language=0, n_recs = 20, slider = 0.5):

    user_data = test_user_frame.loc[(test_user_frame["User ID"] == test_user)]
    review_count = len(user_data.index)

    user_perfume, user_sentiment = input_perfume_2(user_data[["Perfume Name","Sentiment"]])
    user_top, user_mid, user_base = user_vec_prep(user_perfume, user_sentiment, perf_names, vec_top, vec_mid, vec_base)
    temperature = np.array((1, 2, 1, 1.5), dtype=int)
    note_recommendation_list = recommender_notes(perf_names, vec_top, vec_mid, vec_base, user_perfume, user_top, user_mid, user_base, temperature)
    if review_count>19:
        user_recommendation_list = recommender_users(test_user, test_user_frame, comparison_frame)
    else:
        user_recommendation_list = lazy_recommender(test_user, test_user_frame, comparison_frame)

    if language == 0:
        user_rec_list = user_recommendation_list['Perfume Name'].reset_index(drop=True)
        note_rec_list = note_recommendation_list['Perfume'].reset_index(drop=True)
        df_rec_list = pd.concat([user_rec_list, note_rec_list], axis=1)
    elif language == 1:
        user_rec_list = user_recommendation_list['Perfume Name'].reset_index(drop=True)
        note_rec_list = note_recommendation_list['Perfume'].reset_index(drop=True)
        df_rec_list = pd.concat([user_rec_list, note_rec_list], axis=1)

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
    
    return recommendation_list
