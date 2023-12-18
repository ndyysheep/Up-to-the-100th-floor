from flask import Flask, render_template, request, jsonify
import random

from table_class import pull, push

app = Flask(__name__)

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
        self.a_description = '' #饰品描述

        # 加载饰品
        accessory_records = records['accessory']
        accessoryid_list = [int(i) for i in role.accessoryid.split()]
        for accessoryid in accessoryid_list:
            for accessory_record in accessory_records:
                if accessory_record.id == accessoryid:
                    self.hp += accessory_record.hp
                    self.atk += accessory_record.atk
                    self.dft += accessory_record.dft
                    self.a_description += accessory_record.description + "\n"  # 追加描述


records = pull()
role_records = records['role']
monster_records = records['monster']
role = next((i for i in role_records if i.id == 23), None)
monster0 = next((j for j in monster_records if j.m_id == 1), None)

status = Status(role, monster0, records)

def monster_action():
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

    # 重置玩家格挡值
    status.dft = 0
    return f"怪物使用了{mbev.b_description}造成了 {actual_damage} 点伤害,获得了{mbev.dft}点护盾！"

def check_game_over():
    if status.hp <= 0:
        status.die = True
        return " 游戏结束，你输了！"
    elif status.mhp <= 0:
        status.win = True
        # 需要回传的只有：hp, money
        role.hp = status.hp
        role.money += monster0.gold
        # 构造消息字符串
        message = " 你击败了" + monster0.m_name + "，你获得了" + str(monster0.gold) + "金币"
        # 执行数据库操作
        push(records)
        # 返回消息

        # 到达下一个楼层

        return message

    return ""

def update_player_status_with_item(item):
    # 更新玩家的攻击力和防御力
    status.atk += item.atk
    status.dft += item.dft
    status.hp += item.hp  # 假设道具也可以增加 HP

@app.route('/')
def index():
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
                           item1_name=status.item1.item_name,
                           item2_name=status.item2.item_name,
                           accessory_description=status.a_description,
                           status=status)  # 添加这一行
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
            # 玩家选择跳过回合
            status.actp = 0  # 损失所有行动点
            status.player_turn = False  # 切换到怪物回合
            message = monster_action()
            game_over_message = check_game_over()
            if not status.die and not status.win:
                status.player_turn = True  # 回到玩家回合
                status.actp = 3  # 恢复行动点
        elif action_type in ["item1", "item2"]:
            status.actp -= 1
            #  重置攻击力
            status.atk = 0
            selected_item = status.item1 if action_type == "item1" else status.item2
            update_player_status_with_item(selected_item)
            damage = status.atk

            if damage <= status.mdft:
                # 如果伤害小于或等于怪物的防御力，则只减少防御力
                status.mdft -= damage
                actual_damage = 0
            else:
                # 否则，先消耗防御力，剩余的伤害减少怪物生命值
                actual_damage = damage - status.mdft
                status.mhp -= actual_damage
                status.mdft = 0

            message = f"你使用了{selected_item.item_name}造成了 {actual_damage} 点伤害,获得了{selected_item.dft}点护盾！"
            game_over_message = check_game_over()
            if not status.die and not status.win and status.actp == 0:
                status.player_turn = False
                status.actp = 3
                message += " " + monster_action()
                game_over_message = check_game_over()
                if not status.die and not status.win:
                    status.player_turn = True
    else:
        status.player_turn = True

    # 始终返回更新后的状态
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
if __name__ == '__main__':
    app.run(debug=True)