#!/usr/bin/env python3
"""
本地化轻量级数据库封装
使用SQLite + SQLAlchemy ORM
支持基础CRUD操作，通过继承BaseDao快速实现各表的Dao层
"""
import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Type, TypeVar
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func, Select, Table, MetaData, select, or_
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from skills.scripts.common.config import ConstantEnum, ApiEnum

# 基础模型类
Base = declarative_base()

# 泛型类型，用于返回对应模型实例
T = TypeVar('T', bound=Base)

meta = MetaData()

# DB_USER = "root"
# DB_PASSWORD = "root"  # 建议从环境变量读取
# DB_HOST = "192.168.1.234"
# DB_PORT = "3306"
# DB_NAME = "health-cloud"

# 关键部分：mysql+pymysql://...
DATABASE_URL = ApiEnum.DATABASE_URL

print("******=====>>>>> ge tdatabase:", DATABASE_URL)


# exit(1)


class BaseDao:
    """
    基础Dao类，提供通用的CRUD操作
    子类只需配置__model__和__tablename__即可使用
    """
    __model__: Type[T] = None  # 对应的模型类，子类必须配置
    __tablename__: str = None  # 表名，子类必须配置

    def __init__(self, db_path: str = "local.db"):
        """
        初始化Dao
        :param db_path: SQLite数据库文件路径
        """
        # if not self.__model__ or not self.__tablename__:
        #     raise NotImplementedError("子类必须配置__model__和__tablename__")

        # 创建数据库引擎
        # self.engine = create_engine(f"sqlite:///{db_path}", echo=False)

        self.engine = create_engine(
            DATABASE_URL,
            echo=False,
            pool_pre_ping=True,  # 自动重连机制，防止 MySQL 断开连接报错
            pool_size=10,  # 连接池大小
            max_overflow=30  # 允许超过 pool_size 的最大连接数
        )

        # 创建会话工厂
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        # 初始化表结构
        # self._create_tables()

    def _create_tables(self) -> None:
        """创建所有表结构"""
        Base.metadata.create_all(bind=self.engine)

    def get_session(self) -> Session:
        """获取数据库会话"""
        return self.SessionLocal()

    def create(self, **kwargs) -> T:
        """
        创建新记录
        :param kwargs: 字段键值对
        :return: 创建的模型实例
        """
        session = self.get_session()
        try:
            instance = self.__model__(**kwargs)
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return instance
        finally:
            session.close()

    def get_by_id(self, record_id: int) -> Optional[T]:
        """
        根据ID查询记录
        :param record_id: 记录ID
        :return: 模型实例或None
        """
        session = self.get_session()
        try:
            return session.query(self.__model__).filter(self.__model__.id == record_id).first()
        finally:
            session.close()

    def get_by_username(self, username: str) -> Optional[T]:
        """
        根据ID查询记录
        :param record_id: 记录ID
        :return: 模型实例或None
        """
        print("⚠️⚠️更新token⚠️⚠️", username)
        session = self.get_session()
        try:
            or_(
                self.__model__.del_flag == 0,
                self.__model__.del_flag.is_(None)  # 关键：使用 .is_(None) 来判断 SQL 的 NULL
            )
            return session.query(self.__model__).filter(self.__model__.username == username,
                                                        or_(
                                                            self.__model__.del_flag == 0,
                                                            self.__model__.del_flag.is_(None)
                                                            # 关键：使用 .is_(None) 来判断 SQL 的 NULL
                                                        )).first()
        finally:
            session.close()

    def list(self, filters: Optional[Dict[str, Any]] = None, limit: Optional[int] = None,
             offset: Optional[int] = None) -> List[T]:
        """
        查询记录列表
        :param filters: 过滤条件字典，如{"name": "张三", "age": 18}
        :param limit: 最大返回数量
        :param offset: 偏移量
        :return: 模型实例列表
        """
        session = self.get_session()
        try:
            query = session.query(self.__model__)
            # .where(self.__model__.id != 2, self.__model__.id == 1))

            if filters:
                for key, value in filters.items():
                    query = query.filter(getattr(self.__model__, key) == value)

            if offset:
                query = query.offset(offset)
            if limit:
                query = query.limit(limit)

            return query.all()
        finally:
            session.close()

    def update(self, record_id: int, **kwargs) -> Optional[T]:
        """
        更新记录
        :param record_id: 记录ID
        :param kwargs: 要更新的字段键值对
        :return: 更新后的模型实例或None
        """
        session = self.get_session()
        try:
            instance = session.query(self.__model__).filter(self.__model__.id == record_id).first()
            if not instance:
                return None

            for key, value in kwargs.items():
                setattr(instance, key, value)

            session.commit()
            session.refresh(instance)
            return instance
        finally:
            session.close()

    def update_by_username(self, username: str, **kwargs) -> Optional[T]:
        """
        更新记录
        :param username: 记录ID
        :param kwargs: 要更新的字段键值对
        :return: 更新后的模型实例或None
        """
        session = self.get_session()
        try:
            instance = session.query(self.__model__).filter(self.__model__.username == username).first()
            if not instance:
                return None

            for key, value in kwargs.items():
                setattr(instance, key, value)

            session.commit()
            session.refresh(instance)
            return instance
        finally:
            session.close()

    def delete(self, record_id: int) -> bool:
        """
        删除记录
        :param record_id: 记录ID
        :return: 删除成功返回True，失败返回False
        """
        session = self.get_session()
        try:
            instance = session.query(self.__model__).filter(self.__model__.id == record_id).first()
            if not instance:
                return False

            session.delete(instance)
            session.commit()
            return True
        finally:
            session.close()

    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        统计记录数量
        :param filters: 过滤条件字典
        :return: 记录数量
        """
        session = self.get_session()
        try:
            query = session.query(func.count(self.__model__.id))

            if filters:
                for key, value in filters.items():
                    query = query.filter(getattr(self.__model__, key) == value)

            return query.scalar()
        finally:
            session.close()


# ------------------------------
# 示例：定义User模型和UserDao
# ------------------------------

class User(Base):
    """用户模型"""
    __tablename__ = "sys_user"

    id = Column(String(32), primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False, comment="用户名")
    email = Column(String(45), unique=True, index=True, comment="邮箱")
    birthday = Column(DateTime, unique=True, index=True, comment="邮箱")
    sex = Column(Integer, comment="性别")
    token = Column(String(500), comment="token")
    open_token = Column(String(1000), comment="开放token")
    source = Column(String(50), comment="token")
    del_flag = Column(Integer, comment="是否删除", default=0)
    create_time = Column(DateTime, default=func.now(), comment="创建时间")
    update_time = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")

    # class SourceEnum(Enum):
    #     ARK_CLAW = "ARK_CLAW"
    #     FEISHU = "FEISHU"
    #     COZE = "COZE"
    #     JVS_CLAW = "JVS_CLAW"
    #     WUHONG = "WUHONG"
    #     LIGHT_HOUSE = "LIGHT_HOUSE"
    #     SKILL_HUB = "SKILL_HUB"
    #     CLAW_HUB = "CLAW_HUB"


class UserDao(BaseDao):
    """用户Dao，继承BaseDao即可拥有所有基础CRUD功能"""
    __model__ = User
    __tablename__ = "users"


def demo():
    print("=== 本地化轻量级数据库演示 ===")

    # 初始化Dao
    user_dao = UserDao()
    # article_dao = ArticleDao()

    # 1. 创建用户
    print("\n1. 创建用户:")
    try:
        user = user_dao.create(
            id=int(datetime.datetime.now().timestamp()),
            username="zhangsan" + str(datetime.datetime.now().second),
            email="zhangsan@example.com" + str(datetime.datetime.now().second),
            sex=1
        )
        print(f"创建成功: ID={user.id}, 用户名={user.username}, 邮箱={user.email}")
    except Exception as e:
        print(e)

    users = user_dao.list(offset=0, limit=15)
    print("aaaaaaaa*****+====>>>> get foundUser .0000:", len(users), "user.id", type(users))
    for userx in users:
        print("*****+====>>>> get foundUser .0000 and ujser:", userx, "_userNmae:", userx.username,
              "__and create_time:",
              userx.create_time, "user.id", userx.id,
              "user:", type(userx))

    user0 = users[0]

    # 2. 根据ID查询用户
    print("\n100. 查询用户-byname:")
    found_user = user_dao.get_by_username("zhangsan38")
    print("*****+====>>>> get foundUser and user Iname:", found_user, "user.id", user.id, "__userName:", user.username,
          "__found_user:", found_user.username, found_user.token[:20], found_user.open_token[:20])

    print("\n2. 查询用户:")
    found_user = user_dao.get_by_id(user.id)
    print("*****+====>>>> get foundUser:", found_user, "user.id", user.id)

    print("\n3. 查询用户:")
    # userm = Table("user", meta)
    # userm = Table("users", meta, autoload_with=user_dao.engine)
    userm = Table("sys_user", meta, autoload_with=user_dao.engine)
    print("%%%%%%%%%*****+====>>>> get foundUser 33333 and :", userm, "user.id", user.id, ", userx.id", userx.id)
    found_user = Select(userm.c.id, userm.c.username, userm.c.email).where(userm.c.id == user.id,
                                                                           userm.c.username != "lisi")
    with user_dao.engine.connect() as conn:
        res = conn.execute(found_user)
        users = res.scalars().all()
        for row in res:
            print("********* ========= >>>> get in ro row", row, "typeof", type(row), "value==>>>", *row)
        print("&&&&&&&&&&~~~~~~~#####~~~~*****+====>>>> get foundUser 33333 and result ******=====>>>>>>>>>:", res,
              "found_user",
              found_user, "lenof(####)", len(users),
              "__users:", type(users))
    print("*****+====>>>> get foundUser 33333aa121:", found_user, "user.id", user.id)
    # if found_user:
    #     print(f"查询成功 foudn User: {found_user.username}, 年龄={found_user.age}")

    stmt = Select(User).where(User.id == user.id, User.username != "lisi")
    print(f"aaaaa=====>>>>>> bbbb 查询成功4561521 foudn User and othe r : {stmt}", stmt)

    with Session(user_dao.engine) as session:
        newresult = session.execute(stmt)
        found_userss = newresult.scalars().all()

        print(
            f"%%%%%%%%%====######=>>>?aaaaa=====>>>>>> aaaaaaa查询成功4561521 foudn User and othe r:newresult and result:",
            newresult,
            "_found_userss", len(found_userss), found_userss[0].username)

    # 3. 更新用户
    print("\n3. 更新用户:")
    updated_user = user_dao.update(user.id, sex=2, email="zhangsan_new@example.com")
    if updated_user:
        print(f"更新成功: 年龄={updated_user.sex}, 邮箱={updated_user.email}")

    # 4. 创建多个用户
    # print("\n4. 批量创建用户:")
    # user_dao.create(username="lisi", email="lisi@example.com", age=30)
    # user_dao.create(username="wangwu", email="wangwu@example.com", age=28)

    # 5. 查询所有用户
    print("\n5. 查询所有用户:")
    all_users = user_dao.list()
    print("******+===>>> geall user:", all_users)
    for u in all_users:
        print(f"ID={u.id}, 用户名={u.username}, 年龄={u.sex}, 创建时间={u.created_time}")

    # 6. 条件查询
    print("\n6. 条件查询（年龄>25）:")
    filtered_users = user_dao.list(filters={"sex": 26})  # 简单等值查询
    for u in filtered_users:
        print(f"ID={u.id}, 用户名={u.username}, 年龄={u.sex}")

    # 7. 统计用户数量
    print("\n7. 用户总数:", user_dao.count())

    # 8. 删除用户
    print("\n8. 删除用户:")
    delete_success = user_dao.delete(user.id)
    print(f"删除用户ID={user.id} 成功: {delete_success}")
    print("删除后用户总数:", user_dao.count())

    # 9. 文章操作演示
    # print("\n9. 文章操作演示:")
    # article = article_dao.create(
    #     title="SQLAlchemy使用教程",
    #     content="这是一篇关于SQLAlchemy的使用教程...",
    #     author_id=2  # 对应lisi的ID
    # )
    # print(f"创建文章成功: ID={article.id}, 标题={article.title}")

    print("\n=== 演示完成 ===")


if __name__ == "__main__":
    # 安装依赖: pip install sqlalchemy
    demo()
