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

import common_functions


class APICalls:
    """Parent class to hold necessary information required for making api requests.
    
        Attributes:
        url: Api domain to which api calls will be made.
    """
    
    def __init__(self):
        """Initializes instance based on a API URL."""
        self.url = "https://unabrands.gorgias.com/api"
        self.headers = {
        "accept": "application/json",
        "authorization": "Basic c2FtYmhhdi5iaGFuZGFyaUB1bmEtYnJhbmRzLmNvbTo0YTdmMDllNzQwYjM5MmRhMWI5NzRiNWM3NzFkN2MyYjE1MWZjY2E4Y2JjNDQ3YWU2ZTU5ODBlMmEwMzVkY2Yz"
        }
        
def loadSetter(loadSettings,setter_date):
    df_load = loadSettings
    try:
        df_load.iloc[-1][-1]=setter_date
        if(setter_date == None):
            log.info("Something went wrong with the variable setter_date")
        else:
            log.info("Successfully Updated the loadSettings File")
    except:
        log.info("Unable to put data into loadsettings file.")
    

def switch(command):
    if command == "integrations":
        log.info("Executing the integrations function")
        integrations()
    elif command == "tags":
        log.info("Executing the tags function")
        tags()
    elif command == "users":
        log.info("Executing the users function")
        users()
    elif command == "tickets":
        setter_date = ''
        id_generator(setter_date)
        ticket_messages()
        log.info("Generated Messages Data")
        tickets()
        log.info("Generated Tickets Data")
        loadSetter(loadSettings,setter_date)
        log.info('Tickets and Ticket Messages data are successfully fetched')
        
if __name__ == "__main__":
    # write switch cases which are to be passed as arguments
    log = common_functions.Source.set_logger("Gorgias")
    Gorgias_obj = common_functions.Source(env = sys.argv[1], source='Gorgias', full_load= bool(sys.argv[2]))
    
    # s3_client = boto3.client('s3', aws_access_key_id=sys.argv[1], aws_secret_access_key=sys.argv[2])
    # s3_resource = boto3.resource('s3', aws_access_key_id=sys.argv[1], aws_secret_access_key=sys.argv[2])
    # my_bucket = s3_resource.Bucket(Gorgias_obj.configs['vBucket'])
    
    command  = sys.argv[3] # the indexing will be 3, after the amazon credentials
    command = command.lower()
    switch(command)

