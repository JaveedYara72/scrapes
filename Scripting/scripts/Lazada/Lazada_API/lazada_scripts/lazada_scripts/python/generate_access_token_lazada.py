import lazop
#url="https://api.lazada.com/rest"
#appkey=106578
#appSecret="fwsu14kUwBIomgPhxtmI00s6vRnssRCs"
#client = lazop.LazopClient(url, appkey ,appSecret)
#request = lazop.LazopRequest('/auth/token/create')
#request.add_api_param('code', '0_106578_etEKPEAclF6MD2gKun7m31y695972')
##request.add_api_param('uuid', '38284839234')
#response = client.execute(request)
#print(response.type)
#print(response.body)

client = lazop.LazopClient('https://api.lazada.sg/rest', '109756' ,'B28Uimn8IXv9kHsfxPYsy72s8ksqLCg8')
request = lazop.LazopRequest('/auth/token/create')
request.add_api_param('code', '0_109756_5XNNRxurDLSyHnlyoyr01Rdj5411')
response = client.execute(request)
print(response)