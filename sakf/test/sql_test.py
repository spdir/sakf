# -*- coding: utf-8 -*-
from sakf.db.model import sql, Auth
from sqlalchemy import func

sql_engine = sql.sql_session()

# _query_data = sql_engine.query(Auth.AuthGroup).filter_by(id=1).first().url_route
# _url_id_list = [int(i) for i in _query_data.split(',') if i]
# _url_query_data = sql_engine.query(Auth.AuthUrl).filter(Auth.AuthUrl.id.in_(_url_id_list)).all()
# url_list = [url_obj.url for url_obj in _url_query_data]

# print(sql_engine.query(Auth.AuthUrl).filter_by(id=123).first())
# ff = Auth.AuthUrl.url.like("%" + 'test' + "%")

# a = sql_engine.query(func.count(Auth.AuthUrl.id)).filter(ff).scalar()
# print(a)

a = sql_engine.query(Auth.AuthGroup).filter_by(id=1).first().url_route
_url_id_list = [i for i in a.split(',') if i]
print(_url_id_list)