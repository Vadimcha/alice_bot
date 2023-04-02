import random
import logging
import random

from aiohttp import web
from aioalice import Dispatcher, get_new_configured_app, types
from aioalice.dispatcher import MemoryStorage, SkipHandler
from aioalice.utils.helper import Helper, HelperMode, ItemsList, Item
import ssl

from threading import Thread, Event
import queue
import inspect

from datetime import timedelta, datetime
import asyncio

WEBHOOK_URL_PATH = ''  # webhook endpoint

WEBAPP_HOST = '212.57.126.97'
WEBAPP_PORT = 5000

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s', level=logging.INFO)

# Создаем экземпляр диспетчера и подключаем хранилище в памяти
dp = Dispatcher(storage=MemoryStorage())
#ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
#ssl_context.load_cert_chain('cert.pem','key.pem')
