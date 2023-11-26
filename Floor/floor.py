from table_class import *

def fight(role):
    print(role.name)






records = pull()
role_records = records['role']
for role in role_records:
    if role.id == 1:
        fight(role)

push()
# item_records = records['item']
# for record in item_records:
#     if record.item_id == 1:
#         record.item_name = '木剑'
#
#     print(record.item_name)
