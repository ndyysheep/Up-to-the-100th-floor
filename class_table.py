class Role:
    def __init__(self, ID, F_ID, name, HP, ATK, DEF, money, action_point, item_id1, item_id2):
        self.ID = ID
        self.F_ID = F_ID
        self.name = name
        self.HP = HP
        self.ATK = ATK
        self.DEF = DEF
        self.money = money
        self.action_point = action_point
        self.item_id1 = item_id1
        self.item_id2 = item_id2

class User:
    def __init__(self, user_ID, user_name, pwd, player_id1, player_id2, player_id3):
        self.user_ID = user_ID
        self.user_name = user_name
        self.pwd = pwd
        self.player_id1 = player_id1
        self.player_id2 = player_id2
        self.player_id3 = player_id3

class Terrain:
    def __init__(self, L_ID, L_name, L_description):
        self.L_ID = L_ID
        self.L_name = L_name
        self.L_description = L_description

class Floor:
    def __init__(self, F_ID, L_ID, M_ID1, M_ID2, M_ID3):
        self.F_ID = F_ID
        self.L_ID = L_ID
        self.M_ID1 = M_ID1
        self.M_ID2 = M_ID2
        self.M_ID3 = M_ID3

class MonsterLocation:
    def __init__(self, M_ID, L_ID, M_name, L_name):
        self.M_ID = M_ID
        self.L_ID = L_ID
        self.M_name = M_name
        self.L_name = L_name

class Monster:
    def __init__(self, M_ID, M_name, HP, ATK, DEF):
        self.M_ID = M_ID
        self.M_name = M_name
        self.HP = HP
        self.ATK = ATK
        self.DEF = DEF

class Item:
    def __init__(self, item_ID, item_name, HP, ATK, DEF, I_description, price):
        self.item_ID = item_ID
        self.item_name = item_name
        self.HP = HP
        self.ATK = ATK
        self.DEF = DEF
        self.I_description = I_description
        self.price = price

class Accessory:
    def __init__(self, ID, name, description, HP, ATK, DEF):
        self.ID = ID
        self.name = name
        self.description = description
        self.HP = HP
        self.ATK = ATK
        self.DEF = DEF

class Behavior:
    def __init__(self, B_ID, M_ID, HP, ATK, DEF, B_description):
        self.B_ID = B_ID
        self.M_ID = M_ID
        self.HP = HP
        self.ATK = ATK
        self.DEF = DEF
        self.B_description = B_description

class Shop:
    def __init__(self, L_ID, item_id1, item_id2, item_id3):
        self.L_ID = L_ID
        self.item_id1 = item_id1
        self.item_id2 = item_id2
        self.item_id3 = item_id3

class AccessoryOwnership:
    def __init__(self, accessory_ID, role_ID, accessory_name, role_name):
        self.accessory_ID = accessory_ID
        self.role_ID = role_ID
        self.accessory_name = accessory_name
        self.role_name = role_name
