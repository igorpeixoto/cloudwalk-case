import csv
import datetime
import random

# List of issuers and their scores
issuer_scores = {
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
    'banQi': 6,
    'Banco Cetelem': 6
}

# Valid credit card numbers
valid_credit_cards = [
    '4111111111111111',
    '5500000000000004',
    '340000000000009',
    '30000000000004',
    '3088000000000009',
    '6011000000000004',
    '3528000000000007',
    '3530111333300000',
    '5019717010103742',
    '6759649826438453'
]

def generate_fake_transaction():
    # Generate a random transaction
    transaction = {}

    # Randomly select an issuer
    issuer = random.choice(list(issuer_scores.keys()))
    transaction['issuer'] = issuer

    # Calculate the issuer score
    issuer_score = issuer_scores[issuer]
    transaction['score'] = issuer_score

    # Generate a random credit card number
    credit_card_number = generate_credit_card_number()
    transaction['credit_card'] = credit_card_number

    # Check if the credit card number is valid
    if credit_card_number in valid_credit_cards:
        # Generate a random transaction amount
        amount = round(random.uniform(0.01, 20000), 2)
        transaction['amount'] = amount

        # Calculate the time score multiplier
        transaction_time = generate_random_transaction_time()
        transaction['time'] = transaction_time.strftime('%H:%M')
        time_score_multiplier = calculate_time_score_multiplier(transaction_time)

        # Calculate the amount score multiplier
        amount_score_multiplier = calculate_amount_score_multiplier(amount)

        # Calculate the transaction score
        transaction_score = issuer_score * time_score_multiplier * amount_score_multiplier
        transaction['total_score'] = transaction_score

        # Determine the status of the transaction
        if transaction_score > 20:
            transaction['status'] = 'reversed'
        elif issuer_score > 5:
            transaction['status'] = 'denied'
        else:
            transaction['status'] = 'approved'
    else:
        # Invalid credit card number
        transaction['status'] = 'failed'

    return transaction

def generate_credit_card_number():
    # Generate a random credit card number
    credit_card_number = random.choice(valid_credit_cards + ['1234567890123456'])
    return credit_card_number

def generate_random_transaction_time():
    # Generate a random transaction time within the 24-hour period
    transaction_time = datetime.datetime.strptime('2023-01-01', '%Y-%m-%d') + datetime.timedelta(
        minutes=random.randint(0, 23 * 60 + 59))
    return transaction_time

def calculate_time_score_multiplier(transaction_time):
    # Calculate the time score multiplier based on transaction time
    hour = transaction_time.hour

    if 9 <= hour <= 21:
        return 1
    else:
        return 2

def calculate_amount_score_multiplier(amount):
    # Calculate the amount score multiplier based on transaction amount
    if 0.01 <= amount <= 2000:
        return 1
    elif 2000.01 <= amount <= 5000:
        return 2
    elif 5000.01 <= amount <= 10000:
        return 3
    else:
        return 5

def generate_fake_transactions(num_transactions):
    # Generate the specified number of fake transactions
    transactions = []
    for _ in range(num_transactions):
        transaction = generate_fake_transaction()
        transactions.append(transaction)
    return transactions

def generate_fake_transactions_with_spikes(num_transactions, spike_prob):
    # Generate fake transactions with random spikes
    transactions = []
    for i in range(num_transactions):
        transaction = generate_fake_transaction()
        transactions.append(transaction)

        # Check for spikes based on probability
        if random.random() <= spike_prob:
            # Add a spike transaction
            spike_transaction = generate_fake_transaction()
            transactions.append(spike_transaction)

    return transactions

def write_transactions_to_csv(transactions, filename):
    # Write transactions to a CSV file
    with open(filename, mode='w', newline='') as file:
        fieldnames = ['issuer', 'score', 'credit_card', 'amount', 'time', 'total_score', 'status']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(transactions)

# Generate 24000 fake transactions covering a 24-hour period with an average of 20 transactions per minute
num_transactions = 24000
spike_probability = 0.08
transactions = generate_fake_transactions_with_spikes(num_transactions, spike_probability)

# Write transactions to a CSV file
write_transactions_to_csv(transactions, 'test_data.csv')
print('test data generated successfully')