import os
import cherrypy
import redis

redis_conn = redis.from_url(os.environ.get("REDIS_URL"))


conf = {
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.root': os.path.abspath(os.getcwd()),
        'tools.staticdir.dir': 'static'
    }
}
