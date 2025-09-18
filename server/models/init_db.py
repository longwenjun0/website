import pandas as pd
import os
import psycopg2
from psycopg2.extras import RealDictCursor


def postgresql_connect():
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("❌ Do not set enviornment variables  DATABASE_URL")
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    return conn, cursor

def init_db():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    EXCEL_FILE = os.path.join(BASE_DIR, "..", "data", "mausoleums.xlsx")
    TABLE_NAME = os.getenv("DB_TABLE_NAME")

    conn, cursor = postgresql_connect()
    # create table if not exists
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id SERIAL PRIMARY KEY,
        dynasty VARCHAR(50),
        emperor VARCHAR(50),
        reign_title VARCHAR(50),
        start_year INT,
        end_year INT,
        tomb_name VARCHAR(100),
        province VARCHAR(50),
        city VARCHAR(50),
        location VARCHAR(255),
        lat DOUBLE PRECISION,
        lng DOUBLE PRECISION
    );
    """)
    # print(f"✅ Table {TABLE_NAME} ensured to exist.")

    # clear existing data
    cursor.execute(f"TRUNCATE TABLE {TABLE_NAME} RESTART IDENTITY;")
    # print(f"✅ Table {TABLE_NAME} truncated.")

    # Read Excel file
    df = pd.read_excel(EXCEL_FILE)
    df = df.where(pd.notnull(df), None) 

    # Insert data into the table
    for _, row in df.iterrows():
        cursor.execute(f"""
        INSERT INTO {TABLE_NAME} 
        (dynasty, emperor, reign_title, start_year, end_year, tomb_name, province, city, lat, lng)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            row['dynasty'], row['name'], row['reign_title'],
            row['start_year'], row['end_year'], row['tomb_name'],
            row['province'], row['city'], 
            row['lat'], row['lng']
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print("Finished initializing the PostgreSQL database.")

if __name__ == "__main__":
    init_db()

