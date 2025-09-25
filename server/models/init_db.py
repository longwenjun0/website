import pandas as pd
import os
import psycopg2
import math
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

def sanitize_value(val):
    """把 NaN 转换成 None，保证能写入 PostgreSQL"""
    if val is None:
        return None
    if isinstance(val, float) and math.isnan(val):
        return None
    return val

def detect_col_type(series: pd.Series) -> str:
    """根据 Excel 列数据推断 PostgreSQL 类型"""
    # 如果列是全空，默认为 TEXT
    if series.dropna().empty:
        return "TEXT"

    # 如果全是数值（或 NaN），用 DOUBLE PRECISION
    if pd.api.types.is_numeric_dtype(series):
        return "DOUBLE PRECISION"

    # 否则用 TEXT
    return "TEXT"

def init_db():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    EXCEL_FILE = os.path.join(BASE_DIR, "..", "data", "mausoleums.xlsx")
    TABLE_NAME = os.getenv("DB_TABLE_NAME")

    conn, cursor = postgresql_connect()

    # 1️⃣ 删除原表
    cursor.execute(f"DROP TABLE IF EXISTS {TABLE_NAME} CASCADE;")
    print(f"🗑️ Dropped table {TABLE_NAME} if existed")

    # 2️⃣ 读取 Excel 数据
    df = pd.read_excel(EXCEL_FILE)
    df = df.where(pd.notnull(df), None)  # 把 NaN 转 None
    excel_cols = df.columns.tolist()

    # 3️⃣ 自动生成列定义
    col_defs = []
    for col in excel_cols:
        col_type = detect_col_type(df[col])
        col_defs.append(f'"{col}" {col_type}')
    create_cols = ", ".join(col_defs)

    cursor.execute(f"""
        CREATE TABLE {TABLE_NAME} (
            id SERIAL PRIMARY KEY,
            {create_cols}
        );
    """)
    print(f"✅ Created new table {TABLE_NAME} with detected column types")

    # 4️⃣ 插入数据
    columns_str = ",".join([f'"{col}"' for col in excel_cols])
    placeholders = ",".join(["%s"] * len(excel_cols))

    for _, row in df.iterrows():
        values = [sanitize_value(row.get(col)) for col in excel_cols]
        cursor.execute(
            f"INSERT INTO {TABLE_NAME} ({columns_str}) VALUES ({placeholders})",
            values
        )

    # 5️⃣ 提交并关闭
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Finished reinitializing PostgreSQL database (drop + recreate).")

if __name__ == "__main__":
    init_db()
