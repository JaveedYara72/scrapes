import pandas as pd
import numpy as np

# 1st part - Read ASINS
excel_file = '../PPC Management Keyword Tracking.xlsx'
una_ASINS = pd.read_excel(excel_file,'Una ASINs')
comp_ASINS = pd.read_excel(excel_file,'Competitor ASINs')
common_columns = ['UNA ASIN']

common_columns_sheet2 = ['Brand','Region','UNA ASIN','Keyword','Email','Teammate Name','Date of change/request?','Team','is_active?']
starting_row = 4 # 5th row (0-based index)
keywords = pd.read_excel(excel_file,'Keywords for UNA ASINs',header=starting_row)
keywords = keywords.loc[:,common_columns_sheet2]

# drop the duplicates from the una_asins and comp_asins, only unique
una_ASINS_common = una_ASINS.loc[:,common_columns]
comp_ASINS_common = comp_ASINS.loc[:,common_columns]
comp_ASINS_common = comp_ASINS_common.dropna()

combined = pd.concat([una_ASINS_common,comp_ASINS_common],ignore_index=True)
combined_unique = combined.drop_duplicates()
combined_unique.to_csv('combined.csv',index=False)

# find common asins in both keywords df and combined_unique df
common_rows = keywords.merge(combined_unique, on='UNA ASIN',how='inner')
common_rows.to_csv('common.csv',index=False)

#find uncommon rows
uncommon_rows = keywords.merge(combined_unique, on='UNA ASIN',how='outer', indicator=True)
uncommon_rows = uncommon_rows[(uncommon_rows['_merge'] != 'both') & (uncommon_rows['_merge'] != 'right_only')]
uncommon_rows = uncommon_rows[keywords.columns]  # Select only the desired columns
uncommon_rows.to_csv('uncommon.csv',index=False)