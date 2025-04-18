import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

###Cleaning up Persian Data Frame

old = pd.read_csv('../data/Persian_Data.csv')
df = old[['User ID', 'Perfume ID','Perfume Name','Sentiment']]
df = df.dropna()

##Remove perfumes with same name and different ids
black_list = {15195,9500,15615}
df = df.loc[(~df["Perfume ID"].isin(black_list))][['User ID','Perfume Name','Sentiment']]

user_ids = df['User ID'].unique()
user_frame = pd.DataFrame({'User ID':user_ids})
user_samp = user_frame.sample(frac=0.80, random_state=13)
selection = user_samp["User ID"]
persian_data_frame_clean = df.loc[(df['User ID'].isin(selection) )]

def enum_ratings(sentiment):
    if sentiment == "Positive":
        return 1.0
    if sentiment == "Negative":
        return -1.0
    else: 
        return 0.0

persian_data_frame_clean.update(persian_data_frame_clean["Sentiment"].apply(enum_ratings))
persian_data_frame_clean = persian_data_frame_clean.loc[(persian_data_frame_clean['Sentiment'] != 0)]


###Final Test 

final_test_frame = df.loc[(~df['User ID'].isin(selection) )]
final_test_frame.update(final_test_frame["Sentiment"].apply(enum_ratings))
final_test_frame = final_test_frame.loc[(final_test_frame['Sentiment'] != 0)]

user_counts = final_test_frame["User ID"].value_counts()
user_counts = pd.DataFrame({'User ID':user_counts.index, 'Count':user_counts.values})

final_testers = user_counts.loc[(user_counts['Count']>7 )]["User ID"]
final_test_frame = final_test_frame.loc[(final_test_frame["User ID"].isin(final_testers))]



####Selecting Initial Test 

#user_counts = persian_data_frame_clean["User ID"].value_counts()
#user_counts = pd.DataFrame({'User ID':user_counts.index, 'Count':user_counts.values})

#potential_testers = user_counts.loc[(user_counts['Count']>9 )]["User ID"]
#testers = potential_testers.sample(frac=0.30, random_state=13)

#remaining_testers = user_counts.loc[((~user_counts["User ID"].isin(testers))&(user_counts['Count']>9 ))]["User ID"]
#testers_2 = remaining_testers.sample(frac=0.43, random_state=13)


#test_user_frame = persian_data_frame_clean.loc[(persian_data_frame_clean["User ID"].isin(testers))]
#comparison_frame = persian_data_frame_clean.loc[(~persian_data_frame_clean["User ID"].isin(testers))]

#test_user_frame_2 = persian_data_frame_clean.loc[(persian_data_frame_clean["User ID"].isin(testers_2))]
#comparison_frame_2 = persian_data_frame_clean.loc[(~persian_data_frame_clean["User ID"].isin(testers_2))]

####Create RNG Recs 

sentiment_count = persian_data_frame_clean["Sentiment"].value_counts()

positive_count = sentiment_count.iloc[0]
negative_count = sentiment_count.iloc[1]
total_count = positive_count+negative_count

perfumes =  persian_data_frame_clean["Perfume Name"].drop_duplicates()

random_vector_length = len(perfumes)
postive_vector_length = round(random_vector_length*positive_count/total_count)
negative_vector_length = random_vector_length-postive_vector_length

positive_vector = np.repeat(1.0, postive_vector_length)
negative_vector = np.repeat(-1.0, negative_vector_length)

random_vector = np.concatenate((positive_vector,negative_vector))
np.random.seed(13) 
np.random.shuffle(random_vector) 

random_frame = pd.DataFrame({'Perfume Name':perfumes, 'Sentiment':random_vector})

#####User Based Model

def has_opinions(user, frame):
    return set(frame.loc[(frame['User ID'] == user)]["Perfume Name"])

def share_opinions(user_1, user_2, frame_1,frame_2):
    return has_opinions(user_1,frame_1).intersection(has_opinions(user_2,frame_2))

def reference_users(user_1, frame_1,frame_2, commonality=1):
    users= set(frame_2['User ID'])
    relevant_users=set()
    for user_2 in users:
        if len(share_opinions(user_1,user_2,frame_1,frame_2))>= commonality:
            relevant_users.add(user_2)
    return relevant_users

def accuracy_index(user_1, user_2, frame_1,frame_2, weight = 1.0):
    ind = len(share_opinions(user_1, user_2, frame_1,frame_2))/len(has_opinions(user_1, frame_1))
    return ind**weight

def sentiment_vector(user, frame, perfumes = "ALL"):
    if perfumes == "ALL":
        sentiment = frame.loc[(frame["User ID"] == user)][["Perfume Name","Sentiment"]]
    else:
        sentiment = frame.loc[((frame["User ID"] == user) & (frame["Perfume Name"].isin(perfumes)))][["Perfume Name","Sentiment"]]
    
    sentiment = sentiment.sort_values(by="Perfume Name")

    return sentiment["Sentiment"].to_numpy()

def cos_index_1(user_1,user_2,frame_1,frame_2):
    shared = share_opinions(user_1, user_2, frame_1,frame_2)
    vector_1 = sentiment_vector(user_1, frame_1, shared)
    vector_2 = sentiment_vector(user_2, frame_2, shared)
    return cosine_similarity([vector_1],[vector_2])[0][0]

def multiplier(user_1,user_2,frame_1,frame_2,weight=1.0):
    return cos_index_1(user_1,user_2,frame_1,frame_2)*accuracy_index(user_1, user_2, frame_1,frame_2,weight)

def adjust_rating_1(rating, multi):
    return rating*multi

def adjusted_frame_1(user_1,frame_1,frame_2, commonality=1,weight = 1.0):
    relevant_users = reference_users(user_1, frame_1,frame_2, commonality)
    new_frame = frame_2.loc[(frame_2['User ID'].isin(relevant_users))]
    for user_2 in relevant_users:
        m = multiplier(user_1,user_2,frame_1,frame_2,weight)
        adjust = new_frame.loc[(new_frame['User ID']==user_2), "Sentiment"].apply(adjust_rating_1,args=([m]))
        new_frame.update(adjust)
    return new_frame

def ratings(user_1,frame_1,frame_2, commonality=1,weight=1.0, type = "sum"):
    known_perfumes = has_opinions(user_1, frame_1)

    adjusted_ratings = adjusted_frame_1(user_1,frame_1,frame_2,commonality,weight)
    adjusted_ratings = adjusted_ratings.loc[(~adjusted_ratings["Perfume Name"].isin(known_perfumes))]

    adjusted_ratings["Similarity"] = adjusted_ratings.groupby('Perfume Name')['Sentiment'].transform(type)
    adjusted_ratings = adjusted_ratings[["Perfume Name", "Similarity"]].drop_duplicates()

    return adjusted_ratings


###Lazy model

def has_positive_opinions(user, frame):
    return set(frame.loc[((frame['User ID'] == user)&(frame["Sentiment"]==1.0))]["Perfume Name"])

def share_positive_opinions(user_1, user_2, frame_1,frame_2):
    return has_positive_opinions(user_1,frame_1).intersection(has_positive_opinions(user_2,frame_2))

def positive_reference_users(user_1, frame_1,frame_2, commonality=1):
    users= set(frame_2['User ID'])
    relevant_users=set()
    for user_2 in users:
        if len(share_positive_opinions(user_1,user_2,frame_1,frame_2))>= commonality:
            relevant_users.add(user_2)
    return relevant_users 
 
def lazy_frame(user_1,frame_1,frame_2, commonality=1):
    relevant_users = positive_reference_users(user_1, frame_1,frame_2, commonality)
    new_frame = frame_2.loc[(frame_2['User ID'].isin(relevant_users))]
    return new_frame

def lazy_ratings(user_1,frame_1,frame_2, commonality=1, type = "sum"):
    known_perfumes = has_opinions(user_1, frame_1)

    adjusted_ratings = lazy_frame(user_1,frame_1,frame_2,commonality)
    adjusted_ratings = adjusted_ratings.loc[(~adjusted_ratings["Perfume Name"].isin(known_perfumes))]

    adjusted_ratings["Similarity"] = adjusted_ratings.groupby('Perfume Name')['Sentiment'].transform(type)
    adjusted_ratings = adjusted_ratings[["Perfume Name", "Similarity"]].drop_duplicates()

    return adjusted_ratings




###Notes Recommender


def find_overlap(df_persian, df_data_notes, language):
    perf_name_overlap = []
    perf_url_overlap = []
    if language == 0:
        perf_name_unique = df_persian['Perfume Name'].drop_duplicates().str.lower().str.replace(' ', '-').convert_dtypes().to_list()
        perf_name_original = df_persian['Perfume Name'].drop_duplicates().convert_dtypes().to_list()
        perf_name_data_notes = df_data_notes['Perfume'].convert_dtypes()
        perf_url_data_notes = df_data_notes['url'].convert_dtypes()
        perf_rate_data_notes = df_data_notes['Rating Count'].convert_dtypes()
        
    elif language == 1:
        perf_name_unique = df_persian['Perfume Name'].drop_duplicates().convert_dtypes().to_list()
        perf_name_original = perf_name_unique
        perf_name_data_notes = df_data_notes['name'].convert_dtypes()
        perf_url_data_notes = df_data_notes['url'].convert_dtypes()
        perf_rate_data_notes = df_data_notes['rating_count'].fillna('0 c').str.split(' ').str[0].astype('int')
    
    for i in range(len(perf_name_original)):
        perf_name_multi = perf_name_data_notes[perf_name_data_notes == perf_name_unique[i]]
        if len(perf_name_multi) == 1:
            perf_name_overlap += [perf_name_original[i]]
            perf_url_overlap += perf_url_data_notes[perf_name_data_notes == perf_name_unique[i]].to_list()
        elif len(perf_name_multi) > 1:
            perf_rate_multi = perf_rate_data_notes[perf_name_data_notes == perf_name_unique[i]]
            if perf_rate_multi.sort_values(ascending=False).values[0] > 3*perf_rate_multi.sort_values(ascending=False).values[1]:
                perf_name_overlap += [perf_name_original[i]]
                perf_url_multi = perf_url_data_notes[perf_name_data_notes == perf_name_unique[i]]
                perf_url_overlap += [perf_url_multi[perf_rate_multi.idxmax()]]
    
    perf_name_overlap = pd.Series(perf_name_overlap, dtype='string').rename('Perfume')
    perf_url_overlap = pd.Series(perf_url_overlap, dtype='string').rename('url')
    # print('Found {} overlap perfumes between datasets'.format(len(perf_name_overlap)))
    perf_overlap = pd.concat([perf_name_overlap, perf_url_overlap], axis=1)
    return perf_overlap

def notes_vec_prep(perf_overlap, df_data_notes, language):
    if language == 0:
        df_perf_notes = df_data_notes[(df_data_notes['url'].isin(perf_overlap['url']))][['Perfume', 'Top', 'Middle', 'Base']]
        
        perf_name_lower = pd.Series(perf_overlap['Perfume'].str.lower().str.replace(' ', '-').convert_dtypes(), name='Lower')
        perf_name_dict = pd.concat([perf_overlap['Perfume'], perf_name_lower], axis=1)
        perf_names = df_perf_notes['Perfume'].convert_dtypes()
        perf_index = perf_names.reset_index().set_index('Perfume').loc[perf_name_dict.Lower].reset_index().set_index('index').index
        perf_names = perf_name_dict.set_index(perf_index)['Perfume'].sort_index()

        vec_top = df_perf_notes['Top'].str.get_dummies(sep=', ').astype('float')
        vec_mid = df_perf_notes['Middle'].str.get_dummies(sep=', ').astype('float')
        vec_base = df_perf_notes['Base'].str.get_dummies(sep=', ').astype('float')
    elif language == 1:
        df_perf_notes = df_data_notes[df_data_notes['url'].isin(perf_overlap['url'])][['name', 'top_notes', 'middle_notes', 'bottom_notes']]
        perf_names = pd.Series(df_perf_notes['name'].convert_dtypes(), name='Perfume')
        
        vec_top = df_perf_notes['top_notes'].str.replace(r".\]", "", regex=True).str.replace(r"\[.", "", regex=True).str.replace("', '", ", ", regex=False).str.get_dummies(sep=', ').astype('float')
        vec_mid = df_perf_notes['middle_notes'].str.replace(r".\]", "", regex=True).str.replace(r"\[.", "", regex=True).str.replace("', '", ", ", regex=False).str.get_dummies(sep=', ').astype('float')
        vec_base = df_perf_notes['bottom_notes'].str.replace(r".\]", "", regex=True).str.replace(r"\[.", "", regex=True).str.replace("', '", ", ", regex=False).str.get_dummies(sep=', ').astype('float')

    #print('Top notes: {}, middle notes: {}, base notes: {}'.format(vec_top.shape[1], vec_mid.shape[1], vec_base.shape[1]))
    return perf_names, vec_top, vec_mid, vec_base



def input_perfume_2(frame):

    df_input = frame
    user_perfume = df_input.iloc[:, 0].to_list()
    user_sentiment = df_input.iloc[:, 1].to_numpy()
    
    return user_perfume, user_sentiment



def user_vec_prep(user_perfume, user_sentiment, perf_names, vec_top, vec_mid, vec_base):
    for i in range(len(user_sentiment)):
        if i == 0:
            user_top = vec_top.loc[perf_names[perf_names == user_perfume[i]].index] * user_sentiment[i]
            user_mid = vec_mid.loc[perf_names[perf_names == user_perfume[i]].index] * user_sentiment[i]
            user_base = vec_base.loc[perf_names[perf_names == user_perfume[i]].index] * user_sentiment[i]
        else:
            user_top = user_top.add(vec_top.loc[perf_names[perf_names == user_perfume[i]].index] * user_sentiment[i], fill_value=0.)
            user_mid = user_mid.add(vec_mid.loc[perf_names[perf_names == user_perfume[i]].index] * user_sentiment[i], fill_value=0.)
            user_base = user_base.add(vec_base.loc[perf_names[perf_names == user_perfume[i]].index] * user_sentiment[i], fill_value=0.)

    return user_top, user_mid, user_base

def recommender_notes(perf_names, vec_top, vec_mid, vec_base, user_perfume, user_top, user_mid, user_base, temperature):
    vec_allnotes = vec_top.add(vec_mid.add(vec_base, fill_value=0), fill_value=0)
    user_allnotes = user_top.add(user_mid.add(user_base, fill_value=0), fill_value=0)
    
    user_top = user_top.apply(np.sum, axis=0)
    user_mid = user_mid.apply(np.sum, axis=0)
    user_base = user_base.apply(np.sum, axis=0)
    user_allnotes = user_allnotes.apply(np.sum, axis=0)

    user_top = np.reshape(user_top, (1, -1))
    user_mid = np.reshape(user_mid, (1, -1))
    user_base = np.reshape(user_base, (1, -1))
    user_allnotes = np.reshape(user_allnotes, (1, -1))

    sim_top = cosine_similarity(user_top, vec_top)[0]
    sim_mid = cosine_similarity(user_mid, vec_mid)[0]
    sim_base = cosine_similarity(user_base, vec_base)[0]
    sim_allnotes = cosine_similarity(user_allnotes, vec_allnotes)[0]

    sim_total = sim_top * temperature[0] + sim_mid * temperature[1] + sim_base * temperature[2] + sim_allnotes * temperature[-1] 
        
    sim_total = pd.Series(sim_total, index=perf_names.index, name='Score')
    df_sim_total = pd.concat([perf_names, sim_total], axis=1)

    rec_list = df_sim_total
    rec_list = rec_list.drop(rec_list[rec_list['Perfume'].isin(user_perfume)].index)#.reset_index(drop=True)

    # print(rec_list)
    
    return rec_list



###Comparison Test For Single User

def similarity_test_2(test_user, test_user_frame, perf_names, vec_top, vec_mid, vec_base, state=1, i=0):
    user_data_all = test_user_frame.loc[(test_user_frame["User ID"] == test_user)]
    truncated_user_data = user_data_all.sample(frac=0.5, random_state=state)

    count =  truncated_user_data.loc[(truncated_user_data["User ID"]==test_user)]["User ID"].value_counts()
    count = count.iloc[0]

    user_perfume, user_sentiment = input_perfume_2(truncated_user_data[["Perfume Name","Sentiment"]])
    user_top, user_mid, user_base = user_vec_prep(user_perfume, user_sentiment, perf_names, vec_top, vec_mid, vec_base)
    temperature = np.array((1, 2, 1, 1.5), dtype=int)
    generated_notes_ratings = recommender_notes(perf_names, vec_top, vec_mid, vec_base, user_perfume, user_top, user_mid, user_base, temperature)

    known_perfumes = has_opinions(test_user, truncated_user_data)
    unknown_perfumes = set(user_data_all.loc[(~user_data_all["Perfume Name"].isin(known_perfumes))]["Perfume Name"])
    overlap = set(generated_notes_ratings.loc[(generated_notes_ratings["Perfume"].isin(unknown_perfumes))]["Perfume"])

    true_vector = user_data_all.loc[(user_data_all["Perfume Name"].isin(overlap))][["Perfume Name","Sentiment"]].sort_values(by="Perfume Name")
    test_notes_vector = generated_notes_ratings.loc[(generated_notes_ratings["Perfume"].isin(overlap))][["Perfume","Score"]].sort_values(by="Perfume")

    comparison_length = true_vector.shape[0]

    print(test_user)
 
    if (len(true_vector.index)==len(test_notes_vector.index)) and (comparison_length>0):
        test_notes_similarity = cosine_similarity([true_vector["Sentiment"]],[test_notes_vector["Score"]])[0][0]
        
    else:
        test_notes_similarity = np.NaN
        
    results_frame = pd.DataFrame({'User':[test_user],'Known Perfumes':[count], "Notes Similarity":[test_notes_similarity]}, index=[i])

    return results_frame


def similarity_test(test_user,test_user_frame, comparison_frame,commonality=2, weight=1, comparison_vector = random_frame, state=1, i=0, type="sum"):
    user_data_all = test_user_frame.loc[(test_user_frame["User ID"] == test_user)]
    truncated_user_data = user_data_all.sample(frac=0.5, random_state=state)

    count =  truncated_user_data.loc[(truncated_user_data["User ID"]==test_user)]["User ID"].value_counts()
    count = count.iloc[0]

    generated_ratings = ratings(test_user,truncated_user_data,comparison_frame, commonality, weight, type)
    lazy_model = lazy_ratings(test_user,truncated_user_data,comparison_frame, commonality=1)

    known_perfumes = has_opinions(test_user, truncated_user_data)
    unknown_perfumes = set(user_data_all.loc[(~user_data_all["Perfume Name"].isin(known_perfumes))]["Perfume Name"])
    overlap = set(generated_ratings.loc[(generated_ratings["Perfume Name"].isin(unknown_perfumes))]["Perfume Name"])

    true_vector = user_data_all.loc[(user_data_all["Perfume Name"].isin(overlap))][["Perfume Name","Sentiment"]].sort_values(by="Perfume Name")
    test_vector = generated_ratings.loc[(generated_ratings["Perfume Name"].isin(overlap))][["Perfume Name","Similarity"]].sort_values(by="Perfume Name")
    random_vector = comparison_vector.loc[(comparison_vector["Perfume Name"].isin(overlap))][["Perfume Name","Sentiment"]].sort_values(by="Perfume Name")
    lazy_vector = lazy_model.loc[(lazy_model["Perfume Name"].isin(overlap))][["Perfume Name","Similarity"]].sort_values(by="Perfume Name")


    print(test_user)

    if (len(true_vector.index)==len(test_vector.index)) and (len(true_vector.index)>0):
        test_similarity = cosine_similarity([true_vector["Sentiment"]],[test_vector["Similarity"]])[0][0]
        
    else:
        test_similarity = np.NaN
        

    if (len(true_vector.index) == len(random_vector.index)) and (len(true_vector.index)>0):
        random_similarity = cosine_similarity([true_vector["Sentiment"]],[random_vector["Sentiment"]])[0][0]
    else:
        random_similarity = np.NaN

    if (len(true_vector.index) == len(lazy_vector.index)) and (len(true_vector.index)>0):
        lazy_similarity = cosine_similarity([true_vector["Sentiment"]],[lazy_vector["Similarity"]])[0][0]
    else:
        lazy_similarity = np.NaN

    results_frame = pd.DataFrame({'User':[test_user], 'Known Perfumes':[count], 'User Similarity':[test_similarity],'Random Similarity':[random_similarity],'Popular Similarity':[lazy_similarity]}, index=[i])

    return results_frame


### Comparison Test for all Testers

def similarity_test_2_all(test_users,test_user_frame,perf_names, vec_top, vec_mid, vec_base, state=1):
    user_list = test_users.to_list()
    n = len(user_list)
    frames = [similarity_test_2(user_list[ind], test_user_frame, perf_names, vec_top, vec_mid, vec_base, state, ind) for ind in range(n)]
     
    results_frame = pd.concat(frames)

    return results_frame

def similarity_test_all(test_users,test_user_frame, comparison_frame,commonality=2, weight=1, comparison_vector = random_frame, state=1, type="sum"):
    user_list = test_users.to_list()
    n = len(user_list)
    frames = [similarity_test(user_list[ind],test_user_frame,comparison_frame,commonality,weight,comparison_vector,state,ind, type) for ind in range(n)]
    
    results_frame = pd.concat(frames)

    return results_frame


###Test Running

df_persian = persian_data_frame_clean

results_1 = similarity_test_all(final_testers, final_test_frame, persian_data_frame_clean, weight=1, type="sum")

language = 0

df_fra = pd.read_csv('data/fra_cleaned.csv', sep=';', encoding='latin-1')
perf_overlap = find_overlap(df_persian, df_fra, language)
perf_names, vec_top, vec_mid, vec_base = notes_vec_prep(perf_overlap, df_fra, language)

results_2 = similarity_test_2_all(final_testers,final_test_frame,perf_names, vec_top, vec_mid, vec_base)


results = pd.merge(left=results_1,right = results_2, on=["User","Known Perfumes"])
results.to_csv('final_sentiment_results.csv') 








