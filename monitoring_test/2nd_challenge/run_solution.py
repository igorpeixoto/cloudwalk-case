import multiprocessing
import subprocess

def run_transactions_monitor():
    subprocess.run(['python', 'transactions_monitor.py'])

def run_flask_app_transactions_endpoint():
    subprocess.run(['python', 'transactions_endpoint.py'])

def run_send_charges_to_endpoint():
    subprocess.run(['python', 'send_charges_to_endpoint.py'])

if __name__ == '__main__':
    transactions_monitor_process = multiprocessing.Process(target=run_transactions_monitor)
    transactions_endpoint_process = multiprocessing.Process(target=run_flask_app_transactions_endpoint)
    transactions_charge_process = multiprocessing.Process(target=run_send_charges_to_endpoint)

    transactions_monitor_process.start()
    transactions_endpoint_process.start()
    transactions_charge_process.start()

    transactions_monitor_process.join()
    transactions_endpoint_process.join()
    transactions_charge_process.join()
