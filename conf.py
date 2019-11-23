import os
import cherrypy
import redis

# Fetch REDIS_URL from heroku env config
redis_conn = redis.from_url(os.environ.get("REDIS_URL"))

GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google-chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

conf = {
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.root': os.path.abspath(os.getcwd()),
        'tools.staticdir.dir': 'static'
    }
}
