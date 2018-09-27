# -*- coding: utf-8 -*-
from sakf.db.model import sql, Auth

sql_engine = sql.sql_session()


# _query_data = sql_engine.query(Auth.AuthGroup).filter_by(id=1).first().url_route
# _url_id_list = [int(i) for i in _query_data.split(',') if i]
# _url_query_data = sql_engine.query(Auth.AuthUrl).filter(Auth.AuthUrl.id.in_(_url_id_list)).all()
# url_list = [url_obj.url for url_obj in _url_query_data]

print(sql_engine.query(Auth.AuthUrl).filter_by(id=123).first())
