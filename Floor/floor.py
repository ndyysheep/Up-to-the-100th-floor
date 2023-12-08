from table_class import *
import copy
import random

def fight(role0, monster0, records):
    role = copy.deepcopy(role0)
    monster = copy.deepcopy(monster0)
    accessory_records = records['accessory']
    behavior_records = records['behavior']
    floor_records = records['floor']
    item_records = records['item']
    monster_records = records['monster']
    monsterlocation_records = records['monsterlocation']

    # 初始化游戏情况
    win = False  # 设置胜利情况为否
    die = False  # 设置死亡情况为否

    # 初始化角色基础信息
    hp = role.hp
    atk = 0
    dft = 0
    mhp = monster.hp
    matk = 0
    mdft = 0

    # 加载饰品
    accessoryid_list = [int(i) for i in role.accessoryid.split()]
    for accessoryid in accessoryid_list:
        for accessory_record in accessory_records:
            if accessory_record.id == accessoryid:
                hp += accessory_record.hp
                atk += accessory_record.atk
                dft += accessory_record.dft

    # 初始化装备情况
    for item in item_records:
        if role.item_id1 == item.item_id:
            item1 = item
        elif role.item_id2 == item.item_id:
            item2 = item
    item_name = "未知"

    # 初始化行动点
    actpoint = copy.deepcopy(role.action_point)

    # 加载怪物行动模式
    bev = []
    for behave in behavior_records:
        if monster.m_id == behave.m_id:
            bev.append(behave)

    while True:
        # 玩家回合

        # 玩家护甲重置
        dft = 0
        while(actpoint > 0):

            # 选择跳过回合或者进行战斗
            fchoice = input("请选择战斗(1), 跳过回合(2):")
            if fchoice == '2':
                break
            elif fchoice == '1':
                None
            # 判断行动后行动点是否为负
            while(1):
                print("请使用装备")
                print("您的装备有：")
                print(item1.item_name, "行动点：", item1.actp)
                print(item2.item_name, "行动点：", item2.actp)
                choice = input("请选择您要使用的装备：")
                if choice == item1.item_name:
                    item = item1
                    if actpoint - item.actp >= 0:
                        actpoint -= item.actp
                        print("使用了"+item.item_name)
                        hp += item.hp
                        atk += item.atk
                        dft += item.dft
                        print("现在你的数值为：")
                        print("hp:" + str(hp))
                        print("atk:" + str(atk))
                        print("dft:" + str(dft))
                        print("行动点为：" + str(actpoint))
                        break
                    else:
                        print("行动点不够，请切换武器")
                        continue

                if choice == item2.item_name:
                    item = item2
                    if actpoint - item.actp >= 0:
                        actpoint -= item.actp
                        print("使用了"+item.item_name)
                        hp += item.hp
                        atk += item.atk
                        dft += item.dft
                        print("现在你的数值为：")
                        print("hp:" + str(hp))
                        print("atk:" + str(atk))
                        print("dft:" + str(dft))
                        print("行动点为：" + str(actpoint))
                        break
                    else:
                        print("行动点不够，请切换武器")
                        continue

            # 攻击判定
            if atk > 0:
                print(monster.m_name + "受到了" + str(atk) + "点伤害")
                if mdft > 0:
                    mdft -= atk
                    if mdft >= 0:
                        print(monster.m_name + "血量为：" + str(mhp) + "+" + str(mdft))
                    else:
                        mhp += mdft
                        print(monster.m_name + "血量为：" + str(mhp))
                else:
                    mhp -= atk
                    print(monster.m_name + "血量为：" + str(mhp))
                atk = 0

            # 检查玩家的生命值
            if hp <= 0:
                print("游戏结束")
                die = True
                break

            # 检查怪物生命值
            if mhp <= 0:
                win = True
                print("游戏获胜")
                print("你获得了" + str(monster.gold) + "金币")
                role.money += monster.gold
                break

        # 外层循环检测
        if die == True or win == True:
            break
        # 怪物回合

        # 怪物护甲重置
        mdft = 0

        print("进入"+monster.m_name +"的回合")
        # 随机技能
        mbev = random.choice(bev)
        print(monster.m_name+"使用了"+mbev.b_description)
        monster.hp += mbev.hp
        matk = mbev.atk
        mdft = mbev.dft
        matk = 5
        # 怪物攻击检测
        if matk > 0:
            print(role.name + "受到了" + str(matk) + "点伤害")
            if dft > 0:
                dft -= matk
                if dft >= 0:
                    print(role.name + "血量为：" + str(hp) + "+" + str(dft))
                else:
                    hp += dft
                    print(role.name + "血量为：" + str(hp))
            else:
                hp -= matk
                print(role.name + "血量为：" + str(hp))
            matk = 0

        # 护甲加载
        if mdft > 0:
            print(monster.m_name + "获得了" + str(mdft) + "点护甲")

        print(monster.m_name+"的状态为：")
        print(monster.m_name+"hp:" + str(mhp))
        print(monster.m_name+"atk:" + str(matk))
        print(monster.m_name+"dft:" + str(mdft))

        # 检查玩家的生命值
        if hp <= 0:
            print("游戏结束")
            die = True
            break

        # 检查怪物生命值
        if mhp <= 0:
            win = True
            print("游戏获胜")
            print("你获得了" + str(monster.gold) + "金币")
            role.money += monster.gold
            break

        # 重置玩家行动点
        actpoint = copy.deepcopy(role.action_point)


    if win == True:
        print("进入下一层")
        role0 = role

    if die == True:
        print("删除角色")



        # 玩家回合逻辑


# 使用函数的示例
records = pull()
role_records = records['role']
monster_records = records['monster']
role = next((i for i in role_records if i.id == 1), None)
monster = next((j for j in monster_records if j.m_id == 1), None)

if role and monster:
    fight(role, monster, records)
# push(records)
