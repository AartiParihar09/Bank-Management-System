import pickle
import os
import numpy as np
from datetime import datetime


DATA_FILE = "accounts.pkl"

accounts = {}
next_account_number = 1001


# ---------------- SAVE DATA ----------------

def save_data():

    data = {
        "accounts": accounts,
        "next_account_number": next_account_number
    }

    try:
        with open(DATA_FILE, "wb") as file:
            pickle.dump(data, file)

        return True

    except (OSError, pickle.PickleError) as error:
        print(f"Error Saving Data: {error}")
        return False


# ---------------- LOAD DATA ----------------

def load_data():

    global accounts, next_account_number

    if not os.path.exists(DATA_FILE):
        return

    try:
        with open(DATA_FILE, "rb") as file:
            data = pickle.load(file)

        accounts = data["accounts"]
        next_account_number = data["next_account_number"]

    except (
        OSError,
        pickle.PickleError,
        EOFError,
        KeyError
    ) as error:

        print(f"Error Loading Data: {error}")

        accounts = {}
        next_account_number = 1001


# ---------------- OPEN ACCOUNT ----------------

def create_account(name, account_type, balance):

    global next_account_number

    name = name.strip()
    account_type = account_type.strip()

    if not name:
        return False, "Account holder name is required.", None

    if account_type not in ["Saving", "Current"]:
        return False, "Invalid account type.", None

    if balance <= 0:
        return False, "Initial deposit must be positive.", None

    account_number = next_account_number

    opening_transaction = {
        "date": datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        ),
        "type": "Deposit",
        "amount": balance
    }

    accounts[account_number] = {
        "name": name,
        "type": account_type,
        "balance": balance,
        "history": [opening_transaction]
    }

    next_account_number += 1

    save_data()

    return (
        True,
        "Account created successfully.",
        account_number
    )


# ---------------- VIEW ACCOUNT ----------------

def get_account(account_number):

    if account_number not in accounts:
        return False, "Account not found.", None

    account = accounts[account_number]

    return True, "Account found successfully.", account


# ---------------- DEPOSIT ----------------

def deposit(account_number, amount):

    if account_number not in accounts:
        return False, "Account not found."

    if amount <= 0:
        return False, "Deposit amount must be positive."

    account = accounts[account_number]

    account["balance"] += amount

    transaction = {
        "date": datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        ),
        "type": "Deposit",
        "amount": amount
    }

    account["history"].append(transaction)

    save_data()

    return (
        True,
        f"Deposit successful! "
        f"Current Balance: {account['balance']}"
    )


# ---------------- WITHDRAW ----------------

def withdraw(account_number, amount):

    if account_number not in accounts:
        return False, "Account not found."

    if amount <= 0:
        return False, "Withdrawal amount must be positive."

    account = accounts[account_number]

    if amount > account["balance"]:
        return False, "Insufficient balance."

    account["balance"] -= amount

    transaction = {
        "date": datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        ),
        "type": "Withdrawal",
        "amount": amount
    }

    account["history"].append(transaction)

    save_data()

    return (
        True,
        f"Withdrawal successful! "
        f"Current Balance: {account['balance']}"
    )


# ---------------- TRANSFER ----------------

def transfer(sender_number, receiver_number, amount):

    if sender_number not in accounts:
        return False, "Sender account not found."

    if receiver_number not in accounts:
        return False, "Receiver account not found."

    if sender_number == receiver_number:
        return False, "Cannot transfer to the same account."

    if amount <= 0:
        return False, "Transfer amount must be positive."

    sender = accounts[sender_number]
    receiver = accounts[receiver_number]

    if amount > sender["balance"]:
        return False, "Insufficient balance."

    sender["balance"] -= amount
    receiver["balance"] += amount

    transaction_date = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    sender_transaction = {
        "date": transaction_date,
        "type": "Transfer Sent",
        "amount": amount,
        "account": receiver_number
    }

    receiver_transaction = {
        "date": transaction_date,
        "type": "Transfer Received",
        "amount": amount,
        "account": sender_number
    }

    sender["history"].append(sender_transaction)
    receiver["history"].append(receiver_transaction)

    save_data()

    return (
        True,
        f"Transfer successful! "
        f"Sender Balance: {sender['balance']}"
    )


# ---------------- TRANSACTION HISTORY ----------------

def get_transaction_history(account_number):

    if account_number not in accounts:
        return False, "Account not found.", None

    history = accounts[account_number]["history"]

    return (
        True,
        "Transaction history loaded.",
        history
    )


# ---------------- ACCOUNT SUMMARY ----------------

def get_account_summary(account_number):

    if account_number not in accounts:
        return False, "Account not found.", None

    account = accounts[account_number]
    history = account["history"]

    deposit_amounts = [
        transaction["amount"]
        for transaction in history
        if transaction["type"] == "Deposit"
    ]

    withdrawal_amounts = [
        transaction["amount"]
        for transaction in history
        if transaction["type"] == "Withdrawal"
    ]

    all_transaction_amounts = [
        transaction["amount"]
        for transaction in history
    ]

    total_deposits = np.sum(deposit_amounts)

    total_withdrawals = np.sum(
        withdrawal_amounts
    )

    if all_transaction_amounts:

        average_transaction = np.mean(
            all_transaction_amounts
        )

    else:
        average_transaction = 0

    summary = {
        "account_number": account_number,
        "name": account["name"],
        "account_type": account["type"],
        "balance": account["balance"],
        "total_deposits": total_deposits,
        "total_withdrawals": total_withdrawals,
        "average_transaction": average_transaction,
        "total_transactions": len(history)
    }

    return (
        True,
        "Account summary generated.",
        summary
    )


load_data()