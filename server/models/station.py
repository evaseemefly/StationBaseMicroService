from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, DeclarativeBase
from sqlalchemy import String
from datetime import datetime
from arrow import Arrow
from common.default import DEFAULT_FK, UNLESS_INDEX, NONE_ID, DEFAULT_CODE, DEFAULT_PATH_TYPE, DEFAULT_PRO, \
    UNLESS_RANGE, DEFAULT_TABLE_NAME, DEFAULT_YEAR, DEFAULT_SURGE, DEFAULT_NAME, DEFAULT_COUNTRY_INDEX, DEFAULT_LATLNG

from models.base_model import BaseMeta, IIdIntModel, IDel, IForecastDt, IModel


class IForecastTime(BaseMeta):
    __abstract__ = True
    forecast_dt: Mapped[datetime] = mapped_column(default=datetime.utcnow().date())
    forecast_ts: Mapped[int] = mapped_column(default=Arrow.utcnow().int_timestamp)


class IIssueTime(BaseMeta):
    __abstract__ = True
    issue_dt: Mapped[datetime] = mapped_column(default=datetime.utcnow().date())
    issue_ts: Mapped[int] = mapped_column(default=Arrow.utcnow().int_timestamp)


class IStationSurge(BaseMeta):
    __abstract__ = True
    station_code: Mapped[str] = mapped_column(String(10), default=DEFAULT_CODE)
    surge: Mapped[float] = mapped_column(default=DEFAULT_SURGE)


class StationAstronomictideRealDataModel(IIdIntModel, IDel, IForecastDt, IStationSurge):
    """
        + 海洋站天文潮 model
    """
    __tablename__ = 'station_astronomictidee _realdata'

    gmt_created: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    gmt_modified: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class StationBaseInfoDataModel(IIdIntModel, IDel, IModel):
    __tablename__ = 'station_info'

    name: Mapped[str] = mapped_column(String(50), default=DEFAULT_NAME)
    code: Mapped[str] = mapped_column(String(50), default=DEFAULT_CODE)
    lat: Mapped[float] = mapped_column(default=DEFAULT_LATLNG)
    lon: Mapped[float] = mapped_column(default=DEFAULT_LATLNG)
    is_abs: Mapped[bool] = mapped_column(default=False)
    pid: Mapped[int] = mapped_column(default=DEFAULT_FK)
    base_level_diff: Mapped[int] = mapped_column(default=0)
    d85: Mapped[float] = mapped_column(default=0, nullable=True)
    is_in_use: Mapped[bool] = mapped_column(default=False)
    sort: Mapped[int] = mapped_column(default=-1)
    is_in_common_use: Mapped[bool] = mapped_column(default=False)
