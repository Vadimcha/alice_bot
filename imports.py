import random
import logging

from aiohttp import web
from aioalice import Dispatcher, get_new_configured_app, types
from aioalice.dispatcher import MemoryStorage
from aioalice.utils.helper import Helper, HelperMode, ItemsList, Item

from datetime import timedelta, datetime

WEBHOOK_URL_PATH = ''  # webhook endpoint

WEBAPP_HOST = 'localhost'
WEBAPP_PORT = 5000

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s', level=logging.INFO)

# Создаем экземпляр диспетчера и подключаем хранилище в памяти
dp = Dispatcher(storage=MemoryStorage())