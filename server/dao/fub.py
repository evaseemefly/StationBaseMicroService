import json
import requests
from typing import List, Optional, Any, Dict

from sqlalchemy import distinct, select, func, and_, text
from sqlalchemy.orm import aliased
from sqlalchemy import select, within_group, distinct
import arrow
from config.store_config import StoreConfig
from mid_model.station import DistStationTideListMidModel
from models.fub import FubBaseInfoModel
from dao.base import BaseDao
from common.enums import CoverageTypeEnum, ForecastProductTypeEnum


class FubBaseDao(BaseDao):
    def get_dist_fub_codes(self, **kwargs) -> set:
        """
            获取所有fub的codes
        :param kwargs:
        :return:
        """
        session = self.db.session
        stmt = select(FubBaseInfoModel.code).where(FubBaseInfoModel.is_del == False).group_by(FubBaseInfoModel.code)
        res = session.execute(stmt).scalars().all()
        return res

    def get_all_fubinfo_list(self, **kwargs) -> List[FubBaseInfoModel]:
        session = self.db.session
        stmt = select(FubBaseInfoModel).where(FubBaseInfoModel.is_del == False).order_by(FubBaseInfoModel.sort)
        res = session.execute(stmt).scalars().all()
        return res
