import re
import io
import sys
import json
import boto3
import time 
import aiohttp
import asyncio
import requests
import datetime 
import pandas as pd
from csv import reader
from boto3 import client 
from datetime import datetime 

# S3 Code -> Common for all
s3_client = boto3.client('s3',
        aws_access_key_id=sys.argv[1], 
        aws_secret_access_key=sys.argv[2])
s3_resource = boto3.resource('s3',
        aws_access_key_id=sys.argv[1], 
        aws_secret_access_key=sys.argv[2])
VInputRawPrifix='data/prod/landing_raw/gorgias/'
vBucket = 'una-brands-ops'

my_bucket = s3_resource.Bucket(vBucket)


def integrations():
    print("In Integrations")
    # Load Settings
    vLoadSettings='data/prod/load_settings/gorgias/load_settings_integrations.csv'

    #--------------------------------------- List Integrations
    all_data=[]

    url = "https://unabrands.gorgias.com/api/integrations?limit=100&order_by=created_datetime%3Adesc"

    headers = {
        "accept": "application/json",
        "authorization": "Basic c2FtYmhhdi5iaGFuZGFyaUB1bmEtYnJhbmRzLmNvbTo0YTdmMDllNzQwYjM5MmRhMWI5NzRiNWM3NzFkN2MyYjE1MWZjY2E4Y2JjNDQ3YWU2ZTU5ODBlMmEwMzVkY2Yz"
    }
    try:
        response = s3_client.get_object(Bucket=vBucket, Key=vLoadSettings)
        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
    except:
        print('Load Settings file not found')
        exit()
    if status == 200:
        print(f"Successful S3 get_object response. Status - {status}")
        df_load = pd.read_csv(response.get("Body"))  
    else:
        print(f"Unsuccessful S3 get_object response. Status - {status}")

    max_resp_time_frm_api_list=[]

    response = requests.get(url, headers=headers)
    resp=json.loads(response.text)
    max_time_from_load_settings=df_load.iloc[-1][-1]
    max_time_from_load_settings_raw=max_time_from_load_settings
    
    max_time_from_load_settings = datetime.strptime(max_time_from_load_settings.split("+")[0],'%Y-%m-%dT%H:%M:%S.%f')
    print(max_time_from_load_settings)
    
    while True:
        if max_time_from_load_settings < datetime.strptime(resp['data'][0]['created_datetime'].split("+")[0],'%Y-%m-%dT%H:%M:%S.%f'):
            if resp['meta']['next_cursor']!=None:
                print("ifff",len(resp['data']))
                print(resp['meta']['next_cursor'])
                for i in range(0,len(resp['data'])):
                    all_data.append(resp['data'][i])
                    max_resp_time_frm_api_list.append(resp['data'][i]['created_datetime'])
                url = "https://unabrands.gorgias.com/api/integrations?limit=100&order_by=created_datetime%3Adesc&cursor={}".format(resp['meta']['next_cursor'])
                response = requests.get(url, headers=headers)
                resp=json.loads(response.text)
                print(resp['meta']['next_cursor'])
            else:
                print("elsee",len(resp['data']))
                for i in range(0,len(resp['data'])):
                    all_data.append(resp['data'][i])
                    max_resp_time_frm_api_list.append(resp['data'][i]['created_datetime'])
                break
        else:
            break

    print(len(all_data))
    print(df_load)
    try:
        df_load.iloc[-1][-1]=max_resp_time_frm_api_list[0]
    except:
        df_load.iloc[-1][-1]=max_time_from_load_settings_raw
    print(df_load)

    vLatestUpdatedDateTime = datetime.datetime.now()
    vLatestUpdatedDateTimeFile=re.sub(r' ','T',str(vLatestUpdatedDateTime))
    df=pd.DataFrame.from_records(all_data)
    data = io.StringIO()
    df.to_json(data,orient='records', lines=True)
    if len(df)!=0:
        s3_resource.Object(vBucket, '{}integrations/gorgias_integration_{}.jsonl'.format(VInputRawPrifix,vLatestUpdatedDateTimeFile)).put(Body=data.getvalue())
    else:
        print("No new Integrations data")
    with io.StringIO() as csv_buffer:
            df_load.to_csv(csv_buffer, index=False)

            response = s3_client.put_object(
                Bucket=vBucket, Key=vLoadSettings, Body=csv_buffer.getvalue()
            )

            status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    if status == 200:
        print(f"Updated load settings file successfully Status - {status}")
    else:
        print(f"couldnt update load settings file - {status}")

def tags():
    print("In Tags")
    # Load Settings
    vLoadSettings='data/prod/load_settings/gorgias/load_settings_tags.csv'

    #--------------------------------------- Tag Integrations
    all_data=[]

    url = "https://unabrands.gorgias.com/api/tags?order_by=created_datetime%3Adesc&limit=100"

    headers = {
        "accept": "application/json",
        "authorization": "Basic c2FtYmhhdi5iaGFuZGFyaUB1bmEtYnJhbmRzLmNvbTo0YTdmMDllNzQwYjM5MmRhMWI5NzRiNWM3NzFkN2MyYjE1MWZjY2E4Y2JjNDQ3YWU2ZTU5ODBlMmEwMzVkY2Yz"
    }

    try:
        response = s3_client.get_object(Bucket=vBucket, Key=vLoadSettings)
        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
    except:
        print('Load Settings file not found')
        exit()
    if status == 200:
        print(f"Successful S3 get_object response. Status - {status}")
        df_load = pd.read_csv(response.get("Body"))  
    else:
        print(f"Unsuccessful S3 get_object response. Status - {status}")

    max_resp_time_frm_api_list=[]
    response = requests.get(url, headers=headers)
    resp=json.loads(response.text)
    max_time_from_load_settings=df_load.iloc[-1][-1]
    max_time_from_load_settings_raw=max_time_from_load_settings

    
    max_time_from_load_settings = datetime.strptime(max_time_from_load_settings.split("+")[0],'%Y-%m-%dT%H:%M:%S.%f')
    print(max_time_from_load_settings)

    while True:
        if max_time_from_load_settings < datetime.strptime(resp['data'][0]['created_datetime'].split("+")[0],'%Y-%m-%dT%H:%M:%S.%f'):
            if resp['meta']['next_cursor']!=None:
                print("ifff",len(resp['data']))
                print(resp['meta']['next_cursor'])
                for i in range(0,len(resp['data'])):
                    all_data.append(resp['data'][i])
                    max_resp_time_frm_api_list.append(resp['data'][i]['created_datetime'])
                url = "https://unabrands.gorgias.com/api/tags?order_by=created_datetime%3Adesc&limit=100&cursor={}".format(resp['meta']['next_cursor'])
                response = requests.get(url, headers=headers)
                resp=json.loads(response.text)
                print(resp['meta']['next_cursor'])
            else:
                print("elsee",len(resp['data']))
                for i in range(0,len(resp['data'])):
                    all_data.append(resp['data'][i])
                    max_resp_time_frm_api_list.append(resp['data'][i]['created_datetime'])
                break
        else:
            break

    print(len(all_data))
    print(df_load)
    try:
        df_load.iloc[-1][-1]=max_resp_time_frm_api_list[0]
    except:
        df_load.iloc[-1][-1]=max_time_from_load_settings_raw
    print(df_load)

    vLatestUpdatedDateTime = datetime.datetime.now()
    vLatestUpdatedDateTimeFile=re.sub(r' ','T',str(vLatestUpdatedDateTime))
    df=pd.DataFrame.from_records(all_data)
    data = io.StringIO()
    df.to_json(data,orient='records', lines=True)
    if len(df)!=0:
        s3_resource.Object(vBucket, '{}tags/gorgias_tags_{}.jsonl'.format(VInputRawPrifix,vLatestUpdatedDateTimeFile)).put(Body=data.getvalue())
    else:
        print("No new TAGS data")

    with io.StringIO() as csv_buffer:
            df_load.to_csv(csv_buffer, index=False)

            response = s3_client.put_object(
                Bucket=vBucket, Key=vLoadSettings, Body=csv_buffer.getvalue()
            )

            status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    if status == 200:
        print(f"Updated load settings file successfully Status - {status}")
    else:
        print(f"couldnt update load settings file - {status}")

def users():
    print("Inside Users")
    # Load Settings
    vLoadSettings='data/prod/load_settings/gorgias/load_settings_users.csv'

    all_data=[]
    max_resp_time_frm_api_list=[]

    url="https://unabrands.gorgias.com/api/users?limit=100&order_by=created_datetime%3Adesc"

    # Read S3 Object
    try:
        response = s3_client.get_object(Bucket=vBucket, Key=vLoadSettings)
        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
    except:
        print('Load Settings file not found')
        exit()
    if status == 200:
        print(f"Successful S3 get_object response. Status - {status}")
        df_load = pd.read_csv(response.get("Body"))  
    else:
        print(f"Unsuccessful S3 get_object response. Status - {status}")


    headers = {
        "accept": "application/json",
        "authorization": "Basic c2FtYmhhdi5iaGFuZGFyaUB1bmEtYnJhbmRzLmNvbTo0YTdmMDllNzQwYjM5MmRhMWI5NzRiNWM3NzFkN2MyYjE1MWZjY2E4Y2JjNDQ3YWU2ZTU5ODBlMmEwMzVkY2Yz"
    }
    response = requests.get(url, headers=headers)
    resp=json.loads(response.text)

    max_time_from_load_settings=df_load.iloc[-1][-1]
    max_time_from_load_settings_raw=max_time_from_load_settings

    max_time_from_load_settings = datetime.strptime(max_time_from_load_settings.split("+")[0],'%Y-%m-%dT%H:%M:%S.%f')
    print(max_time_from_load_settings)

    while True:
        if max_time_from_load_settings < datetime.strptime(resp['data'][0]['created_datetime'].split("+")[0],'%Y-%m-%dT%H:%M:%S.%f'):
            if resp['meta']['next_cursor']!=None:
                print("if",len(resp['data']))
                print(resp['meta']['next_cursor'])
                for i in range(0,len(resp['data'])):
                    all_data.append(resp['data'][i])
                    max_resp_time_frm_api_list.append(resp['data'][i]['created_datetime'])

                # url = "https://unabrands.gorgias.com/api/users?limit=100&order_by=name%3Aasc&cursor={}".format(resp['meta']['next_cursor'])
                url="https://unabrands.gorgias.com/api/users?limit=100&order_by=created_datetime%3Adesc&cursor={}".format(resp['meta']['next_cursor'])
                response = requests.get(url, headers=headers)
                resp=json.loads(response.text)
                print(resp['meta']['next_cursor'])
            else:
                print("else",len(resp['data']))
                for i in range(0,len(resp['data'])):
                    all_data.append(resp['data'][i])
                    max_resp_time_frm_api_list.append(resp['data'][i]['created_datetime'])
                break
        else:
            break

    print(len(all_data))
    print(df_load)
    try:
        df_load.iloc[-1][-1]=max_resp_time_frm_api_list[0]
    except:
        df_load.iloc[-1][-1]=max_time_from_load_settings_raw
    print(df_load)

    vLatestUpdatedDateTime = datetime.datetime.now()
    vLatestUpdatedDateTimeFile=re.sub(r' ','T',str(vLatestUpdatedDateTime))
    df=pd.DataFrame.from_records(all_data)
    data = io.StringIO()
    df.to_json(data,orient='records', lines=True)
    if len(df)!=0:
        s3_resource.Object(vBucket, '{}users/gorgias_users_{}.jsonl'.format(VInputRawPrifix,vLatestUpdatedDateTimeFile)).put(Body=data.getvalue())
    else:
        print("No new Users data")
    with io.StringIO() as csv_buffer:
            df_load.to_csv(csv_buffer, index=False)

            response = s3_client.put_object(
                Bucket=vBucket, Key=vLoadSettings, Body=csv_buffer.getvalue()
            )

            status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    if status == 200:
        print(f"Updated load settings file successfully Status - {status}")
    else:
        print(f"couldn't update load settings file - {status}")

response_data = []
temp_list = []

id_list=[]
all_data=[]
id_list_fail = []

loadSettings = 'C:/Users/Y Javeed/Downloads/Una Brands/Python/Scripting/scripts/Gorgias_2/loadSettings.csv'

def id_generator(setter_date):
    def id_generator_full(resp,response_data):
        headers = {
            "accept": "application/json",
            "authorization": "Basic c2FtYmhhdi5iaGFuZGFyaUB1bmEtYnJhbmRzLmNvbTo0YTdmMDllNzQwYjM5MmRhMWI5NzRiNWM3NzFkN2MyYjE1MWZjY2E4Y2JjNDQ3YWU2ZTU5ODBlMmEwMzVkY2Yz"
        }
        while True:
            try:
                if resp['meta']['next_cursor']!=None:  
                    for i in range(0,len(resp['data'])):
                        print(resp['data'][i]['id'])
                        id_list.append(resp['data'][i]['id']) # retrieving the ids of the responses
                        print(len(id_list))
                    url = "https://unabrands.gorgias.com/api/tickets?limit=100&order_by=updated_datetime%3Adesc&cursor={}".format(resp['meta']['next_cursor'])
                    response = requests.get(url, headers=headers)
                    resp=json.loads(response.text)
                    response_data.append(resp)
                    
                else:
                    print("else",len(resp['data'])) # cursor logic handled
                    for i in range(0,len(resp['data'])):
                        print(resp['data'][i]['id'])
                        id_list.append(resp['data'][i]['id'])
                        print(len(id_list))
                    break
            except Exception as e:
                print(e)
                id_list_fail.append(resp['data'][i]['id'])

        print('done fetching the ids')

    def id_generator_inc(resp,response_data,UpdatedDate):
        headers = {
            "accept": "application/json",
            "authorization": "Basic c2FtYmhhdi5iaGFuZGFyaUB1bmEtYnJhbmRzLmNvbTo0YTdmMDllNzQwYjM5MmRhMWI5NzRiNWM3NzFkN2MyYjE1MWZjY2E4Y2JjNDQ3YWU2ZTU5ODBlMmEwMzVkY2Yz"
        }
        while True:
            try:
                if resp['meta']['next_cursor']!=None:  
                    for i in range(0,len(resp['data'])):
                        if(UpdatedDate<resp['data'][i]['updated_datetime']):
                            print(f"{UpdatedDate} < {resp['data'][i]['updated_datetime']} -> {resp['data'][i]['id']}")
                            id_list.append(resp['data'][i]['id']) # retrieving the ids of the responses
                            break_flag = 0
                        else:
                            print("breaking the first loop")
                            break_flag = 1
                            break
                    if(break_flag == 0):
                        url = "https://unabrands.gorgias.com/api/tickets?limit=100&order_by=updated_datetime%3Adesc&cursor={}".format(resp['meta']['next_cursor'])
                        response = requests.get(url, headers=headers)
                        resp=json.loads(response.text)
                        response_data.append(resp)
                    else:
                        break
                else:
                    print("else",len(resp['data'])) # cursor logic handled
                    for i in range(0,len(resp['data'])):
                        if(UpdatedDate<resp['data'][i]['updated_datetime']):
                            print(f"{UpdatedDate} < {resp['data'][i]['updated_datetime']} -> {resp['data'][i]['id']}")
                            id_list.append(resp['data'][i]['id']) # retrieving the ids of the responses
                        else:
                            print("breaking the second loop")
                            break
                print(len(id_list))
            except Exception as e:
                print(e)
                id_list_fail.append(resp['data'][i]['id'])
                print(id_list_fail)

    # Code flow starts here
    # url 
    url = "https://unabrands.gorgias.com/api/tickets?limit=100&order_by=updated_datetime%3Adesc"

    headers = {
        "accept": "application/json",
        "authorization": "Basic c2FtYmhhdi5iaGFuZGFyaUB1bmEtYnJhbmRzLmNvbTo0YTdmMDllNzQwYjM5MmRhMWI5NzRiNWM3NzFkN2MyYjE1MWZjY2E4Y2JjNDQ3YWU2ZTU5ODBlMmEwMzVkY2Yz"
    }
    response = requests.get(url, headers=headers)
    resp=json.loads(response.text)
    print((resp['data'][0]['updated_datetime']))

    # to get the max updated_Datetime -> data[0]['updated_datetime'] -> load this into the loadsettings file
    setter_date = resp['data'][0]['updated_datetime'] # this will give us the oldest datetime for the tickets, for incremental load
    print(setter_date)

    # reading the csv
    df_load=pd.read_csv(loadSettings)

    if(df_load.empty):
        print("Full load")

        id_generator_full(resp,response_data)
        print("Network Sleep")
        time.sleep(45)

    else:
        print("Incremental load")

        # reading the date
        UpdatedDate = df_load.iloc[-1][-1]
        print(f"The last load data was of {UpdatedDate}")


        id_generator_inc(resp,response_data,UpdatedDate)
        print("Network Sleep")
        time.sleep(45)

        print(f"{UpdatedDate} -> max date")

def tickets():
    async def caller_fun(session, url):
        headers = {
            "accept": "application/json",
            "authorization": "Basic c2FtYmhhdi5iaGFuZGFyaUB1bmEtYnJhbmRzLmNvbTo0YTdmMDllNzQwYjM5MmRhMWI5NzRiNWM3NzFkN2MyYjE1MWZjY2E4Y2JjNDQ3YWU2ZTU5ODBlMmEwMzVkY2Yz"
        }
        async with session.get(url, headers=headers) as r:
            try:
                if r.status == 429:
                    print(r.status)
                    print("Going into recursion, after 45 second sleep time")
                    # write logic for retry
                    time.sleep(45)
                    text = await caller_fun(session,url)
                elif(r.status == 502):
                    print("Bad Gateway - 502")
                    time.sleep(60)
                    text = await caller_fun(session,url) 
                elif(r.status != 200):
                    print(r.status)
                    print("Sleeping for 60 secs")
                    time.sleep(60)
                else:
                    text = await r.json()
                    print("Sleeping for 2 secs after every successful request")
                    time.sleep(2)
            except ValueError as exc:
                print(r.status)
                print("cannot parse JSON: %s" % exc)
        return text

    async def main_func():
        async with aiohttp.ClientSession() as session:
            tasks = []
            batch_counter = 1
            file_counter = 1
            for i in range(0,len(id_list)):
                # increment file counter by 1 everytime an id has a get request
                if(file_counter%40 == 0): # make sure to keep updating the file_counter,
                    print(f"{i},loop one")
                    url = f"https://unabrands.gorgias.com/api/tickets/{id_list[i]}/"
                    print(f"Getting the API results for {id_list[i]}")
                    task = asyncio.create_task(caller_fun(session, url))
                    tasks.append(task)

                    res = await asyncio.gather(*tasks)
                    print("Done awaiting the tasks") 
                    tasks.clear() # all the 40 tasks are here, waiting to be cleared

                    temp_list.extend(res) # duplicating the data into our main array
                    
                    file_counter = 1
                    time.sleep(25)
                else:
                    print(f"{i}, loop one else loop")
                    url = f"https://unabrands.gorgias.com/api/tickets/{id_list[i]}/"
                    print(f"Getting the API results for {id_list[i]}")
                    task = asyncio.create_task(caller_fun(session, url))
                    tasks.append(task)
                    # since we are sending one call here, make sure to increase the filecounter to 1
                    file_counter += 1
                if len(temp_list)==40:
                    df_batch= pd.DataFrame.from_records(temp_list)
                    df_batch.to_json(f'gorgias_list_{batch_counter}.jsonl',orient='records',lines=True)
                    print("Done writing it to a jsonl")
                    temp_list.clear() # clearing the main array
                    df_batch.iloc[0:0] # clearing the dataframe
                    batch_counter +=1

            # end of list logic
            print("Reached the end of the list")
            if(len(tasks)==0):
                print("No IDS left")
            else:
                res = await asyncio.gather(*tasks)
                print("Done awaiting the tasks")
                temp_list.extend(res)
                vLatestUpdatedDateTime = datetime.now()
                vLatestUpdatedDateTimeFile=re.sub(r' ','T',str(vLatestUpdatedDateTime))
                df_batch= pd.DataFrame.from_records(temp_list)
                df_batch.to_json(f'gorgias_messages_{batch_counter}.jsonl',orient='records',lines=True)

                # if len(df_batch)!=0:
                #     s3_resource.Object(vBucket, '{}tickets/gorgias_tickets_{}.jsonl'.format(VInputRawPrifix,vLatestUpdatedDateTimeFile)).put(Body=data_tickets.getvalue())

                print("Done writing it to a jsonl")
                print(f"Batch done->{batch_counter}")
                tasks.clear() 
                print(f"Done Fetching the data")

        # vLatestUpdatedDateTime = datetime.datetime.now()
        # vLatestUpdatedDateTimeFile=re.sub(r' ','T',str(vLatestUpdatedDateTime))
        # s3_resource.Object(vBucket, '{}tickets/gorgias_tickets_{}.json'.format(VInputRawPrifix,vLatestUpdatedDateTimeFile)).put(Body=bytes(json.dumps(all_data).encode('UTF-8')))

    def load_wrapper():
            # run this over the fully loaded or incrementally loaded ids
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            asyncio.run(main_func())

    # executing the function
    load_wrapper()

def ticket_messages():
    # ------------------------- messages retrieve from ticket ids .... -> now fetch the messages
    async def caller_fun(session, url):
        headers = {
            "accept": "application/json",
            "authorization": "Basic c2FtYmhhdi5iaGFuZGFyaUB1bmEtYnJhbmRzLmNvbTo0YTdmMDllNzQwYjM5MmRhMWI5NzRiNWM3NzFkN2MyYjE1MWZjY2E4Y2JjNDQ3YWU2ZTU5ODBlMmEwMzVkY2Yz"
        }
        async with session.get(url, headers=headers) as r:
            try:
                if r.status != 200:
                    print(r.status)
                    # write logic for retry
                    time.sleep(20)
                    text = await caller_fun(session,url)
                else: 
                    text = await r.json()
            except ValueError as exc:
                print(r.status)
                print("cannot parse JSON: %s" % exc)
        return text

    async def main_func_messages():
        async with aiohttp.ClientSession() as session:
            tasks = []
            batch_counter = 1
            file_counter = 1
            for i in range(0,len(id_list)):
                # increment file counter by 1 everytime an id has a get request
                if(file_counter%40 == 0): # make sure to keep updating the file_counter,
                    print(f"{i},loop one")
                    url = "https://unabrands.gorgias.com/api/messages?limit=30&order_by=created_datetime%3Adesc&ticket_id={}".format(id_list[i])
                    print(f"Getting the API Message results for {id_list[i]}")
                    task = asyncio.create_task(caller_fun(session, url))
                    tasks.append(task)

                    res = await asyncio.gather(*tasks)
                    print("Done awaiting the tasks") 
                    tasks.clear() # all the 40 tasks are here, waiting to be cleared

                    temp_list.extend(res) # duplicating the data into our main array

                    file_counter = 1
                    time.sleep(25)
                else:
                    print(f"{i}, loop one else loop")
                    url = "https://unabrands.gorgias.com/api/messages?limit=30&order_by=created_datetime%3Adesc&ticket_id={}".format(id_list[i])
                    print(f"Getting the API Message results for {id_list[i]}")
                    task = asyncio.create_task(caller_fun(session, url))
                    tasks.append(task)
                    # since we are sending one call here, make sure to increase the filecounter to 1
                    file_counter += 1
                if len(temp_list)==4000:
                    df_batch= pd.DataFrame.from_records(temp_list)
                    df_batch.to_json(f'gorgias_messages_{batch_counter}.jsonl',orient='records',lines=True)
                    print("Done writing it to a jsonl")
                    temp_list.clear() # clearing the main array
                    df_batch.iloc[0:0] # clearing the dataframe
                    batch_counter +=1

            # Reached the end of the list
            if(len(tasks) == 0):
                print("NO IDS Left")
            else:
                # end of list logic
                print("Reached the end of the list")
                res = await asyncio.gather(*tasks)
                print("Done awaiting the tasks")
                temp_list.extend(res)
                vLatestUpdatedDateTime = datetime.now()
                vLatestUpdatedDateTimeFile=re.sub(r' ','T',str(vLatestUpdatedDateTime))
                df_batch= pd.DataFrame.from_records(temp_list)
                df_batch.to_json(f'gorgias_messages_{batch_counter}.jsonl',orient='records',lines=True)

                # if len(df_batch)!=0:
                #     s3_resource.Object(vBucket, '{}tickets/gorgias_tickets_{}.jsonl'.format(VInputRawPrifix,vLatestUpdatedDateTimeFile)).put(Body=data_tickets.getvalue())

                print("Done writing it to a jsonl")
                print(f"Batch done->{batch_counter}")
                tasks.clear() 
                time.sleep(25)
                print(f"Done Fetching the data")

    def load_wrapper_messages():
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main_func_messages())

    # executing the function
    load_wrapper_messages()
    


def loadSetter(loadSettings,setter_date):
    df_load = loadSettings
    try:
        df_load.iloc[-1][-1]=setter_date
        if(setter_date == None):
            print("Something went wrong with the variable setter_date")
        else:
            print("Successfully Updated the loadSettings File")
    except:
        print("Unable to put data into loadsettings file.")
    
    

def switch(command):
    if command == "integrations":
        print("Executing the integrations function")
        integrations()
    elif command == "tags":
        print("Executing the tags function")
        tags()
    elif command == "users":
        print("Executing the users function")
        users()
    elif command == "tickets":
        setter_date = ''
        id_generator(setter_date)
        ticket_messages()
        print("Generated Messages Data")
        tickets()
        print("Generated Tickets Data")
        loadSetter(loadSettings,setter_date)
        print('Tickets and Ticket Messages data are successfully fetched')
        
        
if __name__ == "__main__":
    # write switch cases which are to be passed as arguments
    command  = sys.argv[1] # the indexing will be 3, after the amazon credentials
    command = command.lower()
    switch(command)

