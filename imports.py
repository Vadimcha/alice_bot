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


OAUTH_TOKEN = "y0_AgAAAAActKAOAAT7owAAAADgV2LrXnqbNJbVTLGOBkWB3-1OhdmazVo"
SKILL_ID = "77bdccfe-350c-4bb3-a0e7-16dcbbc59681"

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s', level=logging.INFO)

# Создаем экземпляр диспетчера и подключаем хранилище в памяти
dp = Dispatcher(skill_id=SKILL_ID, oauth_token=OAUTH_TOKEN,storage=MemoryStorage(),)
#ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
#ssl_context.load_cert_chain('cert.pem','key.pem')
