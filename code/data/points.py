import sqlalchemy
from .db_session import SqlAlchemyBase


# ТАБЛИЦА POINTS:
#     id (id метки)
#     type (описание метки)
#     image_point (картинка метки) #может не ввестись


class Point(SqlAlchemyBase):
    __tablename__ = 'points'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    type = sqlalchemy.Column(sqlalchemy.String)
    name_point = sqlalchemy.Column(sqlalchemy.String)
    image_point = sqlalchemy.Column(sqlalchemy.BLOB)
