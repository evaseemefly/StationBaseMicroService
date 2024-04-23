from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, DeclarativeBase
from sqlalchemy import String
from datetime import datetime
from arrow import Arrow
from common.default import DEFAULT_FK, UNLESS_INDEX, NONE_ID, DEFAULT_CODE, DEFAULT_PATH_TYPE, DEFAULT_PRO, \
    UNLESS_RANGE, DEFAULT_TABLE_NAME, DEFAULT_YEAR, DEFAULT_SURGE, DEFAULT_NAME, DEFAULT_COUNTRY_INDEX, DEFAULT_LATLNG

from models.base_model import BaseMeta, IIdIntModel, IDel, IForecastDt, IModel


class FubBaseInfoModel(IIdIntModel, IDel, IModel):
    __tablename__ = 'fub_info'

    name: Mapped[str] = mapped_column(String(50), default=DEFAULT_NAME)
    code: Mapped[str] = mapped_column(String(50), default=DEFAULT_CODE)
    lat: Mapped[float] = mapped_column(default=DEFAULT_LATLNG)
    lon: Mapped[float] = mapped_column(default=DEFAULT_LATLNG)
    sort: Mapped[int] = mapped_column(default=-1)
    fub_type: Mapped[int] = mapped_column(default=-1)
    fub_kind: Mapped[int] = mapped_column(default=-1)
