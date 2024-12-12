from fastapi import APIRouter

import config
import routers.withdraws.models as withdraws_models
from pprint import pprint
from tronpy.exceptions import AddressNotFound
from tronpy import Tron





router = APIRouter(prefix='/api/v1/withdraws', tags=['Вывод средств'])


@router.post("/check-balance")
async def get_stats(request: withdraws_models.Withdraws):
    pass


@router.post("/check-deposit")
async def get_stats(request: withdraws_models.Withdraws):
    pass


@router.post("/balance-out")
async def get_stats(request: withdraws_models.Withdraws):
    pass

@router.post(("/generate-wallet-tron"))
async def get_wallet_tron(request: withdraws_models.Withdraws):
    client = Tron()
    # {'base58check_address': 'TNYxgm5EkxvDPGBJGuY7TJ41omJhJv1CJD',
    #  'hex_address': '418a03b3bf5afe0e94b014be2e3929e11150dc601f',
    #  'private_key': 'b70f4b1c86944dcef14a9c52ceab7c84edddfea640e24fb13588d70246572cb1',
    #  'public_key': '40a135a3d17d66e07e7d814f83e001f702a1eb5aeeaa3b7534aca1401f3ce73064b0043cd694af35cc2cf6dd1dd9e47898c68c2fbea0bc88d40d1dad87983791'}
    pprint(client.generate_address())
    try:
        balance = client.get_account_balance('TNYxgm5EkxvDPGBJGuY7TJ41omJhJv1CJD')

    except AddressNotFound:
        print( "Adress not found..!" )

    print(balance)


@router.post(("/send-to-trx"))
async def get_wallet_tron(request: withdraws_models.Withdraws):
    # Создаем клиент Tron
    client = Tron()

    # Ваши учетные данные из бд админа адрес
    # private_key = 'YOUR_PRIVATE_KEY'
    # from_address = 'YOUR_ADDRESS'
    # to_address = 'RECIPIENT_ADDRESS'
    # amount = 100  # количество USDT для отправки

    # Отправка USDT
    # tx = client.trx.transfer(to_address, amount).build().sign(private_key)
    # result = tx.broadcast()
    # print(result)
    #save transaction to db