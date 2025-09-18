import mysql.connector
import pandas as pd
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(BASE_DIR, "..", "config", "config.json")
# with open(config_path, "r", encoding="utf-8") as f:
#     config = json.load(f)

# 配置
config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "database": os.getenv("DB_NAME"),
    "table_name":os.getenv("DB_TABLE_NAME"),
    "port": int(os.getenv("DB_PORT")) 
    }
DB_NAME = config["database"]
DB_USER = config["user"]
DB_PASSWORD = config["password"]
DB_HOST = config["host"]
TABLE_NAME = config["table_name"]
DB_PORT = config["port"]
EXCEL_FILE = os.path.join(BASE_DIR, "..", "data", "mausoleums.xlsx")

print(f"Using database config: host={DB_HOST}, user={DB_USER}, database={DB_NAME}, port={DB_PORT}", flush=True)


def init_db():
    print("Initializing the database...")
    print(f"Using database config: host={DB_HOST}, user={DB_USER}, database={DB_NAME}, port={DB_PORT}", flush=True)
    # 1. 先连接 MySQL（不指定数据库）
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        database=DB_NAME,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    cursor = conn.cursor()

    # 2. 检查数据库是否存在
    cursor.execute("SHOW DATABASES LIKE %s;", (DB_NAME,))
    exists = cursor.fetchone()

    if not exists:
        print(f"Database {DB_NAME} does not exist, building it...")
        cursor.execute(f"CREATE DATABASE {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    else:
        print(f"Database {DB_NAME} already exists.")

    cursor.close()
    conn.close()

    # 3. 连接到目标数据库
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )
    cursor = conn.cursor()

    # 4. 创建表 mausoleums（如果不存在）
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        dynasty VARCHAR(50),
        emperor VARCHAR(50),
        reign_title VARCHAR(50),
        start_year INT,
        end_year INT,
        tomb_name VARCHAR(100),
        province VARCHAR(50),
        city VARCHAR(50),
        location VARCHAR(255),
        lat DOUBLE,
        lng DOUBLE
    );
    """)

    # 5. 清空表（如果已经存在数据）
    cursor.execute(f"TRUNCATE TABLE {TABLE_NAME};")
    # print(f"表 {TABLE_NAME} 已清空，准备导入新数据...")

    # 6. 读取 Excel 数据
    df = pd.read_excel(EXCEL_FILE)
    df = df.where(pd.notnull(df), None)  # 将所有 NaN 替换为 None

    # 7. 插入数据
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
    print("Finished initializing the database.")

if __name__ == "__main__":
    init_db()

