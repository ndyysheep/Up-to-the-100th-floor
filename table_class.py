from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import declarative_base, sessionmaker


def create_class_for_table(table_name, metadata, engine):
    Base = declarative_base()
    table = Table(table_name, metadata, autoload_with=engine)
    # 显式设置 __tablename__
    return type(table_name, (Base,), {'__table__': table, '__tablename__': table_name})
def pull():
    engine = create_engine('postgresql+psycopg2://ztq:ztqnb123@47.113.185.205:5432/db', echo=False)
    metadata = MetaData()
    metadata.reflect(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    table_records = {}
    table_names = ['item', 'accessory', 'behavior', 'shop', 'users', 'role', 'terrain', 'floor', 'monsterlocation', 'monster']

    for table_name in table_names:
        if table_name in metadata.tables:
            cls = create_class_for_table(table_name, metadata, engine)
            records = session.query(cls).all()
            table_records[table_name] = records

    session.close()  # 关闭会话
    print("读取存档成功")
    return table_records

def push(table_records):
    engine = create_engine('postgresql+psycopg2://ztq:ztqnb123@47.113.185.205:5432/db', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        for table_name, records in table_records.items():
            for record in records:
                session.add(record)  # 将修改后的记录添加到会话中
        session.commit()  # 提交更改
        print("所有修改已成功保存到数据库")
    except Exception as e:
        session.rollback()  # 如果出现异常，回滚更改
        print(f"保存修改时出错: {e}")
    finally:
        session.close()  # 关闭会话

def delete_role(role_id):
    engine = create_engine('postgresql+psycopg2://ztq:ztqnb123@47.113.185.205:5432/db', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # 假设 'role' 表对应的类名为 Role
        metadata = MetaData()
        metadata.reflect(bind=engine)
        Role = create_class_for_table('role', metadata, engine)

        # 查询出对应 ID 的角色
        role_to_delete = session.query(Role).filter(Role.id == role_id).first()

        if role_to_delete:
            session.delete(role_to_delete)  # 删除角色
            session.commit()  # 提交更改
            print(f"角色 {role_id} 已从数据库中删除")
        else:
            print(f"未找到 ID 为 {role_id} 的角色")
    except Exception as e:
        session.rollback()  # 如果出现异常，回滚更改
        print(f"删除角色时出错: {e}")
    finally:
        session.close()  # 关闭会话
