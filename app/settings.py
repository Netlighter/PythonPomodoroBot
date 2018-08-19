import logging


TOKEN = ''

PROXY_URL = ''

# XXX: If telegram.ext.CallbackQueryHandler instance created before this line
# then logs aren't working.
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

try:
    from .settings_local import *  # noqa
except ImportError:
    logging.warn("There's no local settings file, running with stock settings")
