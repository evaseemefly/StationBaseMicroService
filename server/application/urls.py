# from controller import *
from controller.station import app as station_app

urlpatterns = [
    {"ApiRouter": station_app, "prefix": "/station", "tags": ["station"]},
]
