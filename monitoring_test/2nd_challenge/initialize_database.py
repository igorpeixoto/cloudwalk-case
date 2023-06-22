import sqlite3

# Path to the SQLite database file
database_file = 'cc_transactions.db'

def create_database():
    conn = sqlite3.connect(database_file)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            time TEXT,
            amount REAL,
            issuer TEXT,
            score INTEGER,
            status TEXT
        );
    '''
    )

    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions_summary (
            id INTEGER PRIMARY KEY,
            full_date TEXT,
            time TEXT,
            status TEXT,
            count INTEGER
        );
    '''
    )

    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions_alerts (
            id INTEGER PRIMARY KEY,
            date TEXT,
            status TEXT,
            alert_message INTEGER
        );
    '''
    )

    conn.commit()
    conn.close()
    
if __name__ == '__main__':
    create_database()
