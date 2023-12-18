from table_class import pull


def get_profile_info(player_id):
    records = pull()  # 拉取所有相关记录
    role_records = records['role']

    # 根据提供的玩家 ID 找到相应的角色
    role = next((r for r in role_records if r.id == player_id), None)

    if not role:
        return None  # 如果找不到角色，返回 None 或合适的错误信息

    # 以下为基于找到的角色构建状态
    item_records = records['item']
    for item in item_records:
        if role.item_id1 == item.item_id:
            item1 = item
        elif role.item_id2 == item.item_id:
            item2 = item

    accessory = []
    accessory_records = records['accessory']
    # 确保 role.accessoryid 不为空
    if role.accessoryid:
        accessoryid_list = [int(i) for i in role.accessoryid.split()]
        for accessoryid in accessoryid_list:
            for accessory_record in accessory_records:
                if accessory_record.id == accessoryid:
                    accessory.append(accessory_record)  # 使用 append 而不是 join

    # 返回玩家信息
    return {
        "name": role.name,
        "hp": role.hp,
        "item1": item1,
        "item2": item2,
        "accessory": accessory,
        "money": role.money,
        "action_point": role.action_point
    }
