# class
from typing import List


class DistStationTideListMidModel:
    """
        + 23-08-14 配合其他系统获取不同站点的天文潮及时间集合
        serializer 对应 :DistStationTideListSerializer
    """

    def __init__(self, code: str, tide_list: List[float], forecast_ts_list: List[int]):
        self.station_code = code
        self.tide_list = tide_list
        self.forecast_ts_list = forecast_ts_list
