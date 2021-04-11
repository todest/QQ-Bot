import configparser
import os

from app.util.tools import app_path


class Config:
    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.cf.read(os.sep.join([app_path(), 'core', 'config.ini']))

        self.LOGIN_HOST = self.cf.get('bot', 'login_host')
        self.LOGIN_PORT = self.cf.get('bot', 'login_port')
        self.LOGIN_QQ = self.cf.get('bot', 'login_qq')
        self.AUTH_KEY = self.cf.get('bot', 'auth_key')
        self.DEBUG = True if self.cf.get('bot', 'debug').lower() == 'true' else False
        self.ONLINE = True if self.cf.get('bot', 'online').lower() == 'true' else False

        self.MYSQL_USER = self.cf.get('mysql', 'mysql_user')
        self.MYSQL_PWD = self.cf.get('mysql', 'mysql_pwd')
        self.MYSQL_DATABASE = self.cf.get('mysql', 'mysql_database')

        self.APP_ID = self.cf.get('tencent_api', 'app_id')
        self.APP_KEY = self.cf.get('tencent_api', 'app_key')

    def change_debug(self):
        if not self.ONLINE:
            return
        if self.DEBUG:
            self.cf.set('bot', 'debug', 'false')
            self.DEBUG = False
        else:
            self.cf.set('bot', 'debug', 'true')
            self.DEBUG = True
        with open(os.sep.join([app_path(), 'core', 'config.ini']), 'w+')as fb:
            self.cf.write(fb)
