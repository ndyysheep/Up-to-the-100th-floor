from flask import Flask, render_template, request, redirect, url_for
import psycopg2

def login():
    app = Flask(__name__)

    # 连接 PostgreSQL 数据库
    conn = psycopg2.connect(
        database="db",
        user="ztq",
        password="ztqnb123",
        host="47.113.185.205",
        port="5432"
    )

    # 创建一个数据库游标
    cur = conn.cursor()

    # 创建用户表
    cur.execute('''
        DROP TABLE IF EXISTS users;
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        );
    ''')

    # 插入测试数据
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", ('LXY', '123'))
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", ('YXY', 'letmein'))
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", ('CHY', 'securepwd'))

    conn.commit()

    # 定义路由
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login', methods=['POST'])
    def login():
        username = request.form['username']
        password = request.form['password']

        # 查询数据库中是否存在匹配的用户名和密码
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()

        if user:
            return render_template('success.html', username=username)
        else:
            return render_template('failure.html')

    # 关闭数据库连接
    cur.close()
    conn.close()

    return app

# if __name__ == '__main__':
#     app = login()
#     app.run(debug=True)
