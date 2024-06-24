import re
import io
import sys
import json
import time
import boto3 
import aiohttp
import asyncio
import requests
import datetime 
import pandas as pd
import logging as log
from csv import reader
from boto3 import client 
from datetime import datetime 

class users(APIcalls):
    """Access users API of Gorgias.

    Attributes:
        Nil
    """
    def __init__(self):
        super().__init__()
    
    def get_users(self):
        log.info("Getting Tags list from Tags API")
        api_path="/users?limit=100&order_by=created_datetime%3Adesc"
        self.url += api_path
        
        all_data=[]
        max_resp_time_frm_api_list=[]
        
        # Read S3 Object
        try:
            response = s3_client.get_object(Bucket=vBucket, Key=vLoadSettings)
            status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        except:
            log.info('Load Settings file not found')
            exit()
        if status == 200:
            log.info(f"Successful S3 get_object response. Status - {status}")
            df_load = pd.read_csv(response.get("Body"))  
        else:
            log.info(f"Unsuccessful S3 get_object response. Status - {status}")
            
        
        headers = {
        "accept": "application/json",
        "authorization": "Basic c2FtYmhhdi5iaGFuZGFyaUB1bmEtYnJhbmRzLmNvbTo0YTdmMDllNzQwYjM5MmRhMWI5NzRiNWM3NzFkN2MyYjE1MWZjY2E4Y2JjNDQ3YWU2ZTU5ODBlMmEwMzVkY2Yz"
        }
        
        response = requests.get(url, headers=headers)
        resp=json.loads(response.text)

        max_time_from_load_settings=df_load.iloc[-1][-1]
        max_time_from_load_settings_raw=max_time_from_load_settings

        max_time_from_load_settings = datetime.strptime(max_time_from_load_settings.split("+")[0],'%Y-%m-%dT%H:%M:%S.%f')
        log.info(max_time_from_load_settings)

        while True:
            if max_time_from_load_settings < datetime.strptime(resp['data'][0]['created_datetime'].split("+")[0],'%Y-%m-%dT%H:%M:%S.%f'):
                if resp['meta']['next_cursor']!=None:
                    log.info('if condition', len(resp['data']))
                    log.info(resp['meta']['next_cursor'])
                    for i in range(0,len(resp['data'])):
                        all_data.append(resp['data'][i])
                        max_resp_time_frm_api_list.append(resp['data'][i]['created_datetime'])

                    # url = "https://unabrands.gorgias.com/api/users?limit=100&order_by=name%3Aasc&cursor={}".format(resp['meta']['next_cursor'])
                    url="https://unabrands.gorgias.com/api/users?limit=100&order_by=created_datetime%3Adesc&cursor={}".format(resp['meta']['next_cursor'])
                    response = requests.get(url, headers=headers)
                    resp=json.loads(response.text)
                    log.info(resp['meta']['next_cursor'])
                else:
                    log.info("else condition",len(resp['data']))
                    for i in range(0,len(resp['data'])):
                        all_data.append(resp['data'][i])
                        max_resp_time_frm_api_list.append(resp['data'][i]['created_datetime'])
                    break
            else:
                break

        log.info(len(all_data))
        log.info(df_load)
        try:
            df_load.iloc[-1][-1]=max_resp_time_frm_api_list[0]
        except:
            df_load.iloc[-1][-1]=max_time_from_load_settings_raw
        log.info(df_load)

        vLatestUpdatedDateTime = datetime.datetime.now()
        vLatestUpdatedDateTimeFile=re.sub(r' ','T',str(vLatestUpdatedDateTime))
        df=pd.DataFrame.from_records(all_data)
        data = io.StringIO()
        df.to_json(data,orient='records', lines=True)
        if len(df)!=0:
            s3_resource.Object(vBucket, '{}users/gorgias_users_{}.jsonl'.format(VInputRawPrifix,vLatestUpdatedDateTimeFile)).put(Body=data.getvalue())
        else:
            log.info("No new Users data")
            
        # file uploader logic goes here