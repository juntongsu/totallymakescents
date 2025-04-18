import pandas as pd 
def combine_rec_lists(user_rec_list, note_rec_list, n_recs, slider):
    df_rec_list = pd.concat([user_rec_list, note_rec_list], axis=1)
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