# from config.consul_config import CONSUL_OPTIONS
import urllib.parse
from config.consul_config import consul_config

# from util.consul import ConsulConfigClient

# CONSUL_HOST: str = CONSUL_OPTIONS.get('SERVER').get('HOST')
# CONSUL_PORT: int = CONSUL_OPTIONS.get('SERVER').get('PORT')
# consul_config = ConsulConfigClient(CONSUL_HOST, CONSUL_PORT)

# 温带风暴潮数据库配置
# 本地测试
# CONSUL_DB_CONFIG = consul_config.get_consul_kv('wd_db_config_local')
CONSUL_DB_CONFIG = consul_config.get_consul_kv('station_base_config')


class DBConfig:
    """
    DbConfig DB配置类
    :version: 1.4
    :date: 2020-02-11
    TODO:[-] 23-06-28 此处修改为通过 consul 统一获取配置信息
    """

    driver = CONSUL_DB_CONFIG.get('driver')
    host = CONSUL_DB_CONFIG.get('host')
    # 宿主机的mysql服务
    # host = 'host.docker.internal'
    port = CONSUL_DB_CONFIG.get('port')
    username = CONSUL_DB_CONFIG.get('username')
    # 对于密码中包含 @ 等特殊字符的，需要通过此种方式将特殊字符转义
    password = urllib.parse.quote_plus(CONSUL_DB_CONFIG.get('password'))
    # password = CONSUL_DB_CONFIG.get('password')
    database = CONSUL_DB_CONFIG.get('database')
    charset = CONSUL_DB_CONFIG.get('charset')
    table_name_prefix = ''
    echo = CONSUL_DB_CONFIG.get('echo')
    pool_size = CONSUL_DB_CONFIG.get('pool_size')
    max_overflow = CONSUL_DB_CONFIG.get('max_overflow')
    pool_recycle = CONSUL_DB_CONFIG.get('pool_recycle')

    def get_url(self):
        # config = [
        #     self.driver,
        #     '://',
        #     self.username,
        #     ':',
        #     self.password,
        #     '@',
        #     self.host,
        #     ':',
        #     self.port,
        #     '/',
        #     self.database,
        #     '?charset=',
        #     self.charset,
        # ]
        # 'mysql+mysqldb://root:xxxx@128.5.10.21:3308/typhoon_forecast_db?charset=utf8mb4'
        # 'mysql+mysqldb://root:xx%40xxx@128.5.10.21:3308/typhoon_forecast_db?charset=utf8mb4'
        connect_str: str = f"{self.driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}?charset={self.charset}"
        # return ''.join(config)
        return connect_str
