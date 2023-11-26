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

def push(modified_records):
    engine = create_engine('postgresql+psycopg2://ztq:ztqnb123@47.113.185.205:5432/db', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    """
    将修改后的记录推送（保存）到数据库。

    :param session: SQLAlchemy 会话对象
    :param modified_records: 修改后的记录列表
    """
    try:
        for record in modified_records:
            session.add(record)  # 将修改后的记录添加到会话中
        session.commit()  # 提交更改
        print("修改成功")
    except Exception as e:
        session.rollback()  # 如果出现异常，回滚更改
        raise e  # 可以选择重新抛出异常或者处理它
    finally:
        session.close()  # 无论如何，最后都关闭会话

