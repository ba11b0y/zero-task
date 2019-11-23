import os
import cherrypy
import redis

redis_conn = redis.Redis(host='172.23.0.2', port=6379)


conf = {
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.root': os.path.abspath(os.getcwd()),
        'tools.staticdir.dir': 'static'
    }
}
