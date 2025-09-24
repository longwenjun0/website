import pandas as pd
import os
import psycopg2
from psycopg2.extras import RealDictCursor

def postgresql_connect():
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("❌ Do not set environment variable DATABASE_URL")
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

    # 1️⃣ 创建表（如果不存在，默认列）
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id SERIAL PRIMARY KEY,
        dynasty VARCHAR(50),
        country_name VARCHAR(50),
        posthumous_title VARCHAR(100),
        emperor VARCHAR(50),
        temple_name VARCHAR(50),
        reign_title VARCHAR(50),
        reign VARCHAR(50),
        tomb_name VARCHAR(100),
        province VARCHAR(50),
        city VARCHAR(50),
        lat DOUBLE PRECISION,
        lng DOUBLE PRECISION
    );
    """)
    print(f"✅ Table {TABLE_NAME} ensured to exist.")

    # 2️⃣ 获取数据库现有列（排除 id）
    cursor.execute(f"""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = %s AND column_name != 'id';
    """, (TABLE_NAME,))
    db_cols = [row['column_name'] for row in cursor.fetchall()]

    # 3️⃣ 读取 Excel 数据
    df = pd.read_excel(EXCEL_FILE)
    df = df.where(pd.notnull(df), None)  # 将 NaN 转成 None
    excel_cols = df.columns.tolist()

    # 4️⃣ 数据库多余列 → 删除
    for col in db_cols:
        if col not in excel_cols:
            cursor.execute(f"ALTER TABLE {TABLE_NAME} DROP COLUMN {col} CASCADE;")
            print(f"🗑️ Dropped column {col} from table")

    # 5️⃣ Excel 多余列 → 动态添加到数据库
    # 重新获取数据库列（因为可能删除了）
    cursor.execute(f"""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = %s AND column_name != 'id';
    """, (TABLE_NAME,))
    db_cols = [row['column_name'] for row in cursor.fetchall()]

    for col in excel_cols:
        if col not in db_cols:
            cursor.execute(f"ALTER TABLE {TABLE_NAME} ADD COLUMN {col} TEXT;")
            print(f"➕ Added column {col} to table")

    # 6️⃣ 清空表数据
    cursor.execute(f"TRUNCATE TABLE {TABLE_NAME} RESTART IDENTITY CASCADE;")
    print(f"✅ Table {TABLE_NAME} truncated")

    # 7️⃣ 动态列插入
    # 再次获取列名顺序（确保和 Excel 对齐）
    cursor.execute(f"""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = %s AND column_name != 'id';
    """, (TABLE_NAME,))
    db_cols = [row['column_name'] for row in cursor.fetchall()]

    columns_str = ",".join(db_cols)
    placeholders = ",".join(["%s"] * len(db_cols))

    for _, row in df.iterrows():
        values = [row.get(col) for col in db_cols]  # Excel 没有的列会自动填 None
        cursor.execute(f"INSERT INTO {TABLE_NAME} ({columns_str}) VALUES ({placeholders})", values)

    # 8️⃣ 提交事务并关闭
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Finished initializing the PostgreSQL database dynamically.")

if __name__ == "__main__":
    init_db()
