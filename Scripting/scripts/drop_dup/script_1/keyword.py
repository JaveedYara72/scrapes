import pandas as pd
import numpy as np

# 1st part - UNA ASIN
excel_file = '../PPC Management Keyword Tracking.xlsx'
una_ASINS = pd.read_excel(excel_file,'Una ASINs')
comp_ASINS = pd.read_excel(excel_file,'Competitor ASINs')
common_columns = ['UNA Brand', 'Region', 'UNA ASIN']

una_ASINS_common = una_ASINS.loc[:,common_columns]
una_ASINS_common['Region'] = una_ASINS_common['Region'].str.split(', ')
una_ASINS_common = una_ASINS_common.explode('Region')

# get the rows and remove empty rows from all of them
comp_ASINS_common = comp_ASINS.loc[:,common_columns]
comp_ASINS_common = comp_ASINS_common.dropna()

# get the unique data and drop duplicates
combined = pd.concat([una_ASINS_common,comp_ASINS_common],ignore_index=True)
combined.rename(columns={'UNA ASIN': 'ASIN'}, inplace=True)
combined_unique = combined.drop_duplicates()
combined_unique['Region'] = combined_unique['Region'].fillna('US')

# 2nd part - Competitor ASIN
common_columns = ['UNA Brand', 'Region', 'Competitor ASIN','Competitor Brand','UNA ASIN']
comp_df = comp_ASINS.loc[:,common_columns]
comp_df = comp_df.dropna()
comp_df.rename(columns={'Competitor ASIN': 'ASIN'}, inplace=True)

# Append both the dfs and check whether they have a competitive brand or not
final_df = pd.concat([combined_unique,comp_df],ignore_index=True)
final_df['has_competitor'] = np.where(final_df['Competitor Brand'].notnull(), 1, 0)
final_df.to_csv('final.csv',index=False)



