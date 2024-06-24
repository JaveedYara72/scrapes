from datetime import datetime, timedelta,date
from time import sleep
import time
from numpy import empty
import lazop
import os
import pandas as pd
from pandas import json_normalize
from io import StringIO
import datetime
import boto3
import json
from json import JSONEncoder
import re
import sys
import hashlib
import hmac
from csv import writer

# s3_client = boto3.client('s3',
#         aws_access_key_id=sys.argv[1], 
#         aws_secret_access_key=sys.argv[2])
# s3_resource = boto3.resource('s3',
#         aws_access_key_id=sys.argv[1], 
#         aws_secret_access_key=sys.argv[2])

# vBucket = 'una-brands-ops'
# my_bucket = s3_resource.Bucket(vBucket)
# vBrandRegionPrefix='data/prod/load_settings/lazada/brandRegionList.csv'
# VInputRawPrifix='data/prod/landing_raw/lazada_transactions_data/'

# try:
#     response = s3_client.get_object(Bucket=vBucket, Key=vBrandRegionPrefix)
#     status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
# except:
#     print('Brand Region file not found')
#     exit()
# if status == 200:
#     print(f"Successful S3 get_object response. Status - {status}")
#     df_brand_region = pd.read_csv(response.get("Body"), index_col=0)  
# else:
#     print(f"Unsuccessful S3 get_object response. Status - {status}")
# print(df_brand_region)

dt = datetime.datetime(2020,1,1)
end = datetime.datetime(2020,3,1)
step = datetime.timedelta(seconds=86400)

result = []

while dt < end:
    result.append(dt.strftime('%Y-%m-%d'))
    dt += step

# read the csv
df_brand_region = pd.read_csv("brandRegionList.csv")

# Converting dataframe to list
lBrandRegion = df_brand_region.values.tolist()



def getreverseordersforseller(url,appkey,appSecret,access_token,page_no,load_date):
    client = lazop.LazopClient(url, appkey ,appSecret)
    request = lazop.LazopRequest('/reverse/getreverseordersforseller')
    request.add_api_param('page_size', '100')
    request.add_api_param('page_no', page_no)
    request.add_api_param('ReverseOrderLineModfiedTimeRangeStart', load_date) 
    print(load_date)
    # full load -> 1577817000
    # incremental load -> custom date
    response = client.execute(request, access_token)

    while True:
        if response.body['result']['total']!=0:
            for i in range(0,len(response.body['result']['items'])):
                all_data.append(response.body['result']['items'][i])

            page_no = page_no+1
            client = lazop.LazopClient(url, appkey ,appSecret)
            request = lazop.LazopRequest('/reverse/getreverseordersforseller')
            request.add_api_param('page_size', '100')
            request.add_api_param('page_no', page_no)
            request.add_api_param('ReverseOrderLineModfiedTimeRangeStart', load_date)
            response = client.execute(request, access_token)
        else:
            break

    # dumping it into a json file
    with open('reverseorders_data', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)


def load_wrapper_reverseorders(brand,region,reverse_loadSettings):
    df_load=pd.read_csv(reverse_loadSettings)
    df_loadSetting = df_load[df_load['Brand'] == brand].sort_values(by='LastUpdatedDate')
    df_loadSetting = df_loadSetting[df_loadSetting['Region'] == region].sort_values(by='LastUpdatedDate')

    if(df_loadSetting.empty):
        print("Full load")


        for i in range(0,len(result)):
            getreverseordersforseller(vUrl,vAppKey,vAppSecret,vAccessToken,page_no,result[i])

        # appending it into a df and then writing it into the csv
        df_load.loc[len(df_load.index)] = [brand,region,result[-1]]
        df_load.to_csv('reverse_loadSettings.csv')
    else:
        print("Incremental load")
        UpdatedDate = df_loadSetting.iloc[-1][-1]
        print(UpdatedDate)
        
        for i in range(0,len(result)):
            if(UpdatedDate>result[i]):
                pass
            else:
                getreverseordersforseller(vUrl,vAppKey,vAppSecret,vAccessToken,page_no,result[i])

                # appending it into a df and then writing it into the csv
        print(result[-1])
        df_load.loc[len(df_load.index)] = [brand,region,result[-1]]
        df_load.to_csv('reverse_loadSettings.csv')
    

def get_reverse_order_id_details(url,appkey,appSecret,access_token):
    for i in range(0,len(all_data)):
        client = lazop.LazopClient(url, appkey ,appSecret)
        request = lazop.LazopRequest('/order/reverse/return/detail/list','GET')
        request.add_api_param('reverse_order_id', all_data[i]['reverse_order_id'])
        response = client.execute(request, access_token)
        reverse_order_list_data.append(response.body)

    return reverse_order_list_data    

def get_transaction_details(url,appkey,appSecret,access_token,start_time,end_time):
    client = lazop.LazopClient(url, appkey ,appSecret)
    request = lazop.LazopRequest('/finance/transaction/details/get','GET')
    request.add_api_param('start_time', start_time)
    request.add_api_param('end_time', end_time)
    response = client.execute(request, access_token)

    for i in range(0,len(response.body['data'])):
        transaction_data.append(response.body['data'][i])

    # dumping it into a json file
    with open('transactions_data', 'w', encoding='utf-8') as f:
        json.dump(transaction_data, f, ensure_ascii=False, indent=4)

def load_wrapper_transaction(brand,region,loadSettings):
    df_load=pd.read_csv(loadSettings)
    df_loadSetting = df_load[df_load['Brand'] == brand].sort_values(by='LastUpdatedDate')
    df_loadSetting = df_loadSetting[df_loadSetting['Region'] == region].sort_values(by='LastUpdatedDate')

    if(df_loadSetting.empty):
        print("Full load")


        for i in range(0,len(result)):
            get_transaction_details(vUrl,vAppKey,vAppSecret,vAccessToken,result[i],result[i])

        # appending it into a df and then writing it into the csv
        df_load.loc[len(df_load.index)] = [brand,region,result[-1]]
        df_load.to_csv('loadSettings.csv')


    else:
        UpdatedDate = df_loadSetting.iloc[-1][-1]
        print(UpdatedDate)
        
        for i in range(0,len(result)):
            if(UpdatedDate>result[i]):
                pass
            else:
                get_transaction_details(vUrl,vAppKey,vAppSecret,vAccessToken,result[i],result[i])

        
        # appending it into a df and then writing it into the csv
        print(result[-1])
        df_load.loc[len(df_load.index)] = [brand,region,result[-1]]
        df_load.to_csv('loadSettings.csv')

for i in range(0,len(lBrandRegion)):
    order_number=[]
    updated_at=[]

    # list variables to store
    all_data=[]
    reverse_order_list_data = []
    transaction_data = []
    
    page_no=1

    vBrand=lBrandRegion[i][0]
    vRegion=lBrandRegion[i][1]
    vAppKey=lBrandRegion[i][2]
    vAccessToken=lBrandRegion[i][3]
    vRefreshToken=lBrandRegion[i][4]
    vAppSecret = lBrandRegion[i][5]
    vUrl=lBrandRegion[i][6]

    vLoadStartDateTime=datetime.datetime.now()
    print(vUrl,vAppKey,vAppSecret,vAccessToken)

    # # Code logic for incremental wrapper 
    # loadSettings = 'C:/Users/Y Javeed/Downloads/Una Brands/Python/Scripting/scripts/Lazada/lazada_scripts/lazada_scripts/python/loadSettings.csv'
    # load_wrapper_transaction(vBrand,vRegion,loadSettings)

    # Code logic for incremental wrapper - reverse orders
    reverse_loadSettings = 'C:/Users/Y Javeed/Downloads/Una Brands/Python/Scripting/scripts/Lazada/lazada_scripts/lazada_scripts/python/reverse_loadSettings.csv'
    load_wrapper_reverseorders(vBrand,vRegion,reverse_loadSettings)

    # returns_data=getreverseordersforseller(vUrl,vAppKey,vAppSecret,vAccessToken,page_no)
    # reverse_order_details = get_reverse_order_id_details(vUrl,vAppKey,vAppSecret,vAccessToken)

    # # S3 Wrapper
    # vLatestUpdatedDateTime = datetime.datetime.now()
    # vLatestUpdatedDateTimeFile=re.sub(r' ','T',str(vLatestUpdatedDateTime))
    # s3_resource.Object(vBucket, '{}/reverseordersforseller/{}/{}/reverse_seller_{}.json'.format(VInputRawPrifix,vBrand,vRegion,vLatestUpdatedDateTimeFile)).put(Body=bytes(json.dumps(returns_data).encode('UTF-8')))
    # s3_resource.Object(vBucket, '{}/reverseordersdetails/{}/{}/reverse_order_details_{}.json'.format(VInputRawPrifix,vBrand,vRegion,vLatestUpdatedDateTimeFile)).put(Body=bytes(json.dumps(reverse_order_details).encode('UTF-8')))
    # s3_resource.Object(vBucket, '{}{}/{}/transaction_details{}.json'.format(VInputRawPrifix,vBrand,vRegion,vLatestUpdatedDateTimeFile)).put(Body=bytes(json.dumps(transaction_data).encode('UTF-8')))
    exit()