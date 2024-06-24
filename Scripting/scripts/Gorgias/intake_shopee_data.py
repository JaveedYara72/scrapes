import itertools
import json
import sys
import os
import asyncio
import time
import hmac
import hashlib
from datetime import datetime, timedelta

from aiohttp import ClientSession
sys.path.append(os.getcwd()+'/scripts')
import common_functions
from random import randint

class ApiCalls:
    """Parent class to hold necessary information required for making api requests.

    Attributes:
        semaphore: A static semaphore which regulates access to a shared resource.
        url: Api domain to which api calls will be made.
        common parameter: Parameters required to make api calls which are common for all of them.
        session: A client session made prior to making http requests.
        brand: Name of brand.
        country: Name of country where the brand is located.
    """

    semaphore = asyncio.Semaphore(1000)
    def __init__(self, connection, session: ClientSession):
        """Initialises instance based on a connection and session."""

        self.url = "https://partner.shopeemobile.com"
        self.common_parameter = {
            'partner_id' : connection.Partnerid,
            'timestamp' : None,
            'access_token' : connection.AccessToken,
            'shop_id' : connection.Shopid,
            'sign' : None
        }
        self.partner_key = connection.PartnerKey.encode()
        self.session = session
        self.brand = connection.Brand
        self.country = connection.Country

    def calculate_sign(self, api_path: str):
        """Calculates sign which is a common parameter.

        Sign is calculated based on other common paramters
        with sha256 algorithm.

        Args:
            api_path: path for api calls in api domain

        Returns:
            Calculated sign
        """
        msg = f"{self.common_parameter['partner_id']}{api_path}{self.common_parameter['timestamp']}{self.common_parameter['access_token']}{self.common_parameter['shop_id']}".encode()
        sign = hmac.new(self.partner_key, msg, hashlib.sha256).hexdigest()
        return sign

    def update_time_sign(self, api_path: str):
        """Update timestamp and sign which are common parameters.

        These are updated before every api call
        as their limit is 5 mins
        """
        self.common_parameter['timestamp'] = int(time.time())
        self.common_parameter['sign'] = self.calculate_sign(api_path)

class Order(ApiCalls):
    """Access Order API of shopee.

    Attributes:
        request_parameter: parameters required to make api calls which are different for each type of api calls
    """
    def __init__(self, connection: dict, session: ClientSession):
        super().__init__(connection, session)
        self.request_parameter = {}

    async def get_order_list(self, time_from: int, time_to: int):
        """Gets order list via api call.

        Yields:
            A list containing unique identifier of all orders.
        """
        log.info('Getting order list for orders of  Brand = %s, Country = %s', self.brand, self.country)
        api_path = "/api/v2/order/get_order_list"
        self.url += api_path
        self.request_parameter['time_range_field'] = 'update_time'
        self.request_parameter['page_size'] = 100
        order_sn_list = []
        coros = []
        time_till = time_to
        time_to = min(time_till, time_from + int(timedelta(days = ORDER_LIST_INTERVAL).total_seconds())) #modify time_to if interval exceeds ORDER_LIST_INTERVAL
        # make coroutines for api calls based with interval as maximum of ORDER_LIST_INTERVAL
        while time_from < time_till:
            coros.append(self.get_order_list_per_intervals(api_path, time_from, time_to))
            time_from = time_to
            time_to = min(time_till, time_from + int(timedelta(days = ORDER_LIST_INTERVAL).total_seconds()))
        # await as coroutines get completed an yield the result
        # as soon as size of order sn list exceeds BATCH_SIZE
        for get_order_list_per_interval in asyncio.as_completed(coros):
            order_sn_list += await get_order_list_per_interval
            if len(order_sn_list) > common_functions.BATCH_SIZE:
                yield order_sn_list
                order_sn_list.clear()

        yield order_sn_list

    async def get_order_list_per_intervals(self, api_path, time_from, time_to):
        """Fetches order sn for a given time interval.

        Args:
            api_path: Path for api calls in api domain.
            time_from: Time after which we need order sn.
            time_to: Time before which we need order sn.

        Returns:
            A list containing serial numbers of unique identifier of orders
        """
        request_parameter = self.request_parameter.copy()
        request_parameter['time_from'] = time_from
        request_parameter['time_to'] = time_to
        request_parameter['cursor'] = ""
        order_sn_list = []

        attempt = 0
        while attempt <= RETRIES:
            attempt+=1
            # if more request are ready to be made till limit is reached
            # wait for those subsequent request
            while ApiCalls.semaphore.locked():
                await asyncio.sleep(randint(0, 10))
            async with ApiCalls.semaphore :
                log.info('Running for Brand = %s, Country = %s for Time between %s and %s', self.brand, self.country, datetime.fromtimestamp(time_from), datetime.fromtimestamp(time_to))
                self.update_time_sign(api_path)
                try:
                    async with self.session.get(self.url, params = self.common_parameter | request_parameter) as response:
                        response = await response.json()
                        if response['error']:
                            raise Exception(response['message'])
                        response = response['response']
                        order_sn_list += [order['order_sn'] for order in response['order_list']]
                        # access more data with moving cursor through pagination
                        while response['more']:
                            request_parameter['cursor'] = response['next_cursor']
                            self.update_time_sign(api_path)
                            async with self.session.get(self.url, params = self.common_parameter | request_parameter) as response:
                                response = await response.json()
                                if response['error']:
                                    raise Exception(response['message'])
                                response = response['response']
                                order_sn_list += [order['order_sn'] for order in response['order_list']]
                        log.info('Got %s records of Brand = %s, Country = %s for Time between %s and %s', len(order_sn_list), self.brand, self.country, datetime.fromtimestamp(time_from), datetime.fromtimestamp(time_to))
                        return order_sn_list
                except Exception as e:
                    log.error(e.args)
                    log.error('Failed for Brand = %s, Country = %s for Time between %s and %s', self.brand, self.country, datetime.fromtimestamp(time_from), datetime.fromtimestamp(time_to))
                    order_sn_list.clear()
                    await asyncio.sleep(randint(0, 10))

        return order_sn_list

    async def get_order_details(self, order_sn_list: str):
        """Get order details based on serial number of an order

        Args:
            order_sn_list: A comma seperated string containing atmost 50 unique identifiers of orders.

        Returns:
            A list containing order details of all the passed unique identifier of orders.
        """
        api_path = "/api/v2/order/get_order_detail"
        self.url += api_path
        self.request_parameter['order_sn_list'] = order_sn_list

        attempt = 0
        while attempt <= RETRIES:
            attempt += 1
            while ApiCalls.semaphore.locked():
                await asyncio.sleep(randint(0, 10))
            async with ApiCalls.semaphore :
                log.info('Getting order details for Orders = %s of Brand = %s, Country = %s', order_sn_list, self.brand, self.country)
                self.update_time_sign(api_path)
                try:
                    async with self.session.get(self.url, params = self.common_parameter | self.request_parameter) as response:
                        response = await response.json()
                        if response['error']:
                            raise Exception(response['message'])
                        return response['response']['order_list']
                except Exception as e:
                    log.error(e.args)
                    log.error(f"Failed attempt no. {attempt} for order details for Orders = {order_sn_list} of Brand = {self.brand}, Country = {self.country}")
                    await asyncio.sleep(randint(0, 10))

        return []

class Logistics(ApiCalls):
    """Access Logistics API of shopee.

    Attributes:
        request_paramter: Parameters required to make api calls which are different for each type of api calls.
    """
    def __init__(self, connection, session):
        super().__init__(connection, session)
        self.request_parameter = {}

    async def get_tracking_number(self, order: dict):
        """Get tracking number based on unique identifier of an order

        Args:
            order: A dict containing order details of an order

        Returns:
            A dict containing order details of an order with added key of tracking number
            if it exists for a given order
        """
        api_path = "/api/v2/logistics/get_tracking_number"
        self.url += api_path
        self.request_parameter['order_sn'] = order['order_sn']
        order['tracking_number'] = None

        attempt = 0
        while attempt <= RETRIES:
            attempt += 1
            while ApiCalls.semaphore.locked():
                await asyncio.sleep(randint(0, 10))
            async with ApiCalls.semaphore :
                log.info('Getting tracking number for Order = %s of Brand = %s, Country = %s', order['order_sn'], self.brand, self.country)
                self.update_time_sign(api_path)
                try:
                    async with self.session.get(self.url, params = self.common_parameter | self.request_parameter) as response:
                        response = await response.json()
                        if response['error'].startswith('error'):
                            raise Exception(response['message'])
                        elif response['error']:
                            log.info(f"{response['message']} for Order = {order['order_sn']} of Brand = {self.brand}, Country = {self.country}")
                        else:
                            order['tracking_number'] = response['response']['tracking_number']
                        return order
                except Exception as e:
                    log.error(e.args)
                    log.error(f"Failed attempt no. {attempt} for tracking number for Order = {order['order_sn']} of Brand = {self.brand}, Country = {self.country}")
                    await asyncio.sleep(randint(0, 10))

        return order

class Payment(ApiCalls):
    """Access Payment API of shopee.

    Attributes:
        request_paramter: Parameters required to make api calls which are different for each type of api calls.
    """
    def __init__(self, connection, session):
        super().__init__(connection, session)
        self.request_parameter = {}

    async def get_escrow_details(self, order_sn: str):
        """Get escrow details based on unique identifier of an order.

        Args:
            order_sn: Shopee's unique identifier for an order.

        Returns:
            A dict containing escrow details of an order if it exists.
        """
        api_path = "/api/v2/payment/get_escrow_detail"
        self.url += api_path
        self.request_parameter['order_sn'] = order_sn

        attempt = 0
        while attempt <= RETRIES:
            attempt += 1
            while ApiCalls.semaphore.locked():
                await asyncio.sleep(randint(0, 10))
            async with ApiCalls.semaphore :
                log.info('Getting escrow details for Order = %s of Brand = %s, Country = %s', order_sn, self.brand, self.country)
                self.update_time_sign(api_path)
                try:
                    async with self.session.get(self.url, params = self.common_parameter | self.request_parameter) as response:
                        response = await response.json()
                        if response['error']:
                            raise Exception(response['message'])
                        return response['response']
                except Exception as e:
                    log.error(e.args)
                    log.error(f"Failed attempt no. {attempt} for escrow details for Order = {order_sn} of Brand = {self.brand}, Country = {self.country}")
                    await asyncio.sleep(randint(0, 10))

        return {}


async def fetch_data(connection, session: ClientSession):
    """Fetches all the data for a particular brand-region.

    Args:
        connection: Info about a particular brand-region.
        session: Client Session which will be used to make api calls.
    """

    log.info('Fetching last updated time for %s and %s', connection.Brand, connection.Country)
    last_updated_time = [int(load_setting['LastUpdatedTime']) for load_setting in shopee_obj.load_settings if load_setting['Brand'] == connection.Brand and load_setting['Country'] == connection.Country][0]
    curr_time = int(time.time())

    log.info('Making batches to get order list for %s and %s', connection.Brand, connection.Country)
    batches = Order(connection, session).get_order_list(last_updated_time, curr_time)
    batch = 0
    #traverse through all the batches of order sn
    async for order_sn_list in batches:

        log.info('Getting order details for orders of batch no. %s of Brand = %s, Country = %s', batch, connection.Brand, connection.Country)
        async_tasks = [asyncio.create_task(Order(connection, session).get_order_details(",".join(order_sn_list[i:i+50]))) for i in range(0, len(order_sn_list), 50)]
        order_list = list(itertools.chain.from_iterable(await asyncio.gather(*async_tasks)))

        log.info('Getting tracking number for orders of batch no. %s of Brand = %s, Country = %s', batch, connection.Brand, connection.Country)
        async_tasks = [asyncio.create_task(Logistics(connection, session).get_tracking_number(order)) for order in order_list]
        order_list = await asyncio.gather(*async_tasks)

        log.info('Gathered order details of batch no. %s with %s lines of data of Brand = %s, Country = %s', batch, len(order_list), connection.Brand, connection.Country)
        output_jsonl_file = '\n'.join([json.dumps(line) for line in order_list])
        shopee_obj.transfer_to_bucket(f"brand={connection.Brand}/country={connection.Country}/orders/{curr_time}_{batch}.jsonl", output_jsonl_file)

        log.info('Getting escrow details for orders of batch no. %s of Brand = %s, Country = %s', batch, connection.Brand, connection.Country)
        async_tasks = [asyncio.create_task(Payment(connection, session).get_escrow_details(order)) for order in order_sn_list]
        escrow_details = await asyncio.gather(*async_tasks)

        log.info('Gathered escrow details of batch no. %s with %s lines of data of Brand = %s, Country = %s', batch, len(escrow_details), connection.Brand, connection.Country)
        output_jsonl_file = '\n'.join([json.dumps(line) for line in escrow_details])
        shopee_obj.transfer_to_bucket(f"brand={connection.Brand}/country={connection.Country}/payment/{curr_time}_{batch}.jsonl", output_jsonl_file)

        batch += 1

    # updating last updated time for each connection
    for load_setting in shopee_obj.load_settings:
        if load_setting['Brand'] == connection.Brand and load_setting['Country'] == connection.Country:
            load_setting['LastUpdatedTime'] = curr_time

    log.info('Successfuly transferred data of Brand = %s, Country = %s', connection.Brand, connection.Country)

async def main():
    log.info('Running tasks for all the brands - region')

    async with ClientSession() as session:
        # creating coroutines and scheduling its execution
        coros = [asyncio.create_task(fetch_data(connection, session)) for connection in shopee_obj.connections]
        # awaitning for all coroutines to complete
        await asyncio.gather(*coros)

    shopee_obj.update_load_settings()


if __name__ == "__main__":
    ORDER_LIST_INTERVAL = 15 #time interval for which we can fetch order sn at a time
    RETRIES = 10 #no of retires on any request failure
    print("Setting up log")
    log = common_functions.Source.set_logger("Shopee")
    shopee_obj = common_functions.Source(env = sys.argv[1], source='shopee', full_load= bool(sys.argv[2]))
    asyncio.run(main())