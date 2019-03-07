from os import environ

PORT=environ.pop('PORT')
WORKERS=environ.pop('WORKERS')

bind='0.0.0.0:{}'.format(PORT)
workers=int(WORKERS)
application='web:app'
preload_app=True
loglevel='DEBUG'
#errorlog='.data/log/error.log'

