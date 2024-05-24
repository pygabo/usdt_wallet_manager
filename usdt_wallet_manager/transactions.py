import os
import requests
import argparse
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv()


def get_usdt_transactions(wallet_address, api_key):
    url = "https://api.etherscan.io/api"
    params = {
        "module": "account",
        "action": "tokentx",
        "contractaddress": "0xdac17f958d2ee523a2206206994597c13d831ec7",  # USDT contract address
        "address": wallet_address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": api_key
    }
    response = requests.get(url, params=params)
    return response.json()


def calculate_balance(transactions, wallet_address):
    total_in = 0
    total_out = 0
    transaction_details = []

    for tx in transactions["result"]:
        if isinstance(tx, dict):  # Ensure tx is a dictionary
            try:
                value = int(tx["value"]) / 10 ** 6  # USDT has 6 decimal places
                if tx["to"].lower() == wallet_address.lower():
                    total_in += value
                    transaction_details.append(["+", format_number(value), tx['from'], tx['hash']])
                if tx["from"].lower() == wallet_address.lower():
                    total_out += value
                    transaction_details.append(["-", format_number(value), tx['to'], tx['hash']])
            except KeyError as e:
                print(f"KeyError: {e} in transaction {tx}")
            except ValueError as e:
                print(f"ValueError: {e} in transaction {tx}")
        else:
            print(f"Unexpected transaction format: {tx}")

    return total_in, total_out, transaction_details


def format_number(value):
    return "{:,.2f}".format(value)


def main():
    parser = argparse.ArgumentParser(description="USDT Wallet Manager")
    parser.add_argument('--wallet', default=os.environ.get('WALLET_ADDRESS'), help="Wallet address")
    parser.add_argument('--api_key', default=os.environ.get('API_KEY'), help="Etherscan API key")
    args = parser.parse_args()

    if not args.wallet or not args.api_key:
        print(
            "Please set the WALLET_ADDRESS and API_KEY environment variables or provide them as command-line arguments.")
        return

    transactions = get_usdt_transactions(args.wallet, args.api_key)
    total_in, total_out, transaction_details = calculate_balance(transactions, args.wallet)

    print("\nTransaction Details:")
    print(tabulate(transaction_details, headers=["Type", "Amount (USDT)", "Counterparty", "Transaction Hash"],
                   tablefmt="pretty"))

    print("\nSummary:")
    print(f"Total USDT received: {format_number(total_in)}")
    print(f"Total USDT sent: {format_number(total_out)}")
    print(f"Net balance: {format_number(total_in - total_out)}")


if __name__ == "__main__":
    main()
