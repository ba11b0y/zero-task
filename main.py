import cherrypy
from conf import conf, redis_conn
from redis_helpers import search_by_name, get_scrip_details, order_by_num_of_trades, parse_csv_and_seed
from fetch_and_save import convert_helper
import os


class SearchService(object):

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self, query):
        results = search_by_name(query)
        return {"res": results}


class ScripDetails(object):

    exposed = True

    @cherrypy.tools.json_out()
    def GET(self, scrip_name):
        results = convert_helper(get_scrip_details(scrip_name))
        return {"res": results}


class FetchTopTen(object):

    exposed = True

    @cherrypy.tools.json_out()
    def GET(self):
        if not redis_conn.exists("last_sync"):
            parse_csv_and_seed()
        results = order_by_num_of_trades()
        json_res = {}
        for res in results:
            json_res[res] = convert_helper(get_scrip_details(res))
        return json_res


class Root(object):

    @cherrypy.expose
    def index(self):
        return open("index.html")


if __name__ == "__main__":

    cherrypy.tree.mount(SearchService(), '/search')
    cherrypy.tree.mount(Root(), '/', conf)
    cherrypy.tree.mount(ScripDetails(), '/details',
                        {'/':
                         {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
                         }
                        )
    cherrypy.tree.mount(FetchTopTen(), '/fetch',
                        {'/':
                         {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
                         }
                        )
    cherrypy.config.update(
        {'server.socket_host': '0.0.0.0', 'server.socket_port': int(os.environ.get('PORT', 8080))})
    cherrypy.engine.start()
    cherrypy.engine.block()
