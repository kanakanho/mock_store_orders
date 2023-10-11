import sqlite3
import json
import requests

json_data = requests.get(
    "https://esa-storage-tokyo.s3-ap-northeast-1.amazonaws.com/uploads/production/attachments/19973/2023/10/09/137427/727ebb1e-b620-41c7-a3ca-79e61b4bbf4d.json"
).json()


# SQLiteデータベースに接続
conn = sqlite3.connect("orders.db")
cursor = conn.cursor()

# ordersテーブルが存在しない場合は作成する
cursor.execute("CREATE TABLE IF NOT EXISTS orders (item TEXT, qty INTEGER)")

# Access the "orderNums" list from the JSON data
order_nums = json_data.get("orderNums", [])

# Iterate through each order in the list
for order in order_nums:
    try:
        if "orderList" in order:
            order_list = order["orderList"]
            for order_id, order_info in order_list.items():
                item = order_info.get("item")
                qty = order_info.get("qty")

                # 既に同じアイテムがテーブルに存在する場合は数量を足す
                cursor.execute("SELECT qty FROM orders WHERE item = ?", (item,))
                existing_qty = cursor.fetchone()

                if existing_qty:
                    new_qty = existing_qty[0] + qty
                    cursor.execute(
                        "UPDATE orders SET qty = ? WHERE item = ?", (new_qty, item)
                    )
                    print(f"update - {item}")
                else:
                    cursor.execute(
                        "INSERT INTO orders (item, qty) VALUES (?, ?)", (item, qty)
                    )
                    print(f"insert - {item}")
                conn.commit()
    except Exception as e:
        print("faild to insert")

# 変更をコミットし、接続を閉じる
conn.commit()
conn.close()
