import io
import re
import os
import sys
import boto3
import datetime
import openpyxl
import requests
import pandas as pd
from io import BytesIO


# # wrapper for amazon aws s3
# AWS_ACCESS_KEY_ID = sys.argv[1]
# AWS_SECRET_ACCESS_KEY = sys.argv[2]

# directory = os.getcwd()


# vBucket = 'una-brands-ops'
# s3_client = boto3.client('s3',
#         aws_access_key_id= AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
# s3_resource = boto3.resource('s3',
#         aws_access_key_id= AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
# VInputRawPrefix = 'data/prod/landing_raw/inventory_scrapes/gemini/'


spreadsheetId = "10jxi5VRPGIEmLFyLmBrcyRkxd4jFHJoFCOh2rGheKr4" # Please set your Spreadsheet ID.
url = "https://docs.google.com/spreadsheets/export?exportFormat=xlsx&id=" + spreadsheetId
res = requests.get(url)
data = BytesIO(res.content)
xlsx = openpyxl.load_workbook(filename=data)
for name in xlsx.sheetnames:
    if (name == "Gemini Inventory"):

        # latest time
        vLatestUpdatedDateTime = datetime.datetime.now()
        vLatestUpdatedDateTimeFile=re.sub(r' ','T',str(vLatestUpdatedDateTime))

        # reading it into a dataframe
        values = pd.read_excel(data, sheet_name="Gemini Inventory",index_col=None)
        
        # with io.StringIO() as csv_buffer:
        #         values.to_csv(csv_buffer, index=False)
        #         response = s3_client.put_object(
        #                         Bucket=vBucket, Key='{}Gemini_Inventory-{}.csv'.format(VInputRawPrefix,vLatestUpdatedDateTimeFile),Body=csv_buffer.getvalue())
        #         status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

        #         if status == 200:
        #             print(f"Successful S3 put_object response. Status - {status}")
        #         else:
        #             print(f"Unsuccessful S3 put_object response. Status - {status}")