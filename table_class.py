def test():
    print("Hello world")


import psycopg2

def selectAll():
    con = psycopg2.connect(database="db",user="ztq",password="ztqnb123",host="47.113.185.205",port="5432")
    cursor = con.cursor()
    cursor.execute('''
        select *
        from groupx;
        ''')
    rows= cursor.fetchall()
    for row in rows:
        print(row)
def test():
    print("Hello sql")

