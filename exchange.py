import sqlite3

# db接続
db_name = "orders.db"
conn = sqlite3.connect(db_name)
cur = conn.cursor()

# sevenテーブルが存在しない場合は作成する
cur.execute(
    "CREATE TABLE IF NOT EXISTS seven (id INTEGER PRIMARY KEY AUTOINCREMENT,time INTEGER, item STRING, qty INTEGER, cheese STRING, mayo STRING, source STRING, ketchup STRING, salt STRING)"
)

# eightテーブルが存在しない場合は作成する
cur.execute(
    "CREATE TABLE IF NOT EXISTS eight (id INTEGER PRIMARY KEY AUTOINCREMENT,time INTEGER, item STRING, qty INTEGER, cheese STRING, mayo STRING, source STRING, ketchup STRING, salt STRING)"
)

# all_orderテーブルからデータを取得する
cur.execute("select time , item , qty , cheese , mayo , source , ketchup , salt from all_order where time like '2023-10-07%'")
rows_seven = cur.fetchall()

# sevenテーブルにデータを挿入する
cur.executemany(
    "INSERT INTO seven (time, item, qty, cheese, mayo, source, ketchup, salt) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    rows_seven,
)

# 変更をコミット
conn.commit()

# all_orderテーブルからデータを取得する
cur.execute("select time , item , qty , cheese , mayo , source , ketchup , salt from all_order where time like '2023-10-08%'")
rows_eight = cur.fetchall()

# eightテーブルにデータを挿入する
cur.executemany(
    "INSERT INTO eight (time, item, qty, cheese, mayo, source, ketchup, salt) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    rows_eight,
)

# 変更をコミット
conn.commit()

conn.close()