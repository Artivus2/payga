from tronpy import Tron
from tronpy.keys import PrivateKey

BASE_URL = 'http://localhost:8080'
REG_URL = 'https://test.greenavi.com'
API_KEY_EXPIRATION_PERIOD = '1 year'
date_format_all = "'%d/%m/%Y %H:%i'"
config = {
            'user': 'greenavi_user',
            'password': 'tb7x3Er5PQ',
            'host': 'localhost',
            'database': 'greenavi_app',
            'raise_on_warnings': True
        }
SECRET_KEY ="_5x99maBZNQ6du_A4l6Hx2WPAW8-EAp6"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRES_MINUTES = 15 * 24 * 60  # 15 days
TIME_ORDER_PAYIN_EXPIRY = 15
TIME_ORDER_PAYOUT_EXPIRY = 240
api_key_np = '2WMC682-ATF4WCE-NW0HZNC-5E7S427'  # the key that sasha gave
BSC_API_KEY = 'UDFA4KE6NC32K49T8BXI33JFEUM5NUUU3V'
base_url_np = 'https://api.nowpayments.io/v1/'
email = 'test.greenavi@mail.ru'
password = 'M354at790!'
telegram_api = "7687672183:AAF1hgHQDO6q6uoKdiz_0Aj7qccSd-00gNU"
pay_group_test = '-1001896452673'
pay_main_group = '-1002457991085'
string="https://api.telegram.org/bot7687672183:botAAF1hgHQDO6q6uoKdiz_0Aj7qccSd-00gNU/getUpdates"
admin_wallet = "TNYxgm5EkxvDPGBJGuY7TJ41omJhJv1CJD"
private_key = 'b70f4b1c86944dcef14a9c52ceab7c84edddfea640e24fb13588d70246572cb1'
public_key = '40a135a3d17d66e07e7d814f83e001f702a1eb5aeeaa3b7534aca1401f3ce73064b0043cd694af35cc2cf6dd1dd9e47898c68c2fbea0bc88d40d1dad87983791'
hex_address = '418a03b3bf5afe0e94b014be2e3929e11150dc601f'
USDT_CONTRACT_ADDRESS = 'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t'
BYBIT_ADDRESS = "TM6hy595DEm9NSzEJ1dLq7ogGeM1Kv4bQA"
SUPER_ADMIN_ADDRESS = 'support@greenavi.com'
HOST_EMAIL = "mail.hosting.reg.ru"


# client = Tron()
#
# # Define your private key
# priv_key = PrivateKey(bytes.fromhex(private_key))
#
# # Define the recipient address and token amount
# recipient_address = BYBIT_ADDRESS
# token_amount = 1 # Specify the amount of USDT TRC20 tokens to send
#
# # Send the tokens
#
# #priv_key = PrivateKey.fromhex(private_key)
# result = client.trx.transfer(admin_wallet, recipient_address, 1).fee_limit(3000000).build().sign(priv_key).broadcast().wait()
#
# # Print transaction result
# print("Transaction ID:", result["transaction"]["txID"])