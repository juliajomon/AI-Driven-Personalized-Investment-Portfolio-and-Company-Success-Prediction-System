from database.db import get_connection

try:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT NOW();")

    result = cur.fetchone()

    print("Database connected successfully")
    print(result)

    cur.close()
    conn.close()

except Exception as e:
    print("Database connection failed")
    print(e)