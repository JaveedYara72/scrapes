import pandas as pd
import numpy as np

# 1st part - Read ASINS
excel_file = 'netsuite_item_master.csv'
new_df = pd.read_csv('old.csv')
common_columns = ['sku_id','brand_name','sku_id_alias','sku_id_alias2','sku_id_alias3','sku_id_alias4']

sku_id = pd.read_csv(excel_file)
sku_id = sku_id.loc[:, common_columns]

# Create a new DataFrame to store the updated rows
updated_rows = []

# Iterate over each row in the DataFrame
for _, row in sku_id.iterrows():
    # Iterate over the last 4 columns
    for i in range(2, 6):
        value = row.iloc[i]
        if pd.notnull(value):
            # Create a new row with the non-null value
            new_row = row.copy()
            new_row['mapping'] = value
            # Append the new row to the updated_rows list
            updated_rows.append(new_row)

# Create a new DataFrame from the updated_rows list
mapped_sku_id = pd.DataFrame(updated_rows)
mapped_sku_id = mapped_sku_id.drop_duplicates(['mapping','sku_id', 'brand_name'], keep='first')
mapped_sku_id = mapped_sku_id.rename(columns={'sku_id': 'seller_sku', 'brand_name': 'brand'})
mapped_sku_id = mapped_sku_id[['mapping','seller_sku' ,'brand']]

# Save the updated DataFrame to a CSV file
mapped_sku_id[['mapping','seller_sku' ,'brand']].to_csv('new.csv', index=False)

# Concatenate the existing DataFrame with the new DataFrame
concatenated_df = pd.concat([mapped_sku_id, new_df])

# Drop duplicates based on the composite key
deduplicated_df = concatenated_df.drop_duplicates(['mapping', 'seller_sku', 'brand'],keep='first')

deduplicated_df.to_csv('final.csv',index=False)

