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

class tags(APICalls):
    """Access tags of Gorgias.

    Attributes:
        Nil
    """
    def __init__(self):
        super().__init__()
        
    def get_tags(self):
        all_data=[]
        
        log.info("Getting Tags list from Tags API")
        api_path="?limit=100&order_by=created_datetime%3Adesc"
        self.url += api_path
        
        # Load Settings
        vLoadSettings='data/prod/load_settings/gorgias/load_settings_tags.csv'

        headers = {
            "accept": "application/json",
            "authorization": "Basic c2FtYmhhdi5iaGFuZGFyaUB1bmEtYnJhbmRzLmNvbTo0YTdmMDllNzQwYjM5MmRhMWI5NzRiNWM3NzFkN2MyYjE1MWZjY2E4Y2JjNDQ3YWU2ZTU5ODBlMmEwMzVkY2Yz"
        }

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

        max_resp_time_frm_api_list=[]
        response = requests.get(self.url, headers=headers)
        resp=json.loads(response.text)
        max_time_from_load_settings=df_load.iloc[-1][-1]
        max_time_from_load_settings_raw=max_time_from_load_settings

        
        max_time_from_load_settings = datetime.strptime(max_time_from_load_settings.split("+")[0],'%Y-%m-%dT%H:%M:%S.%f')
        log.info(max_time_from_load_settings)

        while True:
            if max_time_from_load_settings < datetime.strptime(resp['data'][0]['created_datetime'].split("+")[0],'%Y-%m-%dT%H:%M:%S.%f'):
                if resp['meta']['next_cursor']!=None:
                    log.info("ifff",len(resp['data']))
                    log.info(resp['meta']['next_cursor'])
                    for i in range(0,len(resp['data'])):
                        all_data.append(resp['data'][i])
                        max_resp_time_frm_api_list.append(resp['data'][i]['created_datetime'])
                    self.url = "https://unabrands.gorgias.com/api/tags?order_by=created_datetime%3Adesc&limit=100&cursor={}".format(resp['meta']['next_cursor'])
                    response = requests.get(self.url, headers=headers)
                    resp=json.loads(response.text)
                    log.info(resp['meta']['next_cursor'])
                else:
                    log.info("else",len(resp['data']))
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
            s3_resource.Object(vBucket, '{}tags/gorgias_tags_{}.jsonl'.format(VInputRawPrifix,vLatestUpdatedDateTimeFile)).put(Body=data.getvalue())
        else:
            log.info("No new TAGS data")

        # file uploader logic goes here 