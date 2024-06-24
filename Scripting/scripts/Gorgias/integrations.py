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

class integrations(APICalls):
    """Access integrations API of Gorgias.

    Attributes:
        Nil
    """
    def __init__(self):
        super().__init__()
    
    def get_integrations(self):
        log.info("In Integrations")
        exit()
        
        log.info("Getting Tags list from Tags API")
        api_path="/integrations?limit=100&order_by=created_datetime%3Adesc"
        self.url += api_path
        
        # Load Settings
        vLoadSettings='data/prod/load_settings/gorgias/load_settings_integrations.csv'
        
        # S3 Logic
        try:
            response = s3_client.get_object(Bucket=Gorgias_obj.configs['vBucket'], Key=vLoadSettings)
            status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        except:
            log.info('Load Settings file not found')
            exit()
        if status == 200:
            log.info(f"Successful S3 get_object response. Status - {status}")
            df_load = pd.read_csv(response.get("Body"))  
        else:
            log.info(f"Unsuccessful S3 get_object response. Status - {status}")

        # local var for storing the data
        all_data=[]

        max_resp_time_frm_api_list=[]
        response = requests.get(self.url, headers=self.headers)
        resp=json.loads(response.text)
        
        max_time_from_load_settings=df_load.iloc[-1][-1]
        max_time_from_load_settings_raw=max_time_from_load_settings
        
        max_time_from_load_settings = datetime.strptime(max_time_from_load_settings.split("+")[0],'%Y-%m-%dT%H:%M:%S.%f')
        log.info(max_time_from_load_settings)
        
        while True:
            if max_time_from_load_settings < datetime.strptime(resp['data'][0]['created_datetime'].split("+")[0],'%Y-%m-%dT%H:%M:%S.%f'):
                if resp['meta']['next_cursor']!=None:
                    log.info("if",len(resp['data']))
                    for i in range(0,len(resp['data'])):
                        all_data.append(resp['data'][i])
                        max_resp_time_frm_api_list.append(resp['data'][i]['created_datetime'])
                    self.url = "https://unabrands.gorgias.com/api/integrations?limit=100&order_by=created_datetime%3Adesc&cursor={}".format(resp['meta']['next_cursor'])
                    response = requests.get(self.url, headers=self.headers)
                    resp=json.loads(response.text)
                else:
                    log.info("else",len(resp['data']))
                    for i in range(0,len(resp['data'])):
                        all_data.append(resp['data'][i])
                        max_resp_time_frm_api_list.append(resp['data'][i]['created_datetime'])
                    break
            else:
                break
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
            s3_resource.Object(Gorgias_obj.configs['vBucket'], '{}integrations/gorgias_integration_{}.jsonl'.format(Gorgias_obj.configs['VInputRawPrifix'],vLatestUpdatedDateTimeFile)).put(Body=data.getvalue())
        else:
            log.info("No new Integrations data")
            
        # file uploader logic here
        with io.StringIO() as csv_buffer:
                df_load.to_csv(csv_buffer, index=False)

                response = s3_client.put_object(
                    Bucket=Gorgias_obj.configs['vBucket'], Key=vLoadSettings, Body=csv_buffer.getvalue()
                )

                status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

        if status == 200:
            log.info(f"Updated load settings file successfully Status - {status}")
        else:
            log.info(f"couldn't update load settings file - {status}")
        