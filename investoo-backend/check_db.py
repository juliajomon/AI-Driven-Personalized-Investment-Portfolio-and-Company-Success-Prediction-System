import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def check_portfolio_table():
    """Check what's in the portfolios table"""
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )
        cursor = conn.cursor()
        
        # Check table structure
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'portfolios'
        """)
        columns = cursor.fetchall()
        print("Table columns:", columns)
        
        # Check all data
        cursor.execute("SELECT * FROM portfolios")
        all_data = cursor.fetchall()
        print("All portfolio data:", all_data)
        
        # Check specific user
        cursor.execute("SELECT * FROM portfolios WHERE user_id = %s", (2,))
        user_data = cursor.fetchall()
        print("User 2 data:", user_data)
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print("Database error:", e)

if __name__ == "__main__":
    check_portfolio_table()
