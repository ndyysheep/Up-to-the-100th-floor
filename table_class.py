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


class Role:
    def __init__(self, ID, F_ID, name, HP, money, action_point, item_id1, item_id2):
        self.ID = ID  # 角色ID
        self.F_ID = F_ID  # 属于的楼层ID
        self.name = name  # 角色名称
        self.HP = HP  # 生命值
        self.money = money  # 金钱
        self.action_point = action_point  # 行动点数
        self.item_id1 = item_id1  # 物品1 ID
        self.item_id2 = item_id2  # 物品2 ID


class Users:
    def __init__(self, user_ID, user_name, pwd, player_id1, player_id2, player_id3):
        self.user_ID = user_ID  # 用户ID
        self.user_name = user_name  # 用户名
        self.pwd = pwd  # 密码
        self.player_id1 = player_id1  # 玩家1 ID
        self.player_id2 = player_id2  # 玩家2 ID
        self.player_id3 = player_id3  # 玩家3 ID


class Terrain:
    def __init__(self, L_ID, L_name, L_description):
        self.L_ID = L_ID  # 地形ID
        self.L_name = L_name  # 地形名称
        self.L_description = L_description  # 地形描述


class Floor:
    def __init__(self, F_ID, L_ID, M_ID1, M_ID2, M_ID3):
        self.F_ID = F_ID  # 楼层ID
        self.L_ID = L_ID  # 地形ID
        self.M_ID1 = M_ID1  # 怪物1 ID
        self.M_ID2 = M_ID2  # 怪物2 ID
        self.M_ID3 = M_ID3  # 怪物3 ID


class MonsterLocation:
    def __init__(self, M_ID, L_ID, M_name, L_name):
        self.M_ID = M_ID  # 怪物ID
        self.L_ID = L_ID  # 地点ID
        self.M_name = M_name  # 怪物名称
        self.L_name = L_name  # 地点名称


class Monster:
    def __init__(self, M_ID, M_name, HP, ATK, DEF):
        self.M_ID = M_ID  # 怪物ID
        self.M_name = M_name  # 怪物名称
        self.HP = HP  # 生命值
        self.ATK = ATK  # 攻击力
        self.DEF = DEF  # 防御力


class Item:
    def __init__(self, item_ID, item_name, HP, ATK, DEF, I_description, price):
        self.item_ID = item_ID  # 物品ID
        self.item_name = item_name  # 物品名称
        self.HP = HP  # 增加的生命值
        self.ATK = ATK  # 增加的攻击力
        self.DEF = DEF  # 增加的防御力
        self.I_description = I_description  # 物品描述
        self.price = price  # 价格


class Accessory:
    def __init__(self, ID, name, description, HP, ATK, DEF):
        self.ID = ID  # 配饰ID
        self.name = name  # 配饰名称
        self.description = description  # 配饰描述
        self.HP = HP  # 增加的生命值
        self.ATK = ATK  # 攻击力


class Behavior:
    def __init__(self, B_ID, M_ID, HP, ATK, DEF, B_description):
        self.B_ID = B_ID  # 行为ID
        self.M_ID = M_ID  # 怪物ID
        self.HP = HP  # 影响的生命值
        self.ATK = ATK  # 影响的攻击力
        self.DEF = DEF  # 影响的防御力
        self.B_description = B_description  # 行为描述


class Shop:
    def __init__(self, L_ID, item_id1, item_id2, item_id3):
        self.L_ID = L_ID  # 地点ID
        self.item_id1 = item_id1  # 物品1 ID
        self.item_id2 = item_id2  # 物品2 ID
        self.item_id3 = item_id3  # 物品3 ID

class AccessoryOwnership:
    def __init__(self, accessory_ID, role_ID, accessory_name, role_name):
        self.accessory_ID = accessory_ID  # 配饰ID
        self.role_ID = role_ID  # 角色ID
        self.accessory_name = accessory_name  # 配饰名称
        self.role_name = role_name  # 角色名称


