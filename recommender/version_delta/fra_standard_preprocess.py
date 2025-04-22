import numpy as np
import pandas as pd
home = '../../'
path_data = home + 'data/'

df_fra = pd.read_csv(path_data + 'fra_perfumes.csv')#, sep=';', encoding='latin-1')
url_ori = df_fra['url'].convert_dtypes()
name_with_brand = df_fra['Name'].convert_dtypes().str.split('for').str[0].convert_dtypes()

df_fra_cleaned = pd.read_csv(path_data + 'fra_cleaned.csv', sep=';', encoding='latin-1')
url_cleaned = df_fra_cleaned['url'].convert_dtypes()
name_from_url = df_fra_cleaned['Perfume'].convert_dtypes()
brand_from_url = df_fra_cleaned['Brand'].convert_dtypes()

url_ori = url_ori[url_ori.str.lower().isin(url_cleaned)].drop_duplicates()
name_with_brand = name_with_brand[url_ori.index]

name_wo_brand = []
brand_ori = []
for i in range(len(url_cleaned)):
    this_url_cleaned = url_cleaned.iloc[i]
    for j in range(len(url_ori)):
        this_url_ori = url_ori.iloc[j]
        if this_url_cleaned.lower() == this_url_ori.lower():
            brand_lower = brand_from_url.iloc[i]
            this_name_with_brand = name_with_brand.iloc[j]
            this_name = this_name_with_brand[:-len(brand_lower)-1]
            this_brand = this_name_with_brand[-len(brand_lower):]
            name_wo_brand.append(this_name)
            brand_ori.append(this_brand)
            break
    print(i)

name_brand_standard = pd.DataFrame((name_wo_brand, brand_ori), dtype='string').T
name_brand_standard.columns = ['Perfume', 'Brand']
df_fra_standard = pd.concat([df_fra_cleaned['url'], 
                            name_brand_standard, 
                            df_fra_cleaned['Rating Count'], 
                            df_fra_cleaned['Top'],
                            df_fra_cleaned['Middle'],
                            df_fra_cleaned['Base'],
                            df_fra_cleaned['mainaccord1'],
                            df_fra_cleaned['mainaccord2'],
                            df_fra_cleaned['mainaccord3'],
                            df_fra_cleaned['mainaccord4'],
                            df_fra_cleaned['mainaccord5']],axis=1)

df_fra_standard.to_csv('{}fra_standard.csv'.format(path_data))