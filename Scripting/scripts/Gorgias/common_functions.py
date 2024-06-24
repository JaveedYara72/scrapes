import configparser
import boto3
from datetime import datetime
from collections import namedtuple
import logging as log
import pandas as pd
import io

BATCH_SIZE = 10000 # no of jsonl lines transferred at a time to S3 bucket

class Source():
    """
    Contains information about all the sources.

    Attributes:
        env: type of environment at which script runs
        source: name of marketplace
        full_load: a boolean indicating if this run will be a full load or not
        client: a S3 client
        configs: a dict like object storing key value pairs in config files
        connections: a named tuple storing info about different brands and regions
        load_settings: a dict storing last updated time of each connections
    """
    def __init__(self, env: str, source: str, full_load : bool):
        """Initialises instance based on env name, source name and whether to run full load."""
        self.env = env
        self.source = source
        self.configs = self.get_configs()
        self.client = self.create_s3_client()
        if full_load:
            self.cleanup_s3()
        self.connections = self.get_connections()
        # self.load_settings = self.get_load_settings()


    @staticmethod
    def set_logger(logger_name: str):
        """Creates logger based on a given format

        Args:
            logger_name: Name of logger printed in the format.

        Returns:
            Logger for a particular script.
        """
        log.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=log.INFO)
        logger = log.getLogger(logger_name)
        return logger

    def get_configs(self):
        """
        Read configuration files.

        Returns:
            A dict like object containing all key-value pairs in config files
        """
        log.info('Parsing the common, env and source level config files')
        configs = configparser.ConfigParser()
        configs.optionxform = str

        with open('config/commonEnv.properties', 'r') as file, \
            open('config/'+ self.env +'/env.properties', 'r') as file_env, \
            open('config/'+ self.env +'/pipelines/' + self.source + '.properties', 'r') as file_source:
            configs.read_string("[DEFAULT]\n" + file.read().replace('"',"") + "\n" + file_env.read().replace('"',"") + "\n" + file_source.read().replace('"',""))

        return configs['DEFAULT']

    def create_s3_client(self):
        """
        Create a client for S3 service of an account.

        Returns:
            S3Client
        """
        log.info('Creating S3 Client')
        client = boto3.client('s3',
            aws_access_key_id='AKIA5IDHVN5WJFROV3O5',
            aws_secret_access_key='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',
            region_name='ap-southeast-1'
        )
        return client

    def get_connections(self):
        """
        Read connections file stored in S3 bucket.

        Returns:
            A list containing all the connections and their properties
        """ 
        log.info('Getting connections file from path %s in the bucket %s', self.configs['BrandRegion'], self.configs['Bucket'])
        response = self.client.get_object(
            Bucket = self.configs['Bucket'],
            Key = self.configs['BrandRegion']
        )
        connections = response['Body'].read().decode("utf-8").split(sep = "\n")
        SourceRecord = namedtuple('SourceRecord', connections[0][1:])
        connections = [SourceRecord(*(connection.split(',')[1:])) for connection in connections[1:-1]]
        return connections

    def get_load_settings(self) -> list[dict[str, str | int]]:
        """
        Read load settings file stored in S3 bucket.

        Returns:
            A list of dictionaries of all the connection with last updated date
        """
        log.info('Loading load settings from path %s', self.configs['LoadSetting'])
        response = self.client.get_object(
            Bucket = self.configs['Bucket'],
            Key = self.configs['LoadSetting']
        )
        load_settings = response['Body'].read().decode("utf-8").split(sep = "\n")
        load_settings = [{'Brand': load_setting.split(',')[0], 'Country': load_setting.split(',')[1], 'LastUpdatedTime': int(load_setting.split(',')[2])} for load_setting in load_settings[1:]]

        for connection in self.connections:
            found = any(load_setting['Brand'] == connection.Brand and load_setting['Country'] == connection.Country for load_setting in load_settings)
            if found is False:
                load_settings.append({'Brand': connection.Brand, 'Country': connection.Country, 'LastUpdatedTime': int(datetime(2020, 1, 1, 00, 00, 00).timestamp())})
        return load_settings

    def transfer_to_bucket(self, suffix: str, jsonl: str):
        """
        Transfer jsonl files to S3 bucket.

        Args:
            suffix: bucket path where data will be stored
            jsonl: contains data which will be dumped
        """
        log.info('Transferring to the path %s', self.configs['InputRaw'] +  suffix)
        self.client.put_object(
            Body = jsonl,
            Bucket = self.configs['Bucket'],
            Key = self.configs['InputRaw'] +  suffix
        )

    def cleanup_s3(self):
        """Remove all data from S3 and refresh load settings file for Full Load."""

        log.info('Cleaning up for S3 bucket %s Full Load', self.configs['Bucket'])
        self.client.delete_objects(
            Bucket = self.configs['Bucket'],
            Delete = {
                'Objects': [
                    {'Key': self.configs['InputRaw']},
                    {'Key': self.configs['LoadSetting']}
                ]
            }
        )
        self.client.put_object(
            Body = 'Brand,Country,LastUpdatedTime',
            Bucket = self.configs['Bucket'],
            Key = self.configs['LoadSetting']
        )

    def update_load_settings(self):
        """Update Load settings to current time after getting all the data."""

        log.info('Updating load settings in the path %s', self.configs['LoadSetting'])
        load_settings = "Brand,Country,LastUpdatedTime\n" + '\n'.join([','.join([str(e) for e in load_setting.values()]) for load_setting in self.load_settings])
        print(load_settings)
        self.client.put_object(
            Body = load_settings,
            Bucket = self.configs['Bucket'],
            Key = self.configs['LoadSetting']
        )

    @staticmethod
    def convert_to_jsonl(json_list):
        """Convert json list to jsonl. """

        log.info('Converting to jsonl')
        output = io.StringIO()
        orders_df = pd.DataFrame(json_list)
        orders_df.to_json(output, orient = 'records', lines=True)
        return output.getvalue()