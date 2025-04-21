home = '../../'
path_data = home + 'data/'

from recommender_users_func import *

df_persian = pd.read_csv(path_data + 'Persian_Data.csv')
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

persian_data_frame_clean.to_csv('{}cleaned_persian.csv'.format(path_data))

df_persian_new.value_counts('Perfume Name').head(20).to_csv('{}newbie_persian.csv'.format(path_data))