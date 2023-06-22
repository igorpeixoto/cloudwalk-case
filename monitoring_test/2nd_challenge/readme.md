## 2nd challenge - Implementation of a monitoring with real time alert

The solution is organized in a jupyter notebook ('2nd_challenge_solution.ipynb')
in order to be more easiable to navigate and run the scripts.

The python scripts are:

- initialize_database.py
    
    Creates SQLite database file cc_transactions.db

- generate_test_data.py

    Creates a test_data.csv file with data to test the solution in a controlled
    way.
    
- send_charges_to_endpoint.py

    Send data from test_data.csv to the transactions endpoint.
    
- transactions_endpoint.py

    Receives the transactions requests and evaluate each one in order to
    approve, deny, reverse or fail the transaction, and record each in the 
    database.

- transactions_monitor.py

    Summarizes the transactions recorded in the database, if there is deviation
    from the normal ratio of distribution of transaction status, it sends an
    email alerting the team and register the occurence in the database.
    
- run_solution.py

    To start concurrent python scripts.
    
- email_alert.py

    
Also there is a Power BI file 'transactions_dashboard.pbix'showing the 
transactions in the past 20 minutes.

![Screen capture of the dashboard.](/image/transactions_dashboard.png "Screen capture of the dashboard")
