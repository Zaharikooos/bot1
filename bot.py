import os
import time
import asyncio
from binance.client import Client
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

# Получение API-ключей из переменных окружения
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")

PHANTOM_WALLETS = {
    'Кошелек 1': 'F2oeLzGqZYrxzhb1YS6NAc26cuBeSZH1iuzk2tRzEVox',
    'Кошелек 2': '6wwTuDFFjmyP6fULn7o3dUh5ok5tyS7u32TzGg9uZjzy',
    'Кошелек 3': 'FCPnSAYHWUS6ELhhyMX1jUDwrwkP7458C5NKm5w5r1JL',
    'Кошелек 4': '6MUPvKWkh1q12E3wi2kMW7yZ1NGVBr6ZSeZMmqQAifQL',
    'Кошелек 5': '2FK57s2TRj1JoU6cYSe48bkcFWpZKdRJZ4YchbEVcg8G',
    'Кошелек 6': '9EHuPhyq5y3zHAwfUbL9uoXYbdhZgwKuiTVcuyWcY4Zm',
    'Кошелек 7': 'BPFKQLoccCLr58DCnwzz696RKAQFfARe4zjU277GeaF9',
    'Кошелек 8': 'BSLpsU5214Syu6TEXB4RMkrHpxBwfx5gohiNdr3Q632V',
    'Кошелек 9': 'PR4biZ5PkoUrFtpTUGrGzXcKz42NqYWsr1qJsETM1AA',
    'Кошелек 10': 'F8SANXD2kgUXVG8cJ9y3X27MzQhvCQsbuwBJ3urCG2t4'
}

client = Client(API_KEY, API_SECRET)
bot = Bot(token=TG_BOT_TOKEN)
dp = Dispatcher()

def withdraw_bmt(wallets):
    asset = 'BMT'
    network = 'SOL'
    amount = 1
    
    for address in wallets.values():
        try:
            client.withdraw(coin=asset, address=address, amount=amount, network=network)
            time.sleep(2)
        except Exception as e:
            print(f"Ошибка вывода на {address}: {e}")

def withdraw_single(wallet_name):
    asset = 'BMT'
    network = 'SOL'
    amount = 1
    address = PHANTOM_WALLETS[wallet_name]
    
    try:
        client.withdraw(coin=asset, address=address, amount=amount, network=network)
    except Exception as e:
        print(f"Ошибка вывода на {address}: {e}")

@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Вывести на все кошельки", callback_data="withdraw_all")],
        [InlineKeyboardButton(text="Выбрать кошелек", callback_data="choose_wallet")]
    ])
    await message.answer("Выберите действие:", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data == "withdraw_all")
async def process_withdraw(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id, "Начинаю вывод на все кошельки...")
    withdraw_bmt(PHANTOM_WALLETS)
    await bot.send_message(callback_query.from_user.id, "Вывод завершен!")

@dp.callback_query(lambda c: c.data == "choose_wallet")
async def choose_wallet(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=wallet, callback_data=f"wallet_{wallet}")]
        for wallet in PHANTOM_WALLETS.keys()
    ])
    await bot.send_message(callback_query.from_user.id, "Выберите кошелек:", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data.startswith("wallet_"))
async def process_single_withdraw(callback_query: types.CallbackQuery):
    wallet_name = callback_query.data.replace("wallet_", "")
    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id, f"Начинаю вывод на {wallet_name}...")
    withdraw_single(wallet_name)
    await bot.send_message(callback_query.from_user.id, "Вывод завершен!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
