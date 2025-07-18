###
# vec prep for top, middle, base notes, and the accords
###
import pandas as pd
home = '../../'
path_data = home + 'data/'

def search_df_prep(df_data_notes):    
    df_accords = df_data_notes[['mainaccord1', 'mainaccord2', 'mainaccord3', 'mainaccord4', 'mainaccord5']].astype('str').agg(','.join, axis=1)
    df_accords.name = 'Accords'
    df_search = df_data_notes[['url', 'Perfume', 'Brand', 'Gender', 'Year', 'Country', 'Top', 'Middle', 'Base']]
    df_search = pd.concat([df_search, df_accords], axis=1)

    return df_search

df_features_reviews_merge = pd.read_parquet(path_data + 'fra_reviews_merged.parquet')
df_search = search_df_prep(df_features_reviews_merge)

df_search.to_parquet('{}search_filter.parquet'.format(path_data))