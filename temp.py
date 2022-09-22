import json

import requests

annual_provisions = 'https://api.bitsong.interbloc.org/cosmos/mint/v1beta1/annual_provisions'
supply = 'https://api.bitsong.interbloc.org/cosmos/bank/v1beta1/supply'

resp = requests.get(url='https://api.bitsong.interbloc.org/cosmos/bank/v1beta1/supply')
cleaner = json.loads(resp.text)
total_supply = 0

for item in cleaner['supply']:
    # breakpoint()
    if 'ubtsg' in item['denom']:
        total_supply = int(item['amount']) + total_supply

print(total_supply/1000000)