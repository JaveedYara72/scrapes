import re
import io
import os
import sys
import ssl
import boto3
import datetime
import traceback
import pandas as pd
from imbox import Imbox # pip install imbox

# ssl logic
context = ssl._create_unverified_context()

# enable less secure apps on your google account
# https://myaccount.google.com/lesssecureapps

host = "imap.gmail.com"
username = "javeed.y@una-brands.com"
password = "Javeed#Broly999!"
download_folder = "C:/Users/Y Javeed/Downloads/Una Brands/Gmail_automation/DataFiles/"


# # wrapper for amazon aws s3
# AWS_ACCESS_KEY_ID = sys.argv[1]
# AWS_SECRET_ACCESS_KEY = sys.argv[2]


# vBucket = 'una-brands-ops'
# s3_client = boto3.client('s3',
#         aws_access_key_id= AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
# s3_resource = boto3.resource('s3',
#         aws_access_key_id= AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
# VInputRawPrefix = 'data/prod/landing_raw/inventory_scrapes/Kerry_Marvable/'

# make directory
os.makedirs(download_folder, exist_ok=True)
    
mail = Imbox(host, username=username, password=password, ssl=True, ssl_context=None, starttls=False)


try:
    messages = mail.messages(date__on=datetime.date.today(),sent_from='ahmadalmas.786.aa@gmail.com') # checks both the parameters
    print(messages)
except:
    print("No Emails came in today")


for (uid, message) in messages:
    print(message.attachments)
    if "gheet" in message.subject:
        for idx, attachment in enumerate(message.attachments):
            try:
                att_fn = attachment.get('filename')
                if 'xlsx' in att_fn:
                    download_path = f"{download_folder}/{att_fn}"
                    with open(download_path, "wb") as fp:
                        fp.write(attachment.get('content').read()) # Download the file

                        # get the xslx/csv file
                        files_list=os.listdir(download_folder)
                        print(files_list)
                        # get the particular excel sheet file
                        excel_Sheet_names = pd.ExcelFile(download_folder+'/'+ files_list[-1]).sheet_names
                        print(excel_Sheet_names)

                        # read the df
                        df_data = pd.read_excel(download_folder+'/'+ files_list[-1],sheet_name=sheet_name)
                        print(df_data)

                        # # get the latest date
                        # vLatestUpdatedDateTime = datetime.datetime.now()
                        # vLatestUpdatedDateTimeFile=re.sub(r' ','T',str(vLatestUpdatedDateTime))

                        # with io.StringIO() as csv_buffer:
                        #     df_data.to_csv(csv_buffer, index=False)
                        #     print(df_data)
                        #     response = s3_client.put_object(
                        #                     Bucket=vBucket, Key='{}Marvable/Kerry_InventoryReport-{}.csv'.format(VInputRawPrefix,vLatestUpdatedDateTimeFile),Body=csv_buffer.getvalue())
                        #     status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

                        #     if status == 200:
                        #         print(f"Successful S3 put_object response. Status - {status}")
                        #     else:
                        #         print(f"Unsuccessful S3 put_object response. Status - {status}")
            except:
                print(traceback.print_exc())

mail.logout()
