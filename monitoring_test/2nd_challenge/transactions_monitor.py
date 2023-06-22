import sqlite3
import threading
import time as t
import datetime
import email_alert

summary = []

def fetch_transactions_summary():
    conn = sqlite3.connect('cc_transactions.db')
    c = conn.cursor()

    # Summarize transactions by time and status
    query = '''
        SELECT strftime('%H:%M', time) AS time_hour_minute, status, COUNT(*) AS count
        FROM transactions
        GROUP BY time_hour_minute, status
    '''
    c.execute(query)
    rows = c.fetchall()

    summary = []
    for row in rows:
        time_hour_minute, status, count = row
        summary.append({
            'time_hour_minute': time_hour_minute,
            'status': status,
            'count': count
        })

    conn.close()
    return summary

def update_summary():
    global summary
    summary = fetch_transactions_summary()
    last_transaction_id = 0  # Keep track of the last processed transaction ID
    while True:
        conn = sqlite3.connect('cc_transactions.db')
        c = conn.cursor()

        query = f'SELECT id, time, status FROM transactions WHERE id > {last_transaction_id}'
        c.execute(query)
        rows = c.fetchall()
        conn.close()

        if rows:
            last_transaction_id = rows[-1][0]

        if rows:
            conn = sqlite3.connect('cc_transactions.db')
            c = conn.cursor()

            for row in rows:
                transaction_id, time_str, status = row
                time = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
                time_hour_minute = time.strftime('%H:%M')

                query = f'''
                    SELECT COUNT(*) FROM transactions_summary
                    WHERE time = ? AND status = ?
                '''
                c.execute(query, (time_hour_minute, status))
                count = c.fetchone()[0]

                if count > 0:
                    query = f'''
                        UPDATE transactions_summary
                        SET count = count + 1
                        WHERE time = ? AND status = ?
                    '''
                    c.execute(query, (time_hour_minute, status))
                else:
                    query = f'''
                        INSERT INTO transactions_summary (time, status, count, full_date)
                        VALUES (?, ?, 1, ?)
                    '''
                    c.execute(query, (time_hour_minute, status, time_str))

            conn.commit()
            conn.close()

        summary = fetch_transactions_summary()

        # Check if the ratio of denied, reversed, or failed transactions exceeds the normal percentages
        check_alert_threshold(summary)

        t.sleep(60)

def check_alert_threshold(summary):
    total_transactions = len(summary)
    denied_count = summary.count("denied")
    reversed_count = summary.count("reversed")
    failed_count = summary.count("failed")

    denied_ratio = (denied_count / total_transactions) * 100
    reversed_ratio = (reversed_count / total_transactions) * 100
    failed_ratio = (failed_count / total_transactions) * 100

    if denied_ratio > 3.0:
        alert_message = "High ratio of denied transactions!"
        email_alert.send_email_alert(alert_message)
        record_alert(datetime.datetime.now(), "denied", alert_message)
        print(alert_message)

    if reversed_ratio > 2.0:
        alert_message = "High ratio of reversed transactions!"
        email_alert.send_email_alert(alert_message)
        record_alert(datetime.datetime.now(), "reversed", alert_message)
        print(alert_message)

    if failed_ratio > 4.0:
        alert_message = "High ratio of failed transactions!"
        email_alert.send_email_alert(alert_message)
        record_alert(datetime.datetime.now(), "failed", alert_message)
        print(alert_message)

def record_alert(date, status, alert_message):
    conn = sqlite3.connect('cc_transactions.db')
    c = conn.cursor()

    query = '''
        INSERT INTO transactions_alerts (date, status, alert_message)
        VALUES (?, ?, ?)
    '''
    c.execute(query, (date, status, alert_message))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    # Separate thread to update the transactions summary
    update_thread = threading.Thread(target=update_summary)
    update_thread.start()

    while True:
        t.sleep(1)
