import requests
import json
import mysql.connector  # pip install mysql-connector-python

from pycoingecko import CoinGeckoAPI


abci_info_url = 'https://bitsong-archive.validatrium.club/abci_info'
validators_list_url = 'https://api.bitsong.interbloc.org/cosmos/staking/v1beta1/validators'


def get_price():
    cg = CoinGeckoAPI('')
    bitsong_price = cg.get_price(ids='bitsong', vs_currencies='usd')
    price = bitsong_price['bitsong']['usd']
    return price


def get_height():
    try:
        response = requests.get(abci_info_url, timeout=5)
        response.raise_for_status()
        clean_data = json.loads(response.text)
        height = clean_data['result']['response']['last_block_height']
        print(f'Current height is {height}')

    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)

    return height


def get_validators_list():
    try:
        response = requests.get(validators_list_url, timeout=5)
        response.raise_for_status()
        clean_data = json.loads(response.text)

        for validator in clean_data['validators']:

            valoper = validator['operator_address']

            jailed = validator['jailed']
            tokens = validator['tokens']
            delegator_shares = validator['delegator_shares']

            moniker = validator['description']['moniker']
            website = validator['description']['website']

            commission = validator['commission']['commission_rates']['rate']

            validators_data = {
                'valoper': valoper,
                'jailed': jailed,
                'tokens': tokens,
                'moniker': moniker,
                'website': website,
                'commission': commission,
            }

            print(f'{validators_data}')

            return validators_data

    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)


def add_to_database():

    height = get_height()
    price = get_price()
    validators_list = get_validators_list()
    breakpoint()

    try:
        connection = mysql.connector.connect(host='hugoboqu.beget.tech',
                                             database='hugoboqu_bitsong	',
                                             user='hugoboqu_bitsong	',
                                             password='UY8wd*Yr')

        mysql_insert_height_price = """INSERT INTO general_info (Height, Price)
                               VALUES
                               (%s, %s) """
        mysql_insert_validators = """INSERT INTO validators (valoper, moniker, jailed, tokens, website, commission)
                               VALUES
                               (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE \
                                valoper = VALUES(valoper), \
                                moniker = VALUES(moniker), \
                                jailed = VALUES(jailed), \
                                commission = VALUES(commission), \
                                tokens = VALUES(tokens), \
                                website = VALUES(website)                                                      
                                 """
        record_1 = (height, price)
        record_2 = (validators_list['valoper'], validators_list['moniker'], validators_list['jailed'],
                    validators_list['tokens'], validators_list['website'], validators_list['commission'])
        cursor = connection.cursor()
        cursor.execute(mysql_insert_height_price, record_1)
        cursor.execute(mysql_insert_validators, record_2)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into Laptop table")
        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into table {}".format(error))

    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")


if __name__ == '__main__':
    # get_price_height()
    # get_validators_list()
    add_to_database()
