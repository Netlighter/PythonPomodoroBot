import os


TOKEN = os.environ.get('TOKEN')

PROXY_URL = os.environ.get('PROXY_URL')

DB_KWARGS = {'db': 'bot_mongodb', 'host': os.environ.get('MONGODB_URI')}
