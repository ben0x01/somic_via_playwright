import asyncio
import json
import re  # Для использования регулярных выражений
from curl_cffi.requests import AsyncSession

from constants import (
    DIAMONDS_CONTRACT,
    CORAL_CONTRACT,
    OBSIDIAN_CONTRACT,
    MALACHITE_CONTRACT,
    ONYX_CONTRACT,
    TOPAZ_CONTRACT,
    OPAL_CONTRACT,
    RUBY_CONTRACT,
)

OUTPUT_FILE = "token_balances.txt"


async def get_token_info(contract_address, wallet_address, session, url, headers):
    payload_symbol = {
        "method": "eth_call",
        "params": [
            {
                "to": contract_address,
                "data": "0x95d89b41"  # ERC-20 function signature for `symbol()`
            },
            "latest",
        ],
        "id": 1,
        "jsonrpc": "2.0",
    }

    payload_decimals = {
        "method": "eth_call",
        "params": [
            {
                "to": contract_address,
                "data": "0x313ce567"  # ERC-20 function signature for `decimals()`
            },
            "latest",
        ],
        "id": 2,
        "jsonrpc": "2.0",
    }

    payload_balance = {
        "method": "eth_call",
        "params": [
            {
                "to": contract_address,
                "data": "0x70a08231000000000000000000000000" + wallet_address[2:]  # ERC-20 `balanceOf()`
            },
            "latest",
        ],
        "id": 3,
        "jsonrpc": "2.0",
    }

    try:
        symbol_resp = await session.post(url, headers=headers, data=json.dumps(payload_symbol))
        decimals_resp = await session.post(url, headers=headers, data=json.dumps(payload_decimals))
        balance_resp = await session.post(url, headers=headers, data=json.dumps(payload_balance))

        if symbol_resp.status_code == 200 and decimals_resp.status_code == 200 and balance_resp.status_code == 200:
            # Удаляем неалфавитные символы в начале строки
            raw_symbol = bytes.fromhex(symbol_resp.json().get("result", "0x")[2:])
            symbol = raw_symbol.decode("utf-8").replace("\x00", "").strip()
            # Используем регулярное выражение для удаления управляющих символов
            symbol = re.sub(r'^\W+', '', symbol)

            decimals = int(decimals_resp.json().get("result", "0x0"), 16)
            balance_wei = int(balance_resp.json().get("result", "0x0"), 16)
            balance_token = balance_wei / (10 ** decimals)

            return {"symbol": symbol, "balance": balance_token}

    except Exception as e:
        print(f"Ошибка при получении данных токена {contract_address}: {str(e)}")

    return None


async def get_random_balance(contract_list, wallet_address):
    url = "https://rpc.testnet.soniclabs.com/"
    headers = {
        "accept": "*/*",
        "content-type": "application/json",
    }

    token_balances = []
    print(f"Запрашиваем балансы для {wallet_address}")

    async with AsyncSession() as session:
        for contract_address in contract_list:
            print(f"Запрашиваем данные для контракта: {contract_address}")
            token_info = await get_token_info(contract_address, wallet_address, session, url, headers)
            print("token_info", token_info)

            if token_info and token_info["balance"] > 0:
                token_balances.append({
                    "contract": contract_address,
                    "symbol": token_info["symbol"],
                    "balance": token_info["balance"]
                })
                print(f"Токен: {token_info['symbol']}, Баланс: {token_info['balance']}")
            else:
                print(f"Контракт {contract_address} не имеет баланса или не поддерживает ERC-20.")

    if token_balances:
        print(f"Найдено {len(token_balances)} токенов с ненулевым балансом")

        return token_balances
    else:
        print("Ненулевых балансов не найдено")
        return None


if __name__ == "__main__":
    contract_list = [
        DIAMONDS_CONTRACT,
        CORAL_CONTRACT,
        OBSIDIAN_CONTRACT,
        MALACHITE_CONTRACT,
        ONYX_CONTRACT,
        TOPAZ_CONTRACT,
        OPAL_CONTRACT,
        RUBY_CONTRACT,
    ]
    wallet_address = "0xD09e83f426edfCA98cf640eBa94380A57b19aD16"

    asyncio.run(get_random_balance(contract_list, wallet_address))
