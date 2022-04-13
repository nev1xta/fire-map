import sqlalchemy
from .db_session import SqlAlchemyBase


# ТАБЛИЦА POINTS_ON_MAPS:
#     point_id (id метки, внешний ключ из таблицы POINTS)
#     position_id (id должности из таблицы POSITION)
#     # координаты меток
#     x0 координата метки
#     y0 координата метки
#     x1 координата метки (если это не точка) # не обязательное
#     y1 координата метки (если это не точка) # не обязательное


class Point_On_Map(SqlAlchemyBase):
    __tablename__ = 'points_on_maps'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    point_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('points.id'))
    position_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('positions.id'))
    x0 = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    y0 = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    x1 = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    y1 = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
