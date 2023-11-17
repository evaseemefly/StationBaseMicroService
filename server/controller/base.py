import arrow
import requests
import json
from typing import List, Type, Any, Optional, Dict
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from schema.station_surge import AstronomicTideSchema
from schema.station import StationBaseInfoSchema, DistStationTideSchema

from dao.station import StationBaseDao, AstronomicTideDao

app = APIRouter()
