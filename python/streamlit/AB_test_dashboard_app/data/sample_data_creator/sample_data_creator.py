import sqlite3
import polars as pl

# # データベースファイルを指定します
# db_file = "school.db"
# # SQLファイルを指定します
# sql_file = "data/sample_data_creator/sql/queries.sql"

# # データベースに接続します
# conn = sqlite3.connect(db_file)
# cursor = conn.cursor()

# # SQLファイルを読み込みます
# with open(sql_file, "r") as file:
#     sql_script = file.read()

# # SQLスクリプトを実行します
# cursor.executescript(sql_script)

# # コミットして接続を閉じます
# conn.commit()
# conn.close()

# print("SQL script executed successfully.")

import sqlite3

# データベースファイルを指定します
db_file = "school.db"

# データベースに接続します
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# データを取得します
cursor.execute("SELECT * FROM students")
data = cursor.fetchall()
column_names = [description[0] for description in cursor.description]
df = pl.DataFrame(data, schema=column_names)
print(df)
