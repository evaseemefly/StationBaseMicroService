import arrow
import requests
import json
from typing import List, Type, Any, Optional, Dict
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request

from dao.fub import FubBaseDao
from schema.fub import FubBaseInfoSchema
from schema.station_surge import AstronomicTideSchema
from schema.station import StationBaseInfoSchema, DistStationTideSchema, StationAlertSchema
from config.consul_config import CONSUL_HOST, CONSUL_PORT
from util.consul_client import ConsulRegisterServer
from dao.station import StationBaseDao, AstronomicTideDao, AlertDao
# 日志装饰器
from util.request_log import request_log_decorator, request_timer_consuming_decorator

app = APIRouter()


@app.get('/dist/codes', response_model=List[str],

         summary="获取所有fub的codes")
@request_log_decorator
@request_timer_consuming_decorator
async def get_dist_fubs_codes(request: Request):
    dao = FubBaseDao()
    codes = dao.get_dist_fub_codes()

    return list(codes)


@app.get('/all/info', response_model=List[FubBaseInfoSchema],

         summary="获取所有fub info list")
@request_log_decorator
@request_timer_consuming_decorator
async def get_all_fubs(request: Request):
    dao = FubBaseDao()
    res = dao.get_all_fubinfo_list()

    return res
