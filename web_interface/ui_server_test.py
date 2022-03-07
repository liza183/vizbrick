import tornado.ioloop
import tornado.web
import http
http.socket_timeout = 9999
import time
import pickle
import time
import json
import os
from  tornado.escape import json_decode
from  tornado.escape import json_encode
from tornado.concurrent import Future
from tornado import gen
from tornado.options import define, options, parse_command_line
import requests
        
REST_API_URL = 'http://localhost:8889'

class ProxyHandler(tornado.web.RequestHandler):
        
     def post(self):
        
        print("\n# Something requested to webserver proxy .. \n")
        
        # passing request to Data API server
        json_obj = json_decode(self.request.body)
        data = json_obj['data']
        url = REST_API_URL+json_obj['url']
        request_type = json_obj['request_type']

        print("REQUESTING to REST server",url,data,request_type)
        
        response_to_send = {}
        
        if request_type =="POST":
            response_to_send = requests.post(url, data=json.dumps(data))
            print("RECEIVED from REST server",response_to_send.json())
        
        else:
            print("GET REQUEST NOT SUPPORTED IN THIS VERSION")
        
        self.write(json.dumps(response_to_send.json()))

class UIMainHandler(tornado.web.RequestHandler):
    
    def get(self):
        # You may want to pass data like 
        # self.render("index.html", title="Some Title", data=json.dumps(json_data))
        self.render("index.html")

def data_api_app():
    return tornado.web.Application([
        
        (r"/proxy", ProxyHandler),
        (r"/", UIMainHandler),

    ], template_path=os.path.join(os.path.dirname(__file__), "templates"),
       static_path=os.path.join(os.path.dirname(__file__), "static"),
       xsrf_cookies=False)

if __name__ == "__main__":
    
    print ("\n# Web Server started .. now listening port 8088 ..\n")
    app = data_api_app()
    app.listen(8088)
    tornado.ioloop.IOLoop.current().start()
