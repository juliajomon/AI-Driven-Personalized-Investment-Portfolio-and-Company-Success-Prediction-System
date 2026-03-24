from database.db import get_connection
import json


def save_portfolio(user_id, amount, risk_rate, expected_return, portfolio_json):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO saved_portfolios
        (user_id, amount, risk_rate, expected_return, portfolio_json)
        VALUES (%s, %s, %s, %s, %s)

        ON CONFLICT (user_id)
        DO UPDATE SET
            amount = EXCLUDED.amount,
            risk_rate = EXCLUDED.risk_rate,
            expected_return = EXCLUDED.expected_return,
            portfolio_json = EXCLUDED.portfolio_json,
            last_checked = NOW()

        RETURNING id
    """, (user_id, amount, risk_rate, expected_return, portfolio_json))

    portfolio_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return portfolio_id


def get_saved_portfolios(user_id: int):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, user_id, amount, risk_rate, expected_return, portfolio_json
        FROM saved_portfolios
        WHERE user_id = %s
        ORDER BY id DESC
    """, (user_id,))

    rows = cur.fetchall()

    portfolios = []

    def parse_portfolio_json(value):
        if value is None:
            return []
        # JSONB may already be decoded by the driver
        if isinstance(value, (list, dict)):
            return value
        if isinstance(value, (bytes, bytearray)):
            value = value.decode("utf-8", errors="ignore")
        if isinstance(value, str):
            try:
                return json.loads(value)
            except Exception:
                return []
        return []

    for row in rows:
        portfolios.append({
            "id": row[0],
            "user_id": row[1],
            "amount": row[2],
            "risk_rate": row[3],
            "expected_return": row[4],
            "portfolio": parse_portfolio_json(row[5])
        })

    cur.close()
    conn.close()

    return portfolios 