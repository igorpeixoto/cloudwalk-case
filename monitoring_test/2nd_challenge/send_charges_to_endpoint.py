import csv
import datetime
import requests
import time

def send_transaction_to_endpoint(issuer, credit_card, amount):
    data = {
        'issuer': issuer,
        'credit_card_number': credit_card,
        'amount': amount
    }
    response = requests.post('http://localhost:5000/transactions', json=data)
    print(response.text)

def read_transactions_from_csv(filename):
    transactions = []

    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            transactions.append(row)

    return transactions

def filter_transactions_by_current_time(transactions):
    current_time = datetime.datetime.now().strftime('%H:%M')
    filtered_transactions = []

    for transaction in transactions:
        if transaction['time'] == current_time:
            filtered_transactions.append(transaction)

    return filtered_transactions

# Path to the csv table
filename = 'test_data.csv'

while True:
    transactions = read_transactions_from_csv(filename)
    # Filter transactions based on the current hour and minute
    filtered_transactions = filter_transactions_by_current_time(transactions)

    # Send filtered transactions to the endpoint
    for transaction in filtered_transactions:
        issuer = transaction['issuer']
        credit_card = transaction['credit_card']
        amount = transaction['amount']
        send_transaction_to_endpoint(issuer, credit_card, amount)

    time.sleep(60)