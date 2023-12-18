import random

import table_class
from table_class import pull, push

class Status:
    def __init__(self, role, monster0, records):
        # 加载物品
        item_records = records['item']
        for item in item_records:
            if role.item_id1 == item.item_id:
                self.item1 = item
            elif role.item_id2 == item.item_id:
                self.item2 = item

        # 加载怪物行动模式
        self.bev = []
        behavior_records = records['behavior']
        for behave in behavior_records:
            if monster0.m_id == behave.m_id:
                self.bev.append(behave)

        self.role = role
        self.monster0 = monster0
        self.records = records
        self.actp = role.action_point

        # 初始化游戏情况
        self.win = False
        self.die = False
        self.player_turn = True

        # 初始化角色基础信息
        self.name = role.name
        self.mname = monster0.m_name
        self.hp = role.hp
        self.atk = 0  # 玩家攻击力
        self.dft = 0  # 玩家防御力
        self.mhp = monster0.hp
        self.matk = 0  # 怪物攻击力
        self.mdft = 0  # 怪物防御力
        self.a_description = ''  # 饰品描述

        # 加载饰品
        accessory_records = records['accessory']
        accessoryid_list = [int(i) for i in role.accessoryid.split()]
        for accessoryid in accessoryid_list:
            for accessory_record in accessory_records:
                if accessory_record.id == accessoryid:
                    self.hp += accessory_record.hp
                    self.atk += accessory_record.atk
                    self.dft += accessory_record.dft
                    self.a_description += accessory_record.description + "\n"

def monster_action(status):
    # 怪物护甲重置
    status.mdft = 0

    # 随机技能
    mbev = random.choice(status.bev)
    status.mhp += mbev.hp
    status.matk = mbev.atk
    status.mdft = mbev.dft

    base_damage = status.matk
    if base_damage <= status.dft:
        status.dft -= base_damage
        actual_damage = 0
    else:
        actual_damage = base_damage - status.dft
        status.hp -= actual_damage
        status.dft = 0
    # 重置玩家护盾
    status.dft = 0

    return f"怪物使用了{mbev.b_description}造成了 {actual_damage} 点伤害,获得了{mbev.dft}点护盾！"

def check_game_over(status):
    if status.hp <= 0:
        status.die = True  # 确保这行存在
        table_class.delete_role(status.role.id)
        return "游戏结束，你输了！"
    elif status.mhp <= 0:
        status.win = True
        status.role.hp = status.hp
        status.role.money += status.monster0.gold
        a = status.monster0.m_name
        b = status.monster0.gold
        push(status.records)
        message = f"你击败了{a}，你获得了{b}金币"
        return message

    return ""

def update_player_status_with_item(status, item):
    status.atk += item.atk
    status.dft += item.dft
    status.hp += item.hp  # 假设道具也可以增加 HP

def initialize_game(id ,m_id):
    records = pull()
    role_records = records['role']
    monster_records = records['monster']
    role = next((i for i in role_records if i.id == id), None)
    monster0 = next((j for j in monster_records if j.m_id == m_id), None)
    return Status(role, monster0, records)


