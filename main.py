import requests
import json
import mysql.connector  # pip install mysql-connector-python

from pycoingecko import CoinGeckoAPI


abci_info_url = 'https://bitsong-archive.validatrium.club/abci_info'

cg = CoinGeckoAPI('')
bitsong_price = cg.get_price(ids='bitsong', vs_currencies='usd')
price = bitsong_price['bitsong']['usd']

try:
    response = requests.get(abci_info_url, timeout=5)
    response.raise_for_status()
    clean_data = json.loads(response.text)
    height = clean_data['result']['response']['last_block_height']
    print(f'Current height is {height}')
    print(f'Current price is {price}')

    try:
        connection = mysql.connector.connect(host='hugoboqu.beget.tech',
                                             database='hugoboqu_bitsong	',
                                             user='hugoboqu_bitsong	',
                                             password='UY8wd*Yr')

        mySql_insert_query = """INSERT INTO general_info (Height, Price)
                               VALUES
                               (%s, %s) """
        record = (height,price)
        cursor = connection.cursor()
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into Laptop table")
        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))

    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

except requests.exceptions.HTTPError as errh:
    print(errh)
except requests.exceptions.ConnectionError as errc:
    print(errc)
except requests.exceptions.Timeout as errt:
    print(errt)
except requests.exceptions.RequestException as err:
    print(err)