import sqlite3
import json
import requests
import datetime


json_data = requests.get(
    "https://esa-storage-tokyo.s3-ap-northeast-1.amazonaws.com/uploads/production/attachments/19973/2023/10/09/137427/727ebb1e-b620-41c7-a3ca-79e61b4bbf4d.json"
).json()

# SQLiteデータベースに接続
conn = sqlite3.connect("orders.db")
cursor = conn.cursor()


# ordersテーブルが存在しない場合は作成する
cursor.execute(
    "CREATE TABLE IF NOT EXISTS all_order (id INTEGER PRIMARY KEY AUTOINCREMENT,time INTEGER, item STRING, qty INTEGER, cheese STRING, mayo STRING, source STRING, ketchup STRING, salt STRING)"
)

for order in json_data["orderNums"]:
    if order:
        try:
            if order['timestamp']:
                unix_time = order["timestamp"]
                print(unix_time)
                unix_time = int(unix_time) / 1000
                time = datetime.datetime.fromtimestamp(unix_time)
                print(time)
            order_list = order["orderList"]
            for order_id, order_info in order_list.items():
                cheese, mayo, source, ketchup, salt = (
                    "false",
                    "false",
                    "false",
                    "false",
                    "false",
                )
                item = order_info.get("item")
                qty = order_info.get("qty")
                if order_info.get("options"):
                    options = order_info.get("options")
                    # optionsの中にあるチーズ、マヨネーズ、ソース、ケチャップ、塩の値を取得する
                    if "チーズ" in options:
                        cheese = "ture"
                    elif "マヨネーズ" in options:
                        mayo = "ture"
                    elif "ソース" in options:
                        source = "ture"
                    elif "ケチャップ" in options:
                        ketchup = "ture"
                    elif "塩" in options:
                        salt = "ture"
                    else:
                        pass
                if qty == 0:
                    continue
                cursor.execute(
                    "INSERT INTO all_order (time, item, qty, cheese, mayo, source, ketchup, salt) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (time, item, qty, cheese, mayo, source, ketchup, salt),
                )
                print(f"insert - {item}")
                conn.commit()
        except Exception as e:
            print("faild to insert")
# 変更をコミットし、接続を閉じる
conn.commit()
conn.close()
