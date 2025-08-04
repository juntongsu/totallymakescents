### 
# merge fra_standard.csv and perfumes_table.csv (notes and reviews)
###

import pandas as pd
home = '../../'
path_data = home + 'data/'

df_fra_standard = pd.read_csv(path_data + 'fra_standard.csv')

df_fra_reviews = pd.read_csv(path_data + 'perfumes_table.csv')
df_fra_reviews = df_fra_reviews[['reviews', 'url']]
reviews = df_fra_reviews['reviews'].convert_dtypes()
reviews = reviews.str.replace('\\n', ' ').str.replace(r'[^a-zA-Z0-9\s]', '', regex=True)
reviews = reviews[reviews != '']
reviews = reviews[reviews != r'\s+']
reviews_url = df_fra_reviews['url'].convert_dtypes().str.lower()[reviews.index]
df_reviews = pd.concat([reviews, reviews_url], axis=1)

df_notes_reviews = pd.merge(df_fra_standard, df_reviews, how='inner', on='url')

# df_notes_reviews.to_csv('{}fra_reviews.csv'.format(path_data))

###
# merge gender, year, and country from the old dataset
###

# df_notes_reviews = pd.read_csv(path_data + 'fra_reviews.csv')
df_fra_cleaned = pd.read_csv(path_data + 'fra_cleaned.csv', sep=';', encoding='latin-1')

df_fra_features = df_fra_cleaned[['Gender', 'Year', 'Country', 'url']]
df_features_reviews_merge = pd.merge(df_notes_reviews, df_fra_features.convert_dtypes(convert_integer=True), how='left', on='url')
df_features_reviews_merge = df_features_reviews_merge[['url', 'Perfume', 'Brand', 
                                                       'Gender', 'Year', 'Country', 'Rating Count', 
                                                       'Top', 'Middle', 'Base', 
                                                       'mainaccord1', 'mainaccord2', 'mainaccord3', 'mainaccord4', 'mainaccord5',
                                                       'reviews'
                                                       ]]
# df_features_reviews_merge.to_csv('{}fra_reviews_merged.csv'.format(path_data))
df_features_reviews_merge.to_parquet('{}fra_reviews_merged.parquet'.format(path_data))