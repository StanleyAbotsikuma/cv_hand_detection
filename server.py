import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.websocket as ws
from tornado.options import define, options
import json
import time

active_clients = set()
active_clients_name = []


def disconnect(target):
    index = 0
    a = ""
    for i in active_clients:
        if i == target:
            # print(i)
            # print(index)
            a = active_clients_name[index]
            del active_clients_name[index]
        else:
            index = index + 1
    active_clients.remove(target)
    return a


define('port', default=4041, help='port to listen on')


class web_socket_handler(ws.WebSocketHandler):
    '''This class handles the websocket channel'''
    @classmethod
    def route_urls(cls):
        return [(r'/', cls, {}), ]

    def simple_init(self):
        self.last = time.time()
        self.stop = False

    def open(self):
        '''client opens a connection'''
        # self.simple_init()

        active_clients.add(self)
        # active_clients_name.append("self")
        # print("New client connected")
        # self.write_message("You are connected")

    def on_message(self, message):
        # print("received message {}".format(message))

        for client in active_clients:
            client.write_message(message)
        # self.write_message(json.dumps(message))

        d = json.loads(message)
        try:
            if d["message"] == "connected":
                active_clients_name.append(d["type"])
                

            else:
                pass
        except:
            pass
        # active_clients_name.append(self)
        print("received message {}".format(message))

        # self.last = time.time()

    def on_close(self):
        '''Channel is closed'''
        print("connection is closed")
        # self.loop.stop()

        li = disconnect(self)

        for client in active_clients:
            client.write_message(json.dumps(
                {"type": li, "message": "disconnected"}))
        # active_clients.remove(self)

    def check_origin(self, origin):
        return True


def initiate_server():
    # create a tornado application and provide the urls
    app = tornado.web.Application(web_socket_handler.route_urls())

    # setup the server
    server = tornado.httpserver.HTTPServer(app)
    server.listen(options.port)

    # start io/event loop
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    initiate_server()
