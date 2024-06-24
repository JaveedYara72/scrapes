import json
import platform
import asyncio
import keepa
import numpy as np

# if production env is windows
if platform.system()=='Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def main():
    key = '2hdnkdq67h54ubdonpf7qcb82lkat17v47ip3t9s94il0jlvcmetrl0m25mralp1'
    api = await keepa.AsyncKeepa().create(key)
    return await api.query('B08862CM7Z',stats=90)
response = asyncio.run(main())

print(response[0]['data'])

# print(f"title of the product -> {response[0]}")
# arr = np.array(response[0]['data']['NEW'])
# print(f"price history of the product -> {response[0]['csv']}")
# print(f"Amazon price history -> {response[0]['csv'][0]}")


# Webhook_test_url -> https://webhook.site/941233ef-72c0-4741-9d68-88c695bdce07



