import sys
import os
import json
from init_db import postgresql_connect


def data_fliter():
    # Get command line arguments
    target_dynasty = sys.argv[1] if len(sys.argv) > 1 else "all"
    target_province = sys.argv[2] if len(sys.argv) > 2 else "all"
    target_city = sys.argv[3] if len(sys.argv) > 3 else "all"

    TABLE_NAME = os.getenv("DB_TABLE_NAME")
 
    conn, cursor = postgresql_connect()

    # 构建动态 SQL
    query = f"SELECT * FROM {TABLE_NAME} WHERE 1=1"
    params = []

    if target_dynasty != "all":
        query += " AND dynasty=%s"
        params.append(target_dynasty)

    if target_province != "all":
        query += " AND province=%s"
        params.append(target_province)
        if target_city != "all":
            query += " AND city=%s"
            params.append(target_city)
    else:
        target_city = "all"

    # check if params is empty
    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()  # returns a list of dictionaries

    print(json.dumps(rows, ensure_ascii=False))

    cursor.close()
    conn.close()

if __name__ == "__main__":
    data_fliter()
