import sys
import os
import json
import mysql.connector  # 使用 mysql-connector-python


def data_fliter():
    # rows = [
    #     {
    #         "id": 1,
    #         "name": "示例陵墓",
    #         "dynasty": "唐",
    #         "province": "陕西",
    #         "city": "西安",
    #         "description": "这是一个示例陵墓。",
    #         "lat": 34.3416,
    #         "lng": 108.9398
    #     }
    # ]

    # 获取 Node.js 传入的参数
    target_dynasty = sys.argv[1] if len(sys.argv) > 1 else "all"
    target_province = sys.argv[2] if len(sys.argv) > 2 else "all"
    target_city = sys.argv[3] if len(sys.argv) > 3 else "all"

    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # config_path = os.path.join(BASE_DIR, "..", "config", "config.json")

    # with open(config_path, "r", encoding="utf-8") as f:
    #     config = json.load(f)
    config = {
        "host": os.getenv("DB_HOST"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASS"),
        "database": os.getenv("DB_NAME"),
        "table_name":os.getenv("DB_TABLE_NAME"),
        "port": int(os.getenv("DB_PORT")) 
    }

    # 1. 创建数据库连接
    conn = mysql.connector.connect(
        host=config["host"],       
        user=config["user"],            
        password=config["password"], 
        database=config["database"],
        port=config["port"]
    )

    # 2. 创建游标（返回字典）
    cursor = conn.cursor(dictionary=True)

    # 4. 构建动态 SQL
    query = "SELECT * FROM mausoleums WHERE 1=1"
    params = []

    # 朝代筛选
    if target_dynasty != "all":
        query += " AND dynasty=%s"
        params.append(target_dynasty)

    # 省份筛选
    if target_province != "all":
        query += " AND province=%s"
        params.append(target_province)

        # 城市筛选，仅当省份不是all且城市不是all时
        if target_city != "all":
            query += " AND city=%s"
            params.append(target_city)
    else:
        # target_province 是all时，强制 target_city 也是all
        target_city = "all"

    # 5. 执行查询
    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()


    print(json.dumps(rows, ensure_ascii=False))

    # # 7. 关闭游标和连接
    cursor.close()
    conn.close()

if __name__ == "__main__":
    data_fliter()
