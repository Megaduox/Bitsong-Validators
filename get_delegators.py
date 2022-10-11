import requests
import json
import mysql.connector


config = {
    'host': 'hugoboqu.beget.tech',
    'database': 'hugoboqu_bitsong',
    'user': 'hugoboqu_bitsong',
    'password': 'UY8wd*Yr',
}


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


def add_to_database_one(address, validator_id):

    try:
        connection = mysql.connector.connect(**config)

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


def get_mysql_id_by_valoper(valoper):

    try:
        connection = mysql.connector.connect(**config)

        mysql_select_id = """SELECT * from validators WHERE valoper = %s"""
        cursor = connection.cursor()
        cursor.execute(mysql_select_id, (valoper,))
        record = cursor.fetchall()

        for row in record:
            print(f'Id for {valoper} is {row[7]}')
            validator_id = row[7]

        return validator_id

    except mysql.connector.Error as error:
        print("Failed to get record from MySQL table: {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def get_validators_delegators():

    all_validators = get_validators_list()
    validators_delegators = list()
    count = 1

    for validator in all_validators:

        validator_id = get_mysql_id_by_valoper(validator)

        if count < 200:  # temporary condition
            all_delegators_for_validator = get_validator_delegators(validator)
            for delegator in all_delegators_for_validator:
                validators_delegators.append((validator_id, delegator))
            count += 1
        else:
            break

    return validators_delegators


def add_to_database_many(record):

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
        mysql_insert_many_delegators = """INSERT INTO delegators (validator_id, address)
                               VALUES
                               (%s, %s) ON DUPLICATE KEY UPDATE \
                               validator_id = VALUES(validator_id), \
                                address = VALUES(address)                                                                                 
                                """

        cursor = connection.cursor()
        cursor.executemany(mysql_insert_many_delegators, record)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into delegators table")
        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into table {}".format(error))

    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")


def get_time_tokens_for_delegations():

    delegator = 'bitsong1n4akqrmpd29stwvh6dklzecplfha2asdtce9nn'
    validator = "bitsongvaloper1f4z9xvfswjyss32d26z8v3ak5f97t74zj5c6ht"
    api_url = f"https://api.bitsong.interbloc.org/cosmos/tx/v1beta1/txs?events=message.sender='{delegator}'&events=delegate.validator='{validator}'"

    response = requests.get(api_url)

    clean_data = json.loads(response.text)

    timestamp = clean_data['tx_responses'][0]['timestamp']
    amount = int(clean_data['txs'][0]['body']['messages'][0]['amount']['amount'])

    print(timestamp, amount)
    # преобразовать timestamp в дату для экспорта в базу и добавить эту функцию в основную по добавлению в базу


if __name__ == '__main__':
    # add_to_database_many(record=get_validators_delegators())
    # get_validators_delegators()
    # get_mysql_id_by_valoper(valoper='bitsongvaloper100akrazwzrxhklgnh2ueaqfcv7kcanh9ew3jxf')
    get_time_tokens_for_delegations()


