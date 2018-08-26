import logging

import mongoengine


TOKEN = ''

PROXY_URL = ''

DB_KWARGS = {'db': 'bot_mongodb'}

# XXX: If telegram.ext.CallbackQueryHandler instance created before this line
# then logs aren't working.
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

try:
    from .settings_local import *  # noqa
except ImportError:
    logging.warn("There's no local settings file, running with stock settings")

try:
    from .settings_heroku import *  # noqa
except ImportError:
    logging.warn("There's no local settings file, running with stock settings")

mongoengine.connect(**DB_KWARGS)
