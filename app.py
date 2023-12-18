from flask import Flask, render_template, request, jsonify
import battle
from profile import get_profile_info

app = Flask(__name__)

@app.route('/')
def menu():
    player_id = 34  # 获取或计算 player_id
    monster_id = 1
    return render_template('menu.html', player_id=player_id, monster_id=monster_id)

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
