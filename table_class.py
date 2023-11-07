import psycopg2

def selectAll():
    try:
        con = psycopg2.connect(database="db", user="ztq", password="ztqnb123", host="47.113.185.205", port="5432")
        cursor = con.cursor()
        cursor.execute('''
            SELECT *
            FROM groupx;
            ''')
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
    finally:
        if con:
            con.close()

def test():
    print("Hello sql")

# 调用 selectAll 函数来执行 SQL 查询
selectAll()
