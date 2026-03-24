from database.db import get_connection
import json


def save_search(user_id, amount, risk_rate, expected_return, portfolio_json):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO search_history
        (user_id, amount, risk_rate, expected_return, portfolio_json)
        VALUES (%s,%s,%s,%s,%s)
    """,
        (user_id, amount, risk_rate, expected_return, portfolio_json),
    )

    conn.commit()
    cur.close()
    conn.close()


def get_search_history(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, amount, risk_rate, expected_return, portfolio_json
        FROM search_history
        WHERE user_id = %s
        ORDER BY id DESC
    """,
        (user_id,),
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()

    def parse_portfolio_json(value):
        if value is None:
            return []
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

    history = []
    for row in rows:
        history.append(
            {
                "id": row[0],
                "amount": float(row[1]) if row[1] is not None else None,
                "risk_rate": float(row[2]) if row[2] is not None else None,
                "expected_return": float(row[3]) if row[3] is not None else None,
                "portfolio": parse_portfolio_json(row[4]),
            }
        )

    return history