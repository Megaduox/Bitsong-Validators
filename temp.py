import json

import requests


def get_time_tokens_for_delegations():


    delegator = 'bitsong18n3vlcthxv5s2s4zgjdrjr5a6lw9e7tmthnwnk'
    validator = 'bitsongvaloper1qxw4fjged2xve8ez7nu779tm8ejw92rv0vcuqr'

    api_url = f"https://api.bitsong.interbloc.org/cosmos/tx/v1beta1/txs?events=message.sender='{delegator}'&events=delegate.validator='{validator}'"

    response = requests.get(api_url)

    clean_data = json.loads(response.text)

    if clean_data['txs'] and 'grantee' not in clean_data['txs'][0]['body']['messages'][0]\
            and 'amount' in clean_data['txs'][0]['body']['messages'][0]:
        timestamp_source = clean_data['tx_responses'][0]['timestamp']
        amount = int(clean_data['txs'][0]['body']['messages'][0]['amount']['amount'])
        print(amount, timestamp_source)

    else:
        pass

if __name__ == '__main__':
    get_time_tokens_for_delegations()

