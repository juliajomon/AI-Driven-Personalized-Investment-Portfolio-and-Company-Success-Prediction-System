from database.db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash


def _get_users_password_column(cur) -> str:
    """
    Detect the password column name in public.users.
    Supports common schemas: password_hash, password, hashed_password.
    """
    cur.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = 'users'
          AND column_name IN ('password_hash', 'password', 'hashed_password')
        """
    )
    cols = [r[0] for r in cur.fetchall()]
    for preferred in ("password_hash", "hashed_password", "password"):
        if preferred in cols:
            return preferred
    raise Exception("users table is missing a password column (expected password_hash/password/hashed_password)")


def create_user(email: str, password: str) -> int:
    conn = get_connection()
    cur = conn.cursor()

    pw_hash = generate_password_hash(password)
    pw_col = _get_users_password_column(cur)

    cur.execute(
        f"""
        INSERT INTO users (email, {pw_col})
        VALUES (%s, %s)
        RETURNING id
        """,
        (email, pw_hash),
    )
    user_id = cur.fetchone()[0]
    conn.commit()

    cur.close()
    conn.close()
    return user_id


def authenticate_user(email: str, password: str):
    conn = get_connection()
    cur = conn.cursor()

    pw_col = _get_users_password_column(cur)
    cur.execute(
        f"""
        SELECT id, {pw_col}
        FROM users
        WHERE email = %s
        """,
        (email,),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return None

    user_id, pw_hash = row[0], row[1]
    if not pw_hash:
        return None

    return user_id if check_password_hash(pw_hash, password) else None

