from http.server import BaseHTTPRequestHandler, HTTPServer
from os import sep, path
import threading
from logging import getLogger

log = getLogger(__name__)

# HTTPRequestHandler class
class TestHTTPServerRequestHandler(BaseHTTPRequestHandler):
    # GET
    FOLDER, TOTO = path.split(path.realpath(__file__))

    def __init__(self, request, client_address, server):
        # super(BaseHTTPRequestHandler, self).__init__(request, client_address, server)
        super().__init__(request, client_address, server)
        self.path = "index.html"
        self.__folder = ""
        self.__folder, test = path.split(path.realpath(__file__))

    @property
    def folder(self):
        return path.split(path.realpath(__file__))[0]

    @folder.setter
    def folder(self, folder):
        self.__folder = folder

    def do_GET(self):
        # print(self.folder)
        log.debug(self.path)
        log.debug(super().__getattribute__("path"))
        if self.path == "/":
            self.path = "index.html"
            log.debug("Get root path")

        log.debug(super().__getattribute__("path"))
        try:
            # Check the file extension required and
            # set the right mime type
            sendReply = False
            if self.path.endswith(".html"):
                log.debug("serve html file")
                mimetype = 'text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype = 'image/jpg'
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype = 'image/gif'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype = 'application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype = 'text/css'
                sendReply = True
            if self.path == "/close":
                log.debug("close")

            if sendReply:
                # Open the static file requested and send it
                log.debug("current dir is '{}'".format(path.realpath(__file__)))
                log.debug("Before join '{}'".format(self.folder))
                file_name = "{}{}{}".format(self.folder, sep, self.path)
                log.debug("Filename '{}'".format(file_name))
                with open(file_name, "br") as f:
                    self.send_response(200)
                    self.send_header('Content-type', mimetype)
                    self.end_headers()
                    self.wfile.write(f.read())
            return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % file_name)
        except Exception as exception:
            log.error(exception.args[0])


class TestServer:
    def __init__(self):
        self.__server_address = ('127.0.0.1', 8081)
        self.__httpd = HTTPServer(self.__server_address, TestHTTPServerRequestHandler)
        self.__thread = None

    def start(self):
        self.__thread = threading.Thread(target=self.__httpd.serve_forever)
        self.__thread.daemon = True
        self.__thread.start()
        log.debug("Starting server")

    def stop(self):
        self.__httpd.shutdown()
        self.__thread = None
        log.debug("Stoping server")
