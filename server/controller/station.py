import arrow
import requests
import json
from typing import List, Type, Any, Optional, Dict
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from schema.station_surge import AstronomicTideSchema
from schema.station import StationBaseInfoSchema, DistStationTideSchema, StationAlertSchema
from config.consul_config import CONSUL_HOST, CONSUL_PORT
from util.consul_client import ConsulRegisterServer
from dao.station import StationBaseDao, AstronomicTideDao, AlertDao
# 日志装饰器
from util.request_log import request_log_decorator

app = APIRouter()

SERVICE_NAME: str = 'station-base'


@app.on_event("startup")
def startup_event():
    """
        本控制器组件启动时向consul注册本服务
    :return:
    """
    server = ConsulRegisterServer('128.5.9.79', 8088, CONSUL_HOST, CONSUL_PORT, SERVICE_NAME)
    server.register()
    pass


@app.get('/tide/range', response_model=List[AstronomicTideSchema],
         response_model_include=['station_code', 'forecast_dt', 'surge', ],
         summary="获取指定时间范围的天文潮集合")
@request_log_decorator
async def get_tide_range(station_code: str, start_dt: str, end_dt: str, request: Request):
    start_arrow: arrow.Arrow = arrow.get(start_dt)
    end_arrow: arrow.Arrow = arrow.get(end_dt)
    tide_dao = AstronomicTideDao()
    res_query = tide_dao.get_tide_range(station_code, start_arrow, end_arrow)
    res_list = list(res_query)
    return list(res_list)


@app.get('/dist/astronomictide/list', response_model=List[DistStationTideSchema],
         response_model_include=['station_code', 'tide_list', 'forecast_ts_list', ],
         summary="获取所有站点的起止时间内的天文潮集合")
@request_log_decorator
async def get_dist_station_tide_range(start_dt: str, end_dt: str, request: Request):
    start_arrow: arrow.Arrow = arrow.get(start_dt)
    end_arrow: arrow.Arrow = arrow.get(end_dt)
    tide_dao = AstronomicTideDao()
    res_query = tide_dao.get_dist_tide_range(start_arrow, end_arrow)
    res_list = list(res_query)
    return list(res_list)


@app.get('/astronomictide/list', response_model=List[AstronomicTideSchema],
         response_model_include=['station_code', 'forecast_dt', 'surge', ],
         summary="获取指定站点的起止时间内的天文潮集合")
@request_log_decorator
async def get_target_station_tide_range(station_code: str, start_dt: str, end_dt: str, request: Request):
    start_arrow: arrow.Arrow = arrow.get(start_dt)
    end_arrow: arrow.Arrow = arrow.get(end_dt)
    tide_dao = AstronomicTideDao()
    res_query = tide_dao.get_tide_range(station_code, start_arrow, end_arrow)
    res_list = list(res_query)
    return list(res_list)


@app.get('/all/list', response_model=List[StationBaseInfoSchema],
         response_model_include=['id', 'name', 'code', 'lat', 'lon', 'is_abs', 'pid', 'base_level_diff', 'd85',
                                 'is_in_use', 'sort', 'is_in_common_use'],
         summary="获取所有in use 的站点")
@request_log_decorator
async def get_all_station(request: Request):
    station_dao = StationBaseDao()
    res_list = station_dao.get_all_station()
    return res_list


@app.get('/alert', response_model=List[StationAlertSchema],
         response_model_include=['station_code', 'tide', 'alert'],
         summary="获取指定站点的警戒潮位集合")
@request_log_decorator
async def get_target_station_alert(station_code: str, request: Request):
    alert_dao = AlertDao()
    res = alert_dao.get_station_alert(station_code)
    return res


@app.get('/dist/alert', response_model=List[Dict],
         response_model_include=['station_code', 'alert_tide_list', 'alert_level_list'],
         summary="获取所有站点的警戒潮位集合")
@request_log_decorator
async def get_target_station_alert(request: Request):
    alert_dao = AlertDao()
    res = alert_dao.get_dist_station_alert()
    return res


@app.get('/test', summary="station-test")
@request_log_decorator
async def get_test(name: str, request: Request):
    return 'test'
