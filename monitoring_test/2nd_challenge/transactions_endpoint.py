from flask import Flask, request
import sqlite3
from luhn import *
import datetime

app = Flask(__name__)

def is_valid_credit_card(credit_card_number):
    # Remove any non-digit characters from the credit card number
    credit_card_number = ''.join(c for c in credit_card_number if c.isdigit())
    # Validate the credit card number using Luhn's algorithm
    return verify(credit_card_number)

def calculate_time_score_multiplier(transaction_time):
    parsed_time = datetime.datetime.strptime(transaction_time, '%Y-%m-%d %H:%M:%S')
    transaction_hour = parsed_time.hour
    transaction_minute = parsed_time.minute
    # Calculate the score multiplier based on the transaction time
    if (transaction_hour >= 9 and transaction_hour <= 21) or (transaction_hour == 8 and transaction_minute >= 59):
        multiplier = 1
    else:
        multiplier = 2

    return multiplier

def calculate_amount_score_multiplier(transaction_amount):
    # Calculate the multiplier based on the transaction amount
    if transaction_amount >= 0.01 and transaction_amount <= 2000:
        amount_score_multiplier = 1
    elif transaction_amount >= 2000.01 and transaction_amount <= 5000:
        amount_score_multiplier = 2
    elif transaction_amount >= 5000.01 and transaction_amount <= 10000:
        amount_score_multiplier = 3
    else:
        amount_score_multiplier = 5

    return amount_score_multiplier

def get_credit_card_issuer_score(credit_card_issuer):
    credit_card_issuer_score = {
        'Banco do Brasil': 1,
        'CEF': 4,
        'Itaú': 1,
        'Santander': 2,
        'Bradesco': 3,
        'Credicard': 4,
        'BS2': 6,
        'Inter': 5,
        'Nubank': 5,
        'PicPay': 5,
        'BrasilCard': 6,
        'BMG': 1,
        'C6 Bank': 2,
        'Bancoob': 1,
        'BTG Pactual': 3,
        'banQi':6,
        'Banco Cetelem': 6
    }
    return credit_card_issuer_score[credit_card_issuer]

@app.route('/transactions', methods=['POST'])
def process_transaction():
    # Get the transaction data from the request
    request_data = request.get_json()

    credit_card_issuer = request_data.get('issuer')
    transaction_amount = float(request_data.get('amount'))
    credit_card_number = request_data.get('credit_card_number')

    # initial status
    transaction_status = 'approved'
    transaction_score = 0
    credit_card_issuer_score = 0
        
    transaction_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Calculate transaction score
    time_score_multiplier = calculate_time_score_multiplier(transaction_time)
    amount_score_multiplier = calculate_amount_score_multiplier(transaction_amount)
    credit_card_issuer_score = get_credit_card_issuer_score(credit_card_issuer)
    transaction_score = credit_card_issuer_score * time_score_multiplier * amount_score_multiplier

    if not transaction_score <= 20:
        transaction_status = 'reversed'
    if not is_valid_credit_card(credit_card_number):
        transaction_status = 'failed'
    if credit_card_issuer_score > 5:
        transaction_status = 'denied'

    transaction_data = (transaction_time, transaction_amount, credit_card_issuer, transaction_score, transaction_status)

    # Record of the transaction in the database
    create_transaction_record(transaction_data)

    # Return response
    return {'transaction_status': transaction_status}

def create_transaction_record(transaction_data):
    conn = sqlite3.connect('cc_transactions.db')
    cursor = conn.cursor()

    query = '''
    INSERT INTO transactions (time, amount, issuer, score, status)
    VALUES (?,?,?,?,?)
    '''
    cursor.execute(query, (transaction_data))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run()
