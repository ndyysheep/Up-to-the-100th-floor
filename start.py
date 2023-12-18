from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import random
from table_class import *
from flask import Flask, render_template, request, jsonify
import battle
from profile import get_profile_info



app = Flask(__name__)

conn = psycopg2.connect(
    database="db",
    user="ztq",
    password="ztqnb123",
    host="47.113.185.205",
    port="5432"
)
cur = conn.cursor()


def get_role(username):
    cur.execute("SELECT role.name, role.id, role.f_id FROM role, users WHERE users.username = '{:s}' and role.user_id "
                "= users.id".format(username))
    roles = ()
    for i in range(3):
        role = cur.fetchone()
        if role:
            roles += role
        else:
            roles += ('创建新角色', '', 0)
    return render_template("success.html", username=username
                           , role_name0=roles[0], role_id0=roles[1], floor0=roles[2]
                           , role_name1=roles[3], role_id1=roles[4], floor1=roles[5]
                           , role_name2=roles[6], role_id2=roles[7], floor2=roles[8])


def getRole(username, role_id):
    if role_id != '':
        cur.execute("SELECT f_id, name FROM role WHERE role.id = {:s}".format(role_id))
        role = cur.fetchone()
        m_id = goNextFloor(role[0])
        # return render_template("game.html", role_id=role_id, m_id=m_id)
        return render_template("floor.html", floor_id=role[0], role_name=role[1], role_id=role_id)
    else:
        name = request.form['newRoleName']
        cur.execute("SELECT id FROM users WHERE users.username = '{:s}'".format(username))
        user_id = cur.fetchone()[0]
        cur.execute("INSERT INTO role (f_id,name,hp,money,action_point,item_id1,item_id2,accessoryid,user_id) "
                    "VALUES (1,'{:s}',50,0,3,10001,10002,'1 2',{:d})".format(name, user_id)
                    )
        conn.commit()
        records = pull()
        role_records = records['role']
        role = role_records[-1]
        return get_role(username)


def goNextFloor(floor):
    ShopOrMonster = False
    layer = floor // 10 + 1
    if floor % 10 == 0:
        print(layer)
        ShopOrMonster = True
        return ShopOrMonster, layer-1
    else:
        cur.execute("SELECT m_id FROM monsterlocation WHERE monsterlocation.l_id = {:d}".format(layer))
        m_id = cur.fetchall()[random.randint(0, 0)]
        return ShopOrMonster, m_id

def deleteRole(role_id):
    cur.execute("DELETE FROM role WHERE role.id = {:s}".format(role_id))
    conn.commit()
    return True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login/', methods=['POST', 'GET'])
def login():
    action = request.form['action']
    if action == '登录':
        username = request.form['username']
        password = request.form['password']

        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        if user:
            return get_role(username)
        else:
            return render_template('failure.html')
    elif action == '注册':
        return render_template('register.html')


@app.route('/register/', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()

        if user:
            cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user_pwd = cur.fetchone()
            if user_pwd:
                return get_role(username)
            else:
                return render_template("index.html")

        else:
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            return get_role(username)
    else:
        return render_template('register.html')


@app.route('/start/', methods=['POST', 'GET'])
def start():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        action = request.form['action']
        username = request.form['username']
        if action == "存档一":
            role_id = request.form['role_id0']
            return getRole(username, role_id)
        if action == "存档二":
            role_id = request.form['role_id1']
            return getRole(username, role_id)
        if action == "存档三":
            role_id = request.form['role_id2']
            return getRole(username, role_id)

@app.route('/floor/', methods=['POST', 'GET'])
def floor():
    action = request.form.get('action')  # 使用 .get() 避免 KeyError
    role_id = request.form['role_id']
    cur.execute("SELECT f_id, name FROM role WHERE role.id = {:s}".format(role_id))
    role = cur.fetchone()
    f_id = role[0]
    role_name = role[1]
    if action == "前往下一层":
        cur.execute("UPDATE role SET f_id = {:d} WHERE role.id = {:s}".format(f_id + 1, role_id))
        conn.commit()
        ShopOrMonster, temp = goNextFloor(f_id + 1)
        if ShopOrMonster:
            return render_template("shop.html", role_id=role_id, layer=temp)
        else:
            return render_template("floor.html", role_name=role_name, floor_id=f_id+1, role_id=role_id)
            #return render_template("game.html", role_id=role_id, f_id=temp)
    if action == "退出游戏":
        return render_template("index.html")
    if action == "查看角色信息":
        # 重定向到角色信息页面
        return redirect(url_for('profile_index', floor_id=role[0], role_name=role[1], role_id=role_id))
    # 如果没有匹配的动作，可以重定向到主页或返回一个默认页面
    return redirect(url_for('menu'))


@app.route('/shop/', methods=['POST', 'GET'])
def shop():
    action = request.form['action']
    role_id = request.form['role_id']
    layer = request.form['layer']
    if action == "购买":
        item_id = request.form['item_id']
        cur.execute("SELECT money FROM role WHERE role.id = {:s}".format(role_id))
        money = cur.fetchone()[0]
        cur.execute("SELECT price FROM item WHERE item.id = {:s}".format(item_id))
        price = cur.fetchone()[0]
        if money < price:
            return render_template("failure.html")
        else:
            cur.execute("UPDATE role SET money = {:d} WHERE role.id = {:s}".format(money - price, role_id))
            conn.commit()
            cur.execute("SELECT item_id1, item_id2 FROM role WHERE role.id = {:s}".format(role_id))
            item_id1, item_id2 = cur.fetchone()
            if item_id1 == 10001:
                cur.execute("UPDATE role SET item_id1 = {:s} WHERE role.id = {:s}".format(item_id, role_id))
            else:
                cur.execute("UPDATE role SET item_id2 = {:s} WHERE role.id = {:s}".format(item_id, role_id))
            conn.commit()
            return render_template("success.html", role_id=role_id, layer=layer)
    if action == "退出游戏":
        return render_template("index.html")
    if action == "查看角色信息":
        return render_template("role.html", role_id=role_id)



@app.route('/delete', methods=['GET'])
def delete():
    username = request.args.get('username')
    role_id = request.args.get('role_id')

    if deleteRole(role_id):
        return get_role(username)
    else:
        return "删除失败"

@app.route('/battle/<int:player_id>/<int:monster_id>')
def battle_index(player_id, monster_id):
    # 根据传递的 ID 初始化游戏状态
    global  status
    status = battle.initialize_game(player_id, monster_id)

    return render_template('battle.html',
                           player_health=status.hp,
                           player_atk=status.atk,
                           player_dft=status.dft,
                           enemy_health=status.mhp,
                           player_turn=status.player_turn,
                           enemy_name=status.mname,
                           enemy_matk=status.matk,
                           enemy_mdft=status.mdft,
                           player_name=status.name,
                           item1_name=status.item1.item_name if status.item1 else '无',
                           item2_name=status.item2.item_name if status.item2 else '无',
                           accessory_description=status.a_description,
                           status=status)


@app.route('/action', methods=['POST'])
def action():
    global status
    if status.die or status.win:

        return jsonify({
            "game_over": status.die or status.win,
            "victory": status.win,
            "message": "游戏已结束",
            "player_hp": status.hp,
            "enemy_health": status.mhp
        })


    action_type = request.json['action_type']

    if status.player_turn:
        if action_type == "skip":
            status.actp = 0
            status.player_turn = False
            message = battle.monster_action(status)
            game_over_message = battle.check_game_over(status)
            if not status.die and not status.win:
                status.player_turn = True
                status.actp = 3
        elif action_type in ["item1", "item2"]:
            status.actp -= 1
            status.atk = 0
            selected_item = status.item1 if action_type == "item1" else status.item2
            battle.update_player_status_with_item(status, selected_item)
            damage = status.atk

            if damage <= status.mdft:
                status.mdft -= damage
                actual_damage = 0
            else:
                actual_damage = damage - status.mdft
                status.mhp -= actual_damage
                status.mdft = 0

            message = f"你使用了{selected_item.item_name}造成了 {actual_damage} 点伤害,获得了{selected_item.dft}点护盾！"
            game_over_message = battle.check_game_over(status)
            if not status.die and not status.win and status.actp == 0:
                status.player_turn = False
                status.actp = 3
                message += " " + battle.monster_action(status)
                game_over_message = battle.check_game_over(status)
                if not status.die and not status.win:
                    status.player_turn = True
    else:
        status.player_turn = True

    return jsonify({
        "player_hp": status.hp,
        "enemy_health": status.mhp,
        "player_atk": status.atk,
        "player_dft": status.dft,
        "enemy_matk": status.matk,
        "enemy_mdft": status.mdft,
        "action_points": status.actp,
        "player_turn": status.player_turn,
        "message": message + game_over_message,
        "game_over": status.die or status.win,
        "victory": status.win
    })

@app.route('/profile/<int:player_id>')  # 动态路由
def profile_index(player_id):
    profile_info = get_profile_info(player_id)
    if profile_info:
        return render_template('profile.html', profile=profile_info)
    else:
        return "玩家信息未找到", 404





if __name__ == '__main__':
    app.run(debug=True)

cur.close()
conn.close()
