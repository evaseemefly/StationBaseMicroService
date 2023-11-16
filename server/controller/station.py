import arrow
import requests
import json
from typing import List, Type, Any, Optional, Dict
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from schema.station_surge import AstronomicTideSchema
from schema.station import StationBaseInfoSchema, DistStationTideSchema
from models.station import StationForecastRealDataModel
from config.consul_config import consul_agent
from dao.station import StationBaseDao, AstronomicTideDao

app = APIRouter()


@app.get('/tide/range', response_model=List[AstronomicTideSchema],
         response_model_include=['station_code', 'forecast_dt', 'surge', ],
         summary="获取指定时间范围的天文潮集合")
def get_tide_range(station_code: str, start_dt: str, end_dt: str):
    start_arrow: arrow.Arrow = arrow.get(start_dt)
    end_arrow: arrow.Arrow = arrow.get(end_dt)
    tide_dao = AstronomicTideDao()
    res_query = tide_dao.get_tide_range(station_code, start_arrow, end_arrow)
    res_list = list(res_query)
    return list(res_list)


@app.get('/dist/astronomictide/list', response_model=List[DistStationTideSchema],
         response_model_include=['station_code', 'tide_list', 'forecast_ts_list', ],
         summary="获取所有站点的起止时间内的天文潮集合")
def get_dist_station_tide_range(start_dt: str, end_dt: str):
    start_arrow: arrow.Arrow = arrow.get(start_dt)
    end_arrow: arrow.Arrow = arrow.get(end_dt)
    tide_dao = AstronomicTideDao()
    res_query = tide_dao.get_dist_tide_range(start_arrow, end_arrow)
    res_list = list(res_query)
    return list(res_list)


@app.get('/all/list', response_model=List[StationBaseInfoSchema],
         response_model_include=['id', 'name', 'code', 'lat', 'lon', 'is_abs', 'pid', 'base_level_diff', 'd85',
                                 'is_in_use', 'sort', 'is_in_common_use'],
         summary="获取所有in use 的站点")
def get_all_station():
    station_dao = StationBaseDao()
    res_list = station_dao.get_all_station()
    return res_list
