from connector import get_connection

con = get_connection()
cur = con.cursor()
cur.execute("SELECT * from addresess")
result = cur.fetchall()
print(result)