import requests
import json
import mysql.connector


def get_validators_list():

    validators_list_url = 'https://api.bitsong.interbloc.org/cosmos/staking/v1beta1/validators'
    all_validators_data = {}
    all_validators_list = []
    count = 1
    try:
        response = requests.get(validators_list_url, timeout=5)
        response.raise_for_status()
        clean_data = json.loads(response.text)
        for validator in clean_data['validators']:

            all_validators_list.append(validator['operator_address'])

        print(f'{all_validators_list}')

        return all_validators_list

    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)


def get_validator_delegators(validator_valoper):
    delegator_url = f'https://api.bitsong.interbloc.org/cosmos/staking/v1beta1/validators/{validator_valoper}/delegations'
    delegator_list = list()
    try:
        response = requests.get(delegator_url, timeout=5)
        response.raise_for_status()
        clean_data = json.loads(response.text)
        for delegator in clean_data['delegation_responses']:
            delegator_address = delegator['delegation']['delegator_address']
            delegator_list.append(delegator_address)

        return delegator_list

    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)


def add_to_database(address, validator_id):

    try:
        connection = mysql.connector.connect(host='hugoboqu.beget.tech',
                                             database='hugoboqu_bitsong	',
                                             user='hugoboqu_bitsong	',
                                             password='UY8wd*Yr')

        mysql_insert_delegators = """INSERT INTO delegators (address, validator_id)
                               VALUES
                               (%s, %s) ON DUPLICATE KEY UPDATE \
                                address = VALUES(address), \
                                validator_id = VALUES(validator_id)                                                    
                                """
        # record_1 = (height, price)
        record_1 = (address, validator_id)

        cursor = connection.cursor()
        cursor.execute(mysql_insert_delegators, record_1)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into delegators table")
        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into table {}".format(error))

    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")


if __name__ == '__main__':
    add_to_database('bitsong1f4z9xvfswjyss32d26z8v3ak5f97t74znsyn8k', 68)




# delegator = 'bitsong1n4akqrmpd29stwvh6dklzecplfha2asdtce9nn'
# validator = "bitsongvaloper1f4z9xvfswjyss32d26z8v3ak5f97t74zj5c6ht"
# api_url = f"https://api.bitsong.interbloc.org/cosmos/tx/v1beta1/txs?events=message.sender='{delegator}'&events=delegate.validator='{validator}'"
#
#
# response = requests.get(api_url)
#
# clean_data = json.loads(response.text)
#
# timestamp = clean_data['tx_responses'][0]['timestamp']
#
# print(timestamp)

# первоначальная задача найти всех делегаторов у каждого валидатора и добавить в связанную таблицу,
# а уже потом добавить им данные о количестве делегаций и датах делегаций