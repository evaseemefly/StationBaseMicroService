import json
import requests
from typing import List, Optional, Any, Dict

from sqlalchemy import distinct, select, func, and_, text
from sqlalchemy.orm import aliased
from sqlalchemy import select, within_group, distinct
import arrow
from config.store_config import StoreConfig
from mid_model.station import DistStationTideListMidModel
from models.station import StationAstronomictideRealDataModel, StationBaseInfoDataModel, StationAlertModel
from schema.station import StationRegionSchema
from schema.station_surge import SurgeRealDataSchema, AstronomicTideSchema, StationTotalSurgeSchema, \
    DistStationTotalSurgeSchema, StationSurgeListSchema, DistStationSurgeListSchema, DistStationTideListSchema
from dao.base import BaseDao
from common.enums import CoverageTypeEnum, ForecastProductTypeEnum


class StationBaseDao(BaseDao):
    """
        站点基础信息 dao (访问台风预报系统)
    """

    def get_dist_station_code(self, **kwargs) -> set:
        """
            获取不同的站点 code set
        @param kwargs:
        @return:
        """
        target_url: str = f'http://128.5.10.21:8000/station/station/all/list'
        res = requests.get(target_url)
        res_content: str = res.content.decode('utf-8')
        # [{'id': 4, 'code': 'SHW', 'name': '汕尾', 'lat': 22.7564, 'lon': 115.3572, 'is_abs': False, 'sort': -1,
        #  'is_in_common_use': True}]
        list_region_dict: List[Dict] = json.loads(res_content)
        list_region: List[StationRegionSchema] = []
        for region_dict in list_region_dict:
            list_region.append(StationRegionSchema.parse_obj(region_dict))
        # 针对code 进行去重操作
        list_codes: List[str] = [station.code for station in list_region]
        return set(list_codes)

    def get_dist_region(self, **kwargs) -> List[str]:
        """
            获取不同的行政区划 code
        @param kwargs:
        @return:
        """

    def get_target_astronomictide(self, code: str, start_ts: int, end_ts: int) -> List[AstronomicTideSchema]:
        """
            获取指定站点的天文潮
            step1: 获取指定站点的 [start,end] 范围内的天文潮集合(间隔1h)
        @param code: 站点
        @param start_ts: 起始时间戳
        @param end_ts: 结束时间戳
        @return:
        """
        target_url: str = f'http://128.5.10.21:8000/station/station/astronomictide/list'
        start_arrow: arrow.Arrow = arrow.get(start_ts)
        end_arrow: arrow.Arrow = arrow.get(end_ts)
        start_dt_str: str = f"{start_arrow.format('YYYY-MM-DDTHH:mm:ss')}Z"
        end_dt_str: str = f"{end_arrow.format('YYYY-MM-DDTHH:mm:ss')}Z"
        # 注意时间格式 2023-07-31T16:00:00Z
        # res = requests.get(target_url,
        #                    data={'station_code': code, 'start_dt': start_dt_str, 'end_dt': end_dt_str})
        res = requests.get(target_url,
                           params={'station_code': code, 'start_dt': start_dt_str, 'end_dt': end_dt_str})
        res_content: str = res.content.decode('utf-8')
        # {'station_code': 'CGM', 'forecast_dt': '2023-07-31T17:00:00Z', 'surge': 441.0}
        # 天文潮字典集合
        list_tide_dict: List[Dict] = json.loads(res_content)
        # 天文潮 schema 集合
        list_tide: List[AstronomicTideSchema] = []
        for tide_dict in list_tide_dict:
            list_tide.append(AstronomicTideSchema.parse_obj(tide_dict))
        return list_tide

    def get_dist_station_tide_list(self, start_ts: int, end_ts: int) -> List[DistStationTideListSchema]:
        """
            + 23-08-16
            获取所有站点 [start,end] 范围内的 天文潮+时间 集合
        @param start_ts:
        @param end_ts:
        @return:
        """
        target_url: str = f'http://128.5.10.21:8000/station/station/dist/astronomictide/list'
        start_arrow: arrow.Arrow = arrow.get(start_ts)
        end_arrow: arrow.Arrow = arrow.get(end_ts)
        start_dt_str: str = f"{start_arrow.format('YYYY-MM-DDTHH:mm:ss')}Z"
        end_dt_str: str = f"{end_arrow.format('YYYY-MM-DDTHH:mm:ss')}Z"
        # 注意时间格式 2023-07-31T16:00:00Z
        # res = requests.get(target_url,
        #                    data={'station_code': code, 'start_dt': start_dt_str, 'end_dt': end_dt_str})
        # TODO:[*] 23-10-24 此接口在高频请求后总会出现无法返回的bug
        res = requests.get(target_url,
                           params={'start_dt': start_dt_str, 'end_dt': end_dt_str})
        res_content: str = res.content.decode('utf-8')
        # {'station_code': 'CGM', 'forecast_dt': '2023-07-31T17:00:00Z', 'surge': 441.0}
        # 天文潮字典集合
        list_tide_dict: List[Dict] = json.loads(res_content)
        list_tide: List[DistStationTideListSchema] = []
        for temp in list_tide_dict:
            list_tide.append(DistStationTideListSchema.parse_obj(temp))
        return list_tide

    def get_all_station(self) -> List[StationBaseInfoDataModel]:
        """
            获取全部站点
        :return:
        """
        session = self.db.session
        stmt = select(StationBaseInfoDataModel).where(
            StationBaseInfoDataModel.is_abs == False, StationBaseInfoDataModel.is_del == False,
            StationBaseInfoDataModel.is_in_use == True)
        res = session.execute(stmt).scalars().all()
        return res


class AstronomicTideDao(BaseDao):

    def get_tide_range(self, station_code: str, start_dt: arrow.Arrow, end_dt: arrow.Arrow) -> List[
        StationAstronomictideRealDataModel]:
        session = self.db.session
        """
            SELECT "station_astronomictidee _realdata".gmt_created, "station_astronomictidee _realdata".gmt_modified, "station_astronomictidee _realdata".id,
             "station_astronomictidee _realdata".is_del,
              "station_astronomictidee _realdata".forecast_dt, 
              "station_astronomictidee _realdata".station_code, 
              "station_astronomictidee _realdata".surge 
            FROM "station_astronomictidee _realdata" 
            WHERE "station_astronomictidee _realdata".station_code = :station_code_1 
            AND "station_astronomictidee _realdata".forecast_dt >= :forecast_dt_1 
            AND "station_astronomictidee _realdata".forecast_dt <= :forecast_dt_2 
            ORDER BY "station_astronomictidee _realdata".forecast_dt
        """
        # TODO:[*] 23-11-16 使用此种方式不行
        stmt = select(StationAstronomictideRealDataModel).where(
            StationAstronomictideRealDataModel.station_code == station_code,
            StationAstronomictideRealDataModel.forecast_dt >= start_dt.datetime,
            StationAstronomictideRealDataModel.forecast_dt <= end_dt.datetime).order_by(
            StationAstronomictideRealDataModel.forecast_dt)
        # 结果为 { Row:1}
        # 注意 .scalars()后需要再 .all()
        res = session.execute(stmt).scalars().all()
        # list_res = list(res)
        # list(res_stmt)
        #
        # query = session.query(StationAstronomictideRealDataModel).filter(
        #     StationAstronomictideRealDataModel.station_code == station_code,
        #     StationAstronomictideRealDataModel.forecast_dt >= start_dt.datetime,
        #     StationAstronomictideRealDataModel.forecast_dt <= end_dt.datetime).order_by(
        #     StationAstronomictideRealDataModel.forecast_dt)
        # # 方式2 执行后的结果每一个都是 StationAstronomictideRealDataModel
        # res = query.all()
        return res

    def get_dist_tide_range(self, start_dt: arrow.Arrow, end_dt: arrow.Arrow) -> List[DistStationTideListMidModel]:
        """
            获取所有站点的起止时间范围内的天文潮集合
        :param start_dt:
        :param end_dt:
        :return:
        """
        session = self.db.session
        # TODO:[*] 23-08-28 此处加入黄骅的单站测试，待删除
        query_sql: str = text(f"""SELECT station_code,
                group_concat(unix_timestamp(forecast_dt)  order by forecast_dt) as forecastdt_list,
                group_concat(surge  order by forecast_dt) as surge_list
                FROM `station_astronomictidee _realdata`
                WHERE forecast_dt>='{start_dt.datetime}' AND forecast_dt<='{end_dt.datetime}'  group by station_code""")

        """
            SELECT station_code ,
               group_concat(forecast_dt order by forecast_dt ) as forecastdt_list,
               group_concat(surge order by forecast_dt) as surge_list
            FROM `station_astronomictidee _realdata`
            WHERE forecast_dt>='2023-08-27 12:00:00+00:00' AND forecast_dt<='2023-09-03 12:00:00+00:00'
            group by station_code
        """
        res = session.execute(query_sql).all()
        # ERROR: 'Raw query must include the primary key'
        # 设定 DistStationTideRealDataModel 的 station_code 为 主键
        dist_station_tide_list: List[DistStationTideListMidModel] = []
        for temp in res:
            # 1- 站点代号
            temp_code: str = temp.station_code
            temp_tide_str_list: List[str] = temp.surge_list.split(',')
            # 2- 天文潮集合
            temp_tide_list: List[float] = []
            for temp_tide_str in temp_tide_str_list:
                if temp_tide_str != '':
                    temp_tide_list.append(float(temp_tide_str))

            temp_dt_str_list: List[str] = temp.forecastdt_list.split(',')
            # 3- 预报时间戳集合
            temp_ts_list: List[int] = []
            for temp_dt_str in temp_dt_str_list:
                if temp_dt_str != '':
                    # '2023-08-01 04:00:00.000000'
                    # 1690862400.000000
                    temp_ts_list.append(int(float(temp_dt_str)))
            temp_tide_middelmodel: DistStationTideListMidModel = DistStationTideListMidModel(code=temp_code,
                                                                                             tide_list=temp_tide_list,
                                                                                             forecast_ts_list=temp_ts_list)
            dist_station_tide_list.append(temp_tide_middelmodel)
        return dist_station_tide_list


class AlertDao(BaseDao):
    """
        + 23-11-17 加入的警戒潮位 dao
    """

    def get_station_alert(self, station_code: str) -> List[StationAlertModel]:
        """
            获取指定站点的警戒潮位集合
        :param station_code:
        :return:
        """
        session = self.db.session
        stmt = select(StationAlertModel).where(StationAlertModel.station_code == station_code)
        res = session.execute(stmt).scalars().all()
        return res

    def get_dist_station_alert(self) -> List[Dict]:
        """
            + 23-11-17 获取所有站点的警戒潮位集合
        :return:
        """
        session = self.db.session
        sql_raw: str = text(f"""
                    SELECT station_code,group_concat(tide) as tide_list,group_concat(alert) as alert_list
                    FROM station_stationalerttidemodel
                    group by station_code
                """)
        res = session.execute(sql_raw).all()
        dist_station_alert_list: List[dict] = []
        for temp in res:
            temp_code: str = temp.station_code
            temp_alert_tide: List[int] = []
            temp_alert_level: List[int] = []
            if temp.tide_list is not None:
                temp_tide_str: List[str] = temp.tide_list.split(',')
                temp_alert_tide = [float(tide) for tide in temp_tide_str]
                temp_alert_tide.sort()
            if temp.alert_list is not None:
                temp_alert_str: List[str] = temp.alert_list.split(',')
                temp_alert_level = [int(alert) for alert in temp_alert_str]
                temp_alert_level.sort()
            temp_station_alert_dict: dict = {
                'station_code': temp_code,
                'alert_tide_list': temp_alert_tide,
                'alert_level_list': temp_alert_level
            }
            dist_station_alert_list.append(temp_station_alert_dict)
        return dist_station_alert_list
