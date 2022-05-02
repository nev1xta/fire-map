import sqlalchemy
from .db_session import SqlAlchemyBase


# ТАБЛИЦА POSITION:
#     id
#     name_position (название должности)
#     # координаты карты
#     x0 (левой верхней)
#     y0 (левой верхней)
#     x1 (правой нижней)
#     y1 (правой нижней)
#     complited (закончена ли работа)

class Position(SqlAlchemyBase):
    __tablename__ = 'positions'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name_position = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('users.name_position'))
    x0 = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    y0 = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    x1 = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    y1 = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    complited = sqlalchemy.Column(sqlalchemy.Integer, default=0)
