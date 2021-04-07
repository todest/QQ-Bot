import configparser
import os

from app.util.tools import app_path

cf = configparser.ConfigParser()
cf.read(os.sep.join([app_path(), 'core', 'config.ini']))

LOGIN_HOST = cf.get('bot', 'login_host')
LOGIN_PORT = cf.get('bot', 'login_port')
LOGIN_QQ = cf.get('bot', 'login_qq')
AUTH_KEY = cf.get('bot', 'auth_key')
DEBUG = True if cf.get('bot', 'debug').lower() == 'true' else False
ONLINE = True if cf.get('bot', 'online').lower() == 'true' else False

MYSQL_USER = cf.get('mysql', 'mysql_user')
MYSQL_PWD = cf.get('mysql', 'mysql_pwd')
MYSQL_DATABASE = cf.get('mysql', 'mysql_database')

APP_ID = cf.get('tencent_api', 'app_id')
APP_KEY = cf.get('tencent_api', 'app_key')


def change_debug():
    if DEBUG:
        cf.set('bot', 'debug', 'false')
    else:
        cf.set('bot', 'debug', 'true')
    with open(os.sep.join([app_path(), 'core', 'config.ini']), 'w+')as fb:
        cf.write(fb)
