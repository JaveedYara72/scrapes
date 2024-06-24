import os
from datetime import datetime, timedelta,date
from time import sleep
import pandas as pd
from pandas import json_normalize
from io import StringIO
import datetime
import boto3
import re
import csv
import pytz
import time
import hmac
import requests
import hashlib
import json
import io
import sys
from csv import writer

# # Amazon Creds
# AWS_ACCESS_KEY_ID = sys.argv[1]
# AWS_SECRET_ACCESS_KEY = sys.argv[2]
# s3_client = boto3.client('s3',
# 		aws_access_key_id= AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
# s3_resource = boto3.resource('s3',
# 		aws_access_key_id= AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# # S3 Creds and file location
# vBucket = 'una-brands-ops'
# my_bucket = s3_resource.Bucket(vBucket)
# vBrandRegionPrefix='data/prod/load_settings/shopee/brandregionfile.csv'
# vLoadSettingPrefix='data/prod/load_settings/shopee/loadSettings.csv'
# VInputRawPrifix='data/prod/landing_raw/shopee_returns_data/'
# vLoadLogsPrefix='data/prod/load_settings/shopee/loadLogs.csv'



# # fetch Brand Region data
# try:
# 	response = s3_client.get_object(Bucket=vBucket, Key=vBrandRegionPrefix)
# 	status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
# except:
# 	print('Brand Region file not found')
# 	exit()
# if (status == 200):
#     print(f"Successful S3 get_object response. Status - {status}")
#     df_brand_region = pd.read_csv(response.get("Body"), index_col=0)	
# else:
#     print(f"Unsuccessful S3 get_object response. Status - {status}")


dt = datetime.datetime(2020,1,1)
end = datetime.datetime(2020,3,2)
step = datetime.timedelta(seconds=86400)

result_unix = []

while dt < end:
    result_unix.append(int(time.mktime(dt.timetuple())))
    dt += step
    

for i in range(0,len(result_unix)):
	print(result_unix[i])



# read csv
df_brand_region=pd.read_csv("brandregionfile.csv")
print(df_brand_region)

# Converting dataframe to list
lBrandRegion = df_brand_region.values.tolist()
timezone = pytz.timezone("Asia/Singapore")

def get_access_token_shop_level(shop_id, partner_id, partner_key, refresh_token):
    timest = int(time.time())
    host = "https://partner.shopeemobile.com"
    path = "/api/v2/auth/access_token/get"
    
    body = {"shop_id": shop_id, "refresh_token": refresh_token, "partner_id": partner_id}
    
    base_string = "%s%s%s"%(partner_id ,path, timest)
    byte_partner_key = bytes(partner_key, 'UTF-8')  # key.encode() would also work in this case
    message = base_string.encode()
    sign = hmac.new(byte_partner_key, message, hashlib.sha256).hexdigest()
    url = host + path + f"?partner_id={partner_id}&timestamp={timest}&sign={sign}"
    
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url, json=body, headers=headers)
    
    return resp

def generate_sign(vaccesstoken, path,vpartnerid,vshopid,vpartnerkey):
    timest = int(time.time())
    host = "https://partner.shopeemobile.com"
    base_string = "%s%s%s%s%s"%(vpartnerid, path, timest, vaccesstoken, vshopid)
    sign = hmac.new(bytes(vpartnerkey, 'UTF-8'), base_string.encode(), hashlib.sha256).hexdigest()
    return timest, sign

def get_order_list(vaccesstoken, start_ts, end_ts, cursor,vpartnerid,vshopid,vpartnerkey):
    timest, sign = generate_sign(vaccesstoken, "/api/v2/order/get_order_list",vpartnerid,vshopid,vpartnerkey)
    base_url = "https://partner.shopeemobile.com/api/v2/order/get_order_list" 
    time_from = start_ts #1579132800
    time_to = end_ts #1580428800
    url = base_url + f"?partner_id={vpartnerid}&timestamp={timest}&access_token={vaccesstoken}&shop_id={vshopid}&sign={sign}&time_range_field=update_time&time_from={time_from}&time_to={time_to}&page_size=100&cursor={cursor}"
    headers = {"Content-Type": "application/json"}
    resp = requests.get(url, headers=headers)
    ret = json.loads(resp.content)
    print("inside get order list function")
    #print(len(ret['response']['order_list']))
    return ret


def get_order_details(vaccesstoken, order_sn_list,vpartnerid,vshopid,vpartnerkey):
    timest, sign = generate_sign(vaccesstoken, "/api/v2/order/get_order_detail",vpartnerid,vshopid,vpartnerkey)
    response_optional_fields = 'buyer_user_id,buyer_username,estimated_shipping_fee,recipient_address,actual_shipping_fee ,goods_to_declare,note,note_update_time,item_list,pay_time,dropshipper,credit_card_number ,dropshipper_phone,split_up,buyer_cancel_reason,cancel_by,cancel_reason,actual_shipping_fee_confirmed,buyer_cpf_id,fulfillment_flag,pickup_done_time,package_list,shipping_carrier,payment_method,total_amount,buyer_username,invoice_data'
    base_url = "https://partner.shopeemobile.com/api/v2/order/get_order_detail" 
    url = base_url + f"?partner_id={vpartnerid}&timestamp={timest}&access_token={vaccesstoken}&shop_id={vshopid}&sign={sign}&order_sn_list={order_sn_list}&response_optional_fields={response_optional_fields}"
    headers = {"Content-Type": "application/json"}
    resp = requests.get(url, headers=headers)
    ret = json.loads(resp.content)
    print("inside get order details function")
    return ret

def get_return_list(vaccesstoken,vpartnerid,vshopid,vpartnerkey,page_no,page_size,LastUpdatedDate,list):
	timest, sign = generate_sign(vaccesstoken,"/api/v2/returns/get_return_list",vpartnerid,vshopid,vpartnerkey)	
	base_url = "https://partner.shopeemobile.com/api/v2/returns/get_return_list" 
	print(LastUpdatedDate)
	# LastUpdatedDate=1672511400
	print(LastUpdatedDate)
	
	url = base_url + f"?partner_id={vpartnerid}&timestamp={timest}&access_token={vaccesstoken}&shop_id={vshopid}&sign={sign}&page_no={page_no}&page_size={page_size}&create_time_from=1676399400"
	headers = {"Content-Type": "application/json"}
	resp = requests.get(url, headers=headers)
	ret = json.loads(resp.content)
	print(ret)
	maxDate = LastUpdatedDate
	print(LastUpdatedDate)

	while True:
		if(ret['response']['more']) != False:
			for i in range(0,len(ret['response']['return'])):
				return_sn_list.append(ret['response']['return'][i]['return_sn'])
				if(ret['response']['return'][i]['create_time'] >= maxDate):
					maxDate = ret['response']['return'][i]['create_time']
					# print("Inside the first loop")
					# print(f"maxDate iteration  -> {maxDate}")
			page_no = page_no+1
			url = base_url + f"?partner_id={vpartnerid}&timestamp={timest}&access_token={vaccesstoken}&shop_id={vshopid}&sign={sign}&page_no={page_no}&page_size={page_size}&create_time_from=1676399400&create_time_to=1677560719"
			# url = base_url + f"?partner_id={vpartnerid}&timestamp={timest}&access_token={vaccesstoken}&shop_id={vshopid}&sign={sign}&page_no={page_no}&page_size={page_size}&create_time_from={LastUpdatedDate}"
			resp = requests.get(url, headers=headers)
			ret = json.loads(resp.content)
			returns_raw_data.append(ret)
		else:
			try:
				for i in range(0,len(ret['response']['return'])):
					return_sn_list.append(ret['response']['return'][i]['return_sn'])
					returns_raw_data.append(ret)
					if(ret['response']['return'][i]['create_time'] >= maxDate):
						maxDate = ret['response']['return'][i]['create_time']
						# print("Inside the second loop")
						# print(f"maxDate iteration  -> {maxDate}")
			except:
				print("ended")
			break

	# appending the max date
	list.append(maxDate)
	print(f"maximum date is {maxDate}")
	
	# dumping it into s3
	with open('returns_raw_data_inc.json', 'w', encoding='utf-8') as f:
		json.dump(returns_raw_data, f, ensure_ascii=False, indent=4)

def return_loadwrapper(brand,region,returnlist_loadSettings):
	df_load=pd.read_csv(returnlist_loadSettings)
	df_loadSetting = df_load[df_load['Brand'] == brand].sort_values(by='LastUpdatedDate')
	df_loadSetting = df_loadSetting[df_loadSetting['Region'] == region].sort_values(by='LastUpdatedDate')
	print(df_loadSetting)

	if (df_loadSetting.empty):
		print("Full Load")
		LastUpdatedDate = 1577817000

		# appending details into a list 
		list = []
		list.append(brand)
		list.append(region)
		print(f"Full Load {brand}, {region}")
		get_return_list(vaccesstoken,vpartnerid,vshopid,vpartnerkey,page_no,page_size,LastUpdatedDate,list)

		# writing it into a csv
		with open('returnlist_loadSettings.csv', 'a',newline='') as f_object:
			writer_object = writer(f_object)
			writer_object.writerow(list)
			f_object.close()

	else:
		print("Incremental Load")
		list = []
		list.append(brand)
		list.append(region)	
		LastUpdatedDate = df_loadSetting.iloc[-1][-1]
		get_return_list(vaccesstoken,vpartnerid,vshopid,vpartnerkey,page_no,page_size,LastUpdatedDate,list)

		# writing it into a csv
		with open('returnlist_loadSettings.csv', 'a',newline='') as f_object:
			writer_object = writer(f_object)
			writer_object.writerow(list)
			f_object.close()


def get_return_details(vaccesstoken,vpartnerid,vshopid,vpartnerkey):
    timest, sign = generate_sign(vaccesstoken, "/api/v2/returns/get_return_detail",vpartnerid,vshopid,vpartnerkey)
    base_url = "https://partner.shopeemobile.com/api/v2/returns/get_return_detail" 
    for i in range(0,len(return_sn_list)):
        url = base_url + f"?partner_id={vpartnerid}&timestamp={timest}&access_token={vaccesstoken}&shop_id={vshopid}&sign={sign}&return_sn={return_sn_list[i]}"
        headers = {"Content-Type": "application/json"}
        resp = requests.get(url, headers=headers)
        ret = json.loads(resp.content)
        return_list_data.append(ret)

    print(len(return_list_data))

	# dumping it into a json file
    with open('returns_data', 'w', encoding='utf-8') as f:
        json.dump(return_list_data, f, ensure_ascii=False, indent=4)	
    
def get_escrow_list(vaccesstoken,vpartnerid,vshopid,vpartnerkey,page_no,page_size,release_time_from,release_time_to):
	timest, sign = generate_sign(vaccesstoken,"/api/v2/payment/get_escrow_list",vpartnerid,vshopid,vpartnerkey)	
	base_url = "https://partner.shopeemobile.com/api/v2/payment/get_escrow_list" 
	url = base_url + f"?partner_id={vpartnerid}&timestamp={timest}&access_token={vaccesstoken}&shop_id={vshopid}&sign={sign}&page_no={page_no}&page_size={page_size}&release_time_from={release_time_from}&release_time_to={release_time_to}"
	headers = {"Content-Type": "application/json"}
	resp = requests.get(url, headers=headers)
	ret = json.loads(resp.content)
	

	while True:
		if(ret['response']['more']) != False:
			for i in range(0,len(ret['response']['escrow_list'])):
				payment_sn_list.append(ret['response']['escrow_list'][i]['order_sn'])
			page_no = page_no+1
			url = base_url + f"?partner_id={vpartnerid}&timestamp={timest}&access_token={vaccesstoken}&shop_id={vshopid}&sign={sign}&page_no={page_no}&page_size={page_size}&release_time_from={release_time_from}&release_time_to={release_time_to}"
			resp = requests.get(url, headers=headers)
			ret = json.loads(resp.content)
			payment_raw_data.append(ret)
		else:
			try:
				for i in range(0,len(ret['response']['escrow_list'])):
					payment_sn_list.append(ret['response']['escrow_list'][i]['order_sn'])
					payment_raw_data.append(ret)
			except:
				print("ended")
			break		

	# dumping it into s3
	with open('payment_raw_data.json', 'w', encoding='utf-8') as f:
		json.dump(payment_raw_data, f, ensure_ascii=False, indent=4)

def escrow_loadwrapper(vBrand,vRegion,vaccesstoken,vpartnerid,vshopid,vpartnerkey,page_no,page_size,escrowlist_loadSettings):
	df_load=pd.read_csv(escrowlist_loadSettings)
	df_loadSetting = df_load[df_load['Brand'] == vBrand].sort_values(by='LastUpdatedDate')
	df_loadSetting = df_loadSetting[df_loadSetting['Region'] == vRegion].sort_values(by='LastUpdatedDate')

	if (df_loadSetting.empty):
		print("Full Load")
		get_escrow_list(vaccesstoken,vpartnerid,vshopid,vpartnerkey,page_no,page_size,result_unix[0],result_unix[-1])
		print(result_unix[0])
		print(result_unix[-1])
		
		# appending it into a df and then writing it into the csv
		df_load.loc[len(df_load.index)] = [vBrand,vRegion,result_unix[-1]]
		df_load.to_csv('escrowlist_loadSettings.csv')
	else:
		print("Incremental Load")	
		UpdatedDate = df_loadSetting.iloc[-1][-1]
		print(UpdatedDate)
        
		for i in range(0,len(result_unix)):
			if(UpdatedDate>result_unix[i]):
				pass
			else:
				print(f"running incremental load for -> {result_unix[i]}")
				get_escrow_list(vaccesstoken,vpartnerid,vshopid,vpartnerkey,page_no,page_size,UpdatedDate,result_unix[i])
		
		
		# appending it into a df and then writing it into the csv
		df_load.loc[len(df_load.index)] = [vBrand,vRegion,result_unix[-1]]
		df_load.to_csv('escrowlist_loadSettings.csv')

def get_escrow_details(vaccesstoken,vpartnerid,vshopid,vpartnerkey):
    timest, sign = generate_sign(vaccesstoken, "/api/v2/payment/get_escrow_detail",vpartnerid,vshopid,vpartnerkey)
    base_url = "https://partner.shopeemobile.com/api/v2/payment/get_escrow_detail" 
    for i in range(0,len(payment_sn_list)):
        url = base_url + f"?partner_id={vpartnerid}&timestamp={timest}&access_token={vaccesstoken}&shop_id={vshopid}&sign={sign}&order_sn={payment_sn_list[i]}"
        headers = {"Content-Type": "application/json"}
        resp = requests.get(url, headers=headers)
        ret = json.loads(resp.content)
        payment_list_data.append(ret)

    print(len(payment_list_data))

	# dumping it into a json file
    with open('payments_data', 'w', encoding='utf-8') as f:
        json.dump(payment_list_data, f, ensure_ascii=False, indent=4)	
	



ltokens = []
print("Testing the repository")
# Loop around all the brand from Brand Region data
for i in range(5,6):
	# Data Structures needed to store the data	
	return_sn_list = []
	return_list_data = []
	returns_raw_data = []

	payment_sn_list = []
	payment_list_data = []
	payment_raw_data = []


	#vLatestUpdatedDateTime = datetime.datetime.now()
	#vLatestUpdatedDateTimeFile=re.sub(r' ','T',str(vLatestUpdatedDateTime))
	vBrand=lBrandRegion[i][0]
	vRegion=lBrandRegion[i][1]
	vshopid=lBrandRegion[i][2]
	vpartnerid=lBrandRegion[i][6]
	vpartnerkey=lBrandRegion[i][5]
	vaccesstoken =lBrandRegion[i][3]
	vrefreshtoken =lBrandRegion[i][4]

	# Return parameters
	page_no = 1
	page_size = 100

	print("printing creds")
	print(vshopid)
	print(vpartnerid)
	print(vpartnerkey)
	print(vrefreshtoken)
	print(vBrand)
	print(vRegion)

	# access token
	resp = get_access_token_shop_level(vshopid, vpartnerid, vpartnerkey, vrefreshtoken)
	ret = json.loads(resp.content)
	print(ret)

	vaccesstoken = ret.get("access_token")
	vrefreshtoken = ret.get("refresh_token")
	print("Acessssssssssss Tokensssssssssssssssss")
	print(vaccesstoken)
	print(vrefreshtoken)


	ltokens.append(vaccesstoken)
	ltokens.append(vrefreshtoken)
	ltokens.append(vBrand)
	ltokens.append(vRegion)

	df_tokens= pd.DataFrame(ltokens)
	# df_tokens.to_csv("tokenssss_testings3.csv")

	# logic to get the maxupdated time
	loadSettings='C:/Users/Y Javeed/Downloads/Una Brands/Python/Scripting/scripts/Shopee/new_loadSettings.csv'
	escrowlist_loadSettings = 'C:/Users/Y Javeed/Downloads/Una Brands/Python/Scripting/scripts/Shopee/escrowlist_loadSettings.csv'
	returnlist_loadSettings = 'C:/Users/Y Javeed/Downloads/Una Brands/Python/Scripting/scripts/Shopee/returnlist_loadSettings.csv'

	# # To get the most recent date
	# df_load=pd.read_csv(loadSettings,index_col=0)
	# df_loadSetting = df_load[df_load['Brand'] == vBrand].sort_values(by='LastUpdatedDate')
	# df_loadSetting = df_loadSetting[df_loadSetting['Region'] == vRegion].sort_values(by='LastUpdatedDate')
	# LastUpdatedDate = df_loadSetting.iloc[-1][-1]

	# Today's Date
	d = datetime.datetime.now()
	unixtime = time.mktime(d.timetuple())
	unixtime_ = int(unixtime)

	# print("running load wrapper")
	# return_loadwrapper(vBrand,vRegion,returnlist_loadSettings)

	print("running escrow load wrapper")
	escrow_loadwrapper(vBrand,vRegion,vaccesstoken,vpartnerid,vshopid,vpartnerkey,page_no,page_size,escrowlist_loadSettings)
	# get_escrow_list(vaccesstoken,vpartnerid,vshopid,vpartnerkey,page_no,page_size,LastUpdatedDate,unixtime_)

	exit()

	# with open("filess_testings3.txt", "a") as att_file: # 4b5478544c476a5374577142527a717a 6a63476c65685a747672434e514a4469
	# 	for item in ltokens:  # 78794a4d785672644e57736f426e4977  444d4e684c4c6671446c704449416f4c
	# 		att_file.write(item + "\n") # 74787254507771514b4c524a78566545  626d486c68726165774a6f7476505967

	csv_buffer_load_log = StringIO()
	df_brand_region.loc[i,'RefreshToken']=vrefreshtoken
	df_brand_region.loc[i,'AccessToken']=vaccesstoken
	df_brand_region.to_csv(csv_buffer_load_log)
	s3_resource.Object(vBucket, 'data/prod/load_settings/shopee/brandregionfile1.csv').put(Body=csv_buffer_load_log.getvalue())	
	

	vLoadStartDateTime=datetime.datetime.now()

	# #Check if LoadSettingsFile Exists and load csv into dataframe
	# try:
	# 	print("Check if LoadSettingsFile Exists and load csv into dataframe",vLoadSettingPrefix)
	# 	response_load = s3_client.get_object(Bucket=vBucket, Key=vLoadSettingPrefix)
	# 	status_load = response_load.get("ResponseMetadata", {}).get("HTTPStatusCode")
	# 	if (status_load == 200):
	# 		print(f"Successful S3 get_object response. Status - {status_load}")
	# 		df_load=pd.read_csv(response_load.get("Body"),index_col=0)
	# 		print(df_load)
	# 		df_loadSetting = df_load[df_load['Brand'] == vBrand].sort_values(by='LastUpdatedDate')
	# 		df_loadSetting = df_loadSetting[df_loadSetting['Region'] == vRegion].sort_values(by='LastUpdatedDate')			
	# 		print("data from load settings file")
	# 		print(df_loadSetting)
	# 		if df_loadSetting.empty:
	# 			vFullLoadRun=1
	# 			print("FULLLLLLLLLLLLLLLLLLL LOAAAAAAAAAAAAAAADDDDDDDDDDDDDDDD")
	# 		else:
	# 			print("INCREMMMMMEEEEENTALLLL LLLLOOOAAAAAADDDDDD")
	# 			vLastUpdatedDate=df_loadSetting.iloc[-1][-1]
	# 			print(vLastUpdatedDate)
	# 			#vLastUpdatedDate = datetime.datetime.strptime(vLastUpdatedDateTime, '%Y-%m-%d %H:%M:%S.%f').timestamp()
	# 			#print(vLastUpdatedDate)
	# 			print(type(vLastUpdatedDate))
	# 			#vLastUpdatedTime = re.sub(r'\d{4}-\d{2}-\d{2}', '', vLastUpdatedDateTime)
	# 			#print(vLastUpdatedTime)
	# 			vFullLoadRun=0	
	# 	else:
	# 		print(f"Unsuccessful S3 get_object response for load setting file for {vBrand} Status - {status}")
	# 		continue
	# except:
	# 	print('load Setting file not found.......inside except')
	# 	vFullLoadRun=1
	

	# if vFullLoadRun==1:
	# 	vLastUpdatedDate=int(datetime.datetime(2020, 1, 1, 00, 00,00).replace(tzinfo = timezone).timestamp())
	# 	vCreatedBeforeDate = int(datetime.datetime.now().timestamp())
	# 	vLastUpdatedTime=None

	# 	# delete all files  for the brand and region in input raw Bucket
	# 	my_bucket.objects.filter(Prefix='{}{}/'.format(VInputRawPrifix,vBrand)).delete()

	# else:
	# 	vCreatedBeforeDate = int(datetime.datetime.now().timestamp())

	# interval = int(datetime.timedelta(days=1).total_seconds())
	# order_list = []
	# counter=1

	# vExtractStartDateTime=datetime.datetime.now()
	# print("Start time :->>>>>>>>>>>>>>>",vLastUpdatedDate)
	# print("End time :->>>>>>>>>>>>>>>",vCreatedBeforeDate)
	# for time_from in range(int(vLastUpdatedDate), vCreatedBeforeDate, interval):
	# 	cursor = 0
	# 	while True:
	# 		# print(cursor)
	# 		# print(i)
	# 		# print(time_from)
	# 		# print(time_from + interval)
	# 		try:
	# 			ret = get_order_list(vaccesstoken, time_from, time_from + interval, cursor,vpartnerid,vshopid,vpartnerkey)
	# 			order_list += ([order['order_sn'] for order in ret.get('response').get('order_list')])
	# 			#print(ret['response'])
	# 			if not ret['response']['more']:
	# 				break
	# 			cursor += 100
	# 		except:
	# 			break
	# 	counter=counter+1

	# print(len(order_list))
	# print("Number of orderssssssssssssssssss")
	
	# if len(order_list)==0:
	# 	print("No new orders since last run")
	# 	continue
	
	# order details
	# order_details = []
	# df_datajson = pd.DataFrame()
	# for i in range(0, len(order_list), 50):
	# 	print(i,"order details")
	# 	order_sn_list = ','.join([str(x) for x in order_list[i:i+50]])
	# 	try:
	# 		ret = get_order_details(vaccesstoken, order_sn_list,vpartnerid,vshopid,vpartnerkey)
	# 		order_details += ret["response"]["order_list"]
	# 		df_datajson += pd.DataFrame.from_dict(ret["response"]["order_list"])
	# 	except:
	# 		print("didnt get data for -->",i)
	# 		continue
	# print("Starting for logistics now")
	# for i in range(0,len(order_details)):
	# 	try:
	# 		print(i)
	# 		ret = get_logistics(vaccesstoken, vpartnerid, vshopid, vpartnerkey, order_details[i]['order_sn'])
	# 		order_details[i]['logistics']=ret
	# 	except Exception as e:
	# 		print('error while fetching logistics for order id ----{} as exception -----{}'.format(order_details[i]['order_sn'],e))
	# 		continue

	# #print(order_details)
	# print("printing order details")
	# #with open('data_jan_2401.json', 'w', encoding='utf-8') as f:
	# #	json.dump(order_details, f, ensure_ascii=False, indent=4)

	#returns details
	# return_details = []
	# df_datajson = pd.DataFrame()
	# for i in range(0, len(order_list), 50):
	# 	print(i,"returns details")
	# 	returns_sn_list = ','.join([str(x) for x in order_list[i:i+50]])
	# 	try:
	# 		ret = get_return_list(vaccesstoken, return_sn_list,vpartnerid,vshopid,vpartnerkey)
	# 		return_details += ret["response"]["return_list"]
	# 		df_datajson += pd.DataFrame.from_dict(ret["response"]["return_list"])
	# 	except:
	# 		print("didnt get data for -->",i)
	# 		continue
	# print("Starting for logistics now")
	# for i in range(0,len(return_details)):
	# 	try:
	# 		print(i)
	# 		ret = get_logistics(vaccesstoken, vpartnerid, vshopid, vpartnerkey, return_details[i]['return_sn'])
	# 		return_details[i]['logistics']=ret
	# 	except Exception as e:
	# 		print('error while fetching logistics for return id ----{} as exception -----{}'.format(return_details[i]['return_sn'],e))
	# 		continue

	# #print(returns_details)
	# print("printing returns details")
	# #with open('returns_data.json', 'w', encoding='utf-8') as f:
	# #	json.dump(return_details, f, ensure_ascii=False, indent=4)
	
	# #s3 = boto3.resource('s3')
	# #s3object = s3_resource.Object(vBucket, "{}/a.json".format(VInputRawPrifix))

	# #s3object.put(
	# #	Body=(bytes(json.dumps(order_details).encode('UTF-8')))
	# #)

	# # Write order file in input_raw
	# if len(order_details)!=0:
	# 	print("line no 242")
	# 	tempts=[]
	# 	for i in range(0,len(order_details)):
	# 		tempts.append(int(order_details[i]['update_time']))	        
	# 	vLatestUpdatedDateTime=max(tempts)
	# 	#vLatestUpdatedDateTimeFile = vLatestUpdatedDateTime
	# 	vLatestUpdatedDateTimef = datetime.datetime.now()
	# 	vLatestUpdatedDateTimeFile=re.sub(r' ','T',str(vLatestUpdatedDateTimef))
	# else:
	# 	print("line no 246")
	# 	vLatestUpdatedDateTime = datetime.datetime.now()
	# 	vLatestUpdatedDateTimeFile=re.sub(r' ','T',str(vLatestUpdatedDateTime))
	
	# print("vLatestUpdatedDateTime for this run is : ->>>>>>>>>>>",vLatestUpdatedDateTime)    
	# vExtractEndDateTime=datetime.datetime.now()	
	# #my_bucket.put_object(Key=destination, Body=json_buffer.getvalue())
	# s3_resource.Object(vBucket, '{}{}/orders/{}_order_inc_{}.json'.format(VInputRawPrifix,vBrand,vRegion,vLatestUpdatedDateTimeFile)).put(Body=bytes(json.dumps(order_details).encode('UTF-8')))	

	# vLoadEndDateTime=datetime.datetime.now()
	# # escrow_details = []
	# # for i in range(0, len(order_list)):
	# # 	print(i)
	# # 	ret = get_escrow_details(vaccesstoken, order_list[i],vpartnerid,vshopid,vpartnerkey)
	# # 	try:
	# # 		escrow_details.append(ret['response'])
	# # 	except:
	# # 		continue

	# # VInputRawPrifix_escrow = 'data/source-data/tejas_test/shopee_escrow_data/'
	# # s3_resource.Object(vBucket, '{}{}/{}_escrowdata_inc_{}.json'.format(VInputRawPrifix_escrow,vBrand,vRegion,vLatestUpdatedDateTimeFile)).put(Body=bytes(json.dumps(escrow_details).encode('UTF-8')))	

	# # update load setting
	# try:
	# 	df_load.loc[len(df_load.index)] = [vBrand, vRegion, vLatestUpdatedDateTime]
	# except:
	# 	print('load logs file does not exist')
	# 	data = [[vBrand, vRegion, vLatestUpdatedDateTime]]
	# 	df_load = pd.DataFrame(data, columns = ['Brand', 'Region','LastUpdatedDate'])
	# 	print(df_load)
	# csv_buffer_load = StringIO()
	# print(csv_buffer_load)
	# df_load.to_csv(csv_buffer_load)
	# print(df_load)
	# s3_resource.Object(vBucket, vLoadSettingPrefix).put(Body=csv_buffer_load.getvalue())		

	# # update load logs
	# try:
	# 	response_load_log = s3_client.get_object(Bucket=vBucket, Key=vLoadLogsPrefix)
	# 	status_load_log = response_load_log.get("ResponseMetadata", {}).get("HTTPStatusCode")	

	# 	if (status_load_log == 200):
	# 		print(f"Successful S3 get_object response. Status - {status_load_log}")
	# 		df_load_log=pd.read_csv(response_load_log.get("Body"), index_col=0)
	# 		df_load_log.loc[df_load_log['LatestRun'] == 1, 'LatestRun'] = 0
	# 		df_load_log.loc[len(df_load_log.index)] = [vBrand, vRegion, vLoadStartDateTime,vLoadEndDateTime,vExtractStartDateTime,vExtractEndDateTime,len(order_list),1]
	# 	else:
	# 		print("Unsuccessful S3 get_object response for load logs. Note:- Load log file not updated. Status - {status}")

	# except:
	# 	print('load logs file does not exist')
	# 	data = [[vBrand, vRegion, vLoadStartDateTime,vLoadEndDateTime,vExtractStartDateTime,vExtractEndDateTime,len(order_list),1]]
	# 	df_load_log = pd.DataFrame(data, columns = ['Brand','Country','LoadStartDateTime','LoadEndDateTime','ExtractStartDateTime','ExtractEndDateTime','ExtractedOrderCount','LatestRun'])
	# print(df_load_log)
	# csv_buffer_load_log = StringIO()
	# df_load_log.to_csv(csv_buffer_load_log)
	# s3_resource.Object(vBucket, vLoadLogsPrefix).put(Body=csv_buffer_load_log.getvalue())
	# #get escrow data after updating the log files
	# # escrow_details = []
	# # for i in range(0, len(order_list)):
	# # 	print(i)
	# # 	ret = get_escrow_details(vaccesstoken, order_list[i],vpartnerid,vshopid,vpartnerkey)
	# # 	try:
	# # 		escrow_details.append(ret['response'])
	# # 	except:
	# # 		continue

	# s3_resource.Object(vBucket, '{}returnorder_list/{}/{}/returnorder_list{}.json'.format(VInputRawPrifix,vBrand,vRegion,vLatestUpdatedDateTimeFile)).put(Body=bytes(json.dumps(returns_raw_data).encode('UTF-8')))
	# s3_resource.Object(vBucket, '{}returnorder_details/{}/{}/returnorder_details{}.json'.format(VInputRawPrifix,vBrand,vRegion,vLatestUpdatedDateTimeFile)).put(Body=bytes(json.dumps(return_list_data).encode('UTF-8')))
	s3_resource.Object(vBucket, '{}transaction_details/{}/{}/transaction_list{}.json'.format(VInputRawPrifix,vBrand,vRegion,vLatestUpdatedDateTimeFile)).put(Body=bytes(json.dumps(payment_raw_data).encode('UTF-8')))
	s3_resource.Object(vBucket, '{}transaction_details/{}/{}/transaction_details{}.json'.format(VInputRawPrifix,vBrand,vRegion,vLatestUpdatedDateTimeFile)).put(Body=bytes(json.dumps(payment_list_data).encode('UTF-8')))