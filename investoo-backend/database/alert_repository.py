from database.db import get_connection


def create_alert(user_id, portfolio_id, message):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO alerts (user_id, portfolio_id, message)
        VALUES (%s,%s,%s)
    """, (user_id, portfolio_id, message))

    conn.commit()

    cur.close()
    conn.close()


def get_user_alerts(user_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT message, created_at
        FROM alerts
        WHERE user_id=%s
        ORDER BY created_at DESC
    """, (user_id,))

    alerts = cur.fetchall()

    cur.close()
    conn.close()

    return alerts