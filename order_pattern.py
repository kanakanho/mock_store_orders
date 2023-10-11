import sqlite3

conn = sqlite3.connect('orders.db')
cursor = conn.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS option_pattern (id INTEGER PRIMARY KEY AUTOINCREMENT, cheese string, mayo string, sauce string,ketchup string)')

# これの全ての組み合わせをコミットする
for i in range(2):
    for j in range(2):
        for k in range(2):
            for l in range(2):
                # 1のときはtrue, 0のときはfalse
                cheese = 'true' if i == 1 else 'false'
                mayo = 'true' if j == 1 else 'false'
                sauce = 'true' if k == 1 else 'false'
                ketchup = 'true' if l == 1 else 'false'
                cursor.execute('INSERT INTO option_pattern (cheese, mayo, sauce, ketchup) VALUES (?, ?, ?, ?)', (cheese, mayo, sauce, ketchup))
                conn.commit()
