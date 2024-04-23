# from controller import *
from controller.station import app as station_app
from controller.fub import app as fub_app

urlpatterns = [
    {"ApiRouter": station_app, "prefix": "/station", "tags": ["station"]},
    {"ApiRouter": fub_app, "prefix": "/fub", "tags": ["fub"]},
]
