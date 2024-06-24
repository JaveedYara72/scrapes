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
                        log.info(resp['data'][i]['id'])
                        id_list.append(resp['data'][i]['id']) # retrieving the ids of the responses
                        log.info(len(id_list))
                    url = "https://unabrands.gorgias.com/api/tickets?limit=100&order_by=updated_datetime%3Adesc&cursor={}".format(resp['meta']['next_cursor'])
                    response = requests.get(url, headers=headers)
                    resp=json.loads(response.text)
                    response_data.append(resp)
                    
                else:
                    log.info("else",len(resp['data'])) # cursor logic handled
                    for i in range(0,len(resp['data'])):
                        log.info(resp['data'][i]['id'])
                        id_list.append(resp['data'][i]['id'])
                        log.info(len(id_list))
                    break
            except Exception as e:
                log.info(e)
                id_list_fail.append(resp['data'][i]['id'])

        log.info('done fetching the ids')

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
                            log.info(f"{UpdatedDate} < {resp['data'][i]['updated_datetime']} -> {resp['data'][i]['id']}")
                            id_list.append(resp['data'][i]['id']) # retrieving the ids of the responses
                            break_flag = 0
                        else:
                            log.info("breaking the first loop")
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
                    log.info("else",len(resp['data'])) # cursor logic handled
                    for i in range(0,len(resp['data'])):
                        if(UpdatedDate<resp['data'][i]['updated_datetime']):
                            log.info(f"{UpdatedDate} < {resp['data'][i]['updated_datetime']} -> {resp['data'][i]['id']}")
                            id_list.append(resp['data'][i]['id']) # retrieving the ids of the responses
                        else:
                            log.info("breaking the second loop")
                            break
                log.info(len(id_list))
            except Exception as e:
                log.info(e)
                id_list_fail.append(resp['data'][i]['id'])
                log.info(id_list_fail)

    # Code flow starts here
    # url 
    url = "https://unabrands.gorgias.com/api/tickets?limit=100&order_by=updated_datetime%3Adesc"

    headers = {
        "accept": "application/json",
        "authorization": "Basic c2FtYmhhdi5iaGFuZGFyaUB1bmEtYnJhbmRzLmNvbTo0YTdmMDllNzQwYjM5MmRhMWI5NzRiNWM3NzFkN2MyYjE1MWZjY2E4Y2JjNDQ3YWU2ZTU5ODBlMmEwMzVkY2Yz"
    }
    response = requests.get(url, headers=headers)
    resp=json.loads(response.text)
    log.info((resp['data'][0]['updated_datetime']))

    # to get the max updated_Datetime -> data[0]['updated_datetime'] -> load this into the loadsettings file
    setter_date = resp['data'][0]['updated_datetime'] # this will give us the oldest datetime for the tickets, for incremental load
    log.info(setter_date)

    # reading the csv
    df_load=pd.read_csv(loadSettings)

    if(df_load.empty):
        log.info("Full load")

        id_generator_full(resp,response_data)
        log.info("Network Sleep")
        time.sleep(45)

    else:
        log.info("Incremental load")

        # reading the date
        UpdatedDate = df_load.iloc[-1][-1]
        log.info(f"The last load data was of {UpdatedDate}")


        id_generator_inc(resp,response_data,UpdatedDate)
        log.info("Network Sleep")
        time.sleep(45)

        log.info(f"{UpdatedDate} -> max date")

class tickets:
    async def caller_fun(session, url):
        headers = {
            "accept": "application/json",
            "authorization": "Basic c2FtYmhhdi5iaGFuZGFyaUB1bmEtYnJhbmRzLmNvbTo0YTdmMDllNzQwYjM5MmRhMWI5NzRiNWM3NzFkN2MyYjE1MWZjY2E4Y2JjNDQ3YWU2ZTU5ODBlMmEwMzVkY2Yz"
        }
        async with session.get(url, headers=headers) as r:
            try:
                if r.status == 429:
                    log.info(r.status)
                    log.info("Going into recursion, after 45 second sleep time")
                    # write logic for retry
                    time.sleep(45)
                    text = await caller_fun(session,url)
                elif(r.status == 502):
                    log.info("Bad Gateway - 502")
                    time.sleep(60)
                    text = await caller_fun(session,url) 
                elif(r.status != 200):
                    log.info(r.status)
                    log.info("Sleeping for 60 secs")
                    time.sleep(60)
                else:
                    text = await r.json()
                    log.info("Sleeping for 2 secs after every successful request")
                    time.sleep(2)
            except ValueError as exc:
                log.info(r.status)
                log.info("cannot parse JSON: %s" % exc)
        return text

    async def main_func():
        async with aiohttp.ClientSession() as session:
            tasks = []
            batch_counter = 1
            file_counter = 1
            for i in range(0,len(id_list)):
                # increment file counter by 1 everytime an id has a get request
                if(file_counter%40 == 0): # make sure to keep updating the file_counter,
                    log.info(f"{i},loop one")
                    url = f"https://unabrands.gorgias.com/api/tickets/{id_list[i]}/"
                    log.info(f"Getting the API results for {id_list[i]}")
                    task = asyncio.create_task(caller_fun(session, url))
                    tasks.append(task)

                    res = await asyncio.gather(*tasks)
                    log.info("Done awaiting the tasks") 
                    tasks.clear() # all the 40 tasks are here, waiting to be cleared

                    temp_list.extend(res) # duplicating the data into our main array
                    
                    file_counter = 1
                    time.sleep(25)
                else:
                    log.info(f"{i}, loop one else loop")
                    url = f"https://unabrands.gorgias.com/api/tickets/{id_list[i]}/"
                    log.info(f"Getting the API results for {id_list[i]}")
                    task = asyncio.create_task(caller_fun(session, url))
                    tasks.append(task)
                    # since we are sending one call here, make sure to increase the filecounter to 1
                    file_counter += 1
                if len(temp_list)==40:
                    df_batch= pd.DataFrame.from_records(temp_list)
                    df_batch.to_json(f'gorgias_list_{batch_counter}.jsonl',orient='records',lines=True)
                    log.info("Done writing it to a jsonl")
                    temp_list.clear() # clearing the main array
                    df_batch.iloc[0:0] # clearing the dataframe
                    batch_counter +=1

            # end of list logic
            log.info("Reached the end of the list")
            if(len(tasks)==0):
                log.info("No IDS left")
            else:
                res = await asyncio.gather(*tasks)
                log.info("Done awaiting the tasks")
                temp_list.extend(res)
                vLatestUpdatedDateTime = datetime.now()
                vLatestUpdatedDateTimeFile=re.sub(r' ','T',str(vLatestUpdatedDateTime))
                df_batch= pd.DataFrame.from_records(temp_list)
                df_batch.to_json(f'gorgias_messages_{batch_counter}.jsonl',orient='records',lines=True)

                # if len(df_batch)!=0:
                #     s3_resource.Object(vBucket, '{}tickets/gorgias_tickets_{}.jsonl'.format(VInputRawPrifix,vLatestUpdatedDateTimeFile)).put(Body=data_tickets.getvalue())

                log.info("Done writing it to a jsonl")
                log.info(f"Batch done->{batch_counter}")
                tasks.clear() 
                log.info(f"Done Fetching the data")

        # vLatestUpdatedDateTime = datetime.datetime.now()
        # vLatestUpdatedDateTimeFile=re.sub(r' ','T',str(vLatestUpdatedDateTime))
        # s3_resource.Object(vBucket, '{}tickets/gorgias_tickets_{}.json'.format(VInputRawPrifix,vLatestUpdatedDateTimeFile)).put(Body=bytes(json.dumps(all_data).encode('UTF-8')))

    def load_wrapper():
            # run this over the fully loaded or incrementally loaded ids
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            asyncio.run(main_func())

    # executing the function
    load_wrapper()

class ticket_messages:
    # ------------------------- messages retrieve from ticket ids .... -> now fetch the messages
    async def caller_fun(session, url):
        headers = {
            "accept": "application/json",
            "authorization": "Basic c2FtYmhhdi5iaGFuZGFyaUB1bmEtYnJhbmRzLmNvbTo0YTdmMDllNzQwYjM5MmRhMWI5NzRiNWM3NzFkN2MyYjE1MWZjY2E4Y2JjNDQ3YWU2ZTU5ODBlMmEwMzVkY2Yz"
        }
        async with session.get(url, headers=headers) as r:
            try:
                if r.status != 200:
                    log.info(r.status)
                    # write logic for retry
                    time.sleep(20)
                    text = await caller_fun(session,url)
                else: 
                    text = await r.json()
            except ValueError as exc:
                log.info(r.status)
                log.info("cannot parse JSON: %s" % exc)
        return text

    async def main_func_messages():
        async with aiohttp.ClientSession() as session:
            tasks = []
            batch_counter = 1
            file_counter = 1
            for i in range(0,len(id_list)):
                # increment file counter by 1 everytime an id has a get request
                if(file_counter%40 == 0): # make sure to keep updating the file_counter,
                    log.info(f"{i},loop one")
                    url = "https://unabrands.gorgias.com/api/messages?limit=30&order_by=created_datetime%3Adesc&ticket_id={}".format(id_list[i])
                    log.info(f"Getting the API Message results for {id_list[i]}")
                    task = asyncio.create_task(caller_fun(session, url))
                    tasks.append(task)

                    res = await asyncio.gather(*tasks)
                    log.info("Done awaiting the tasks") 
                    tasks.clear() # all the 40 tasks are here, waiting to be cleared

                    temp_list.extend(res) # duplicating the data into our main array

                    file_counter = 1
                    time.sleep(25)
                else:
                    log.info(f"{i}, loop one else loop")
                    url = "https://unabrands.gorgias.com/api/messages?limit=30&order_by=created_datetime%3Adesc&ticket_id={}".format(id_list[i])
                    log.info(f"Getting the API Message results for {id_list[i]}")
                    task = asyncio.create_task(caller_fun(session, url))
                    tasks.append(task)
                    # since we are sending one call here, make sure to increase the filecounter to 1
                    file_counter += 1
                if len(temp_list)==4000:
                    df_batch= pd.DataFrame.from_records(temp_list)
                    df_batch.to_json(f'gorgias_messages_{batch_counter}.jsonl',orient='records',lines=True)
                    log.info("Done writing it to a jsonl")
                    temp_list.clear() # clearing the main array
                    df_batch.iloc[0:0] # clearing the dataframe
                    batch_counter +=1

            # Reached the end of the list
            if(len(tasks) == 0):
                log.info("NO IDS Left")
            else:
                # end of list logic
                log.info("Reached the end of the list")
                res = await asyncio.gather(*tasks)
                log.info("Done awaiting the tasks")
                temp_list.extend(res)
                vLatestUpdatedDateTime = datetime.now()
                vLatestUpdatedDateTimeFile=re.sub(r' ','T',str(vLatestUpdatedDateTime))
                df_batch= pd.DataFrame.from_records(temp_list)
                df_batch.to_json(f'gorgias_messages_{batch_counter}.jsonl',orient='records',lines=True)

                # if len(df_batch)!=0:
                #     s3_resource.Object(vBucket, '{}tickets/gorgias_tickets_{}.jsonl'.format(VInputRawPrifix,vLatestUpdatedDateTimeFile)).put(Body=data_tickets.getvalue())

                log.info("Done writing it to a jsonl")
                log.info(f"Batch done->{batch_counter}")
                tasks.clear() 
                time.sleep(25)
                log.info(f"Done Fetching the data")

    def load_wrapper_messages():
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main_func_messages())
        
    # executing the function
    load_wrapper_messages()
