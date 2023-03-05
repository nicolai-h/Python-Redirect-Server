#!/usr/bin/env python3

# Useful links: 
# 1. https://docs.python.org/3/library/socketserver.html
# 2. https://docs.python.org/3/library/http.server.html
# 3. https://docs.python.org/3/library/argparse.html
# 4. https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/307

import http.server
import socketserver
import argparse
from pprint import pprint


def Handler(GET_REDIRECT, POST_REDIRECT, GET_REDIRECT_URL, POST_REDIRECT_URL):
    class Request_handler(http.server.SimpleHTTPRequestHandler):
        """
        Returns a class that handles requests
        """

        def OK(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

        def GET_redirect(self):
            self.send_response(301) # 301, moved Permanently (todo add 303?)
            self.send_header("Location", GET_REDIRECT_URL) # add location header to indicate the new location
            self.end_headers()
        
        def POST_redirect(self):
            self.send_response(307) # 307, temporary redirect
            self.send_header("Location", POST_REDIRECT_URL) # add location header to indicate the new location
            self.end_headers()

        def do_GET(self):
            if GET_REDIRECT == True:
                self.GET_redirect()
            else:
                self.OK()

        def do_POST(self):
            post_data = self.rfile.read(int(self.headers["Content-Length"]))
            pprint(post_data.decode("UTF-8"))

            if POST_REDIRECT == True:
                self.POST_redirect()
            else:
                self.OK()
        
        def do_HEAD(self):
            if GET_REDIRECT == True:
                self.GET_redirect()
            else:
                self.OK()
    
    return Request_handler


def main():
    parser = argparse.ArgumentParser(
        prog = "Redirect server",
        description="A server that can redirect GET and POST requests",
        epilog="Redirect server")

    parser.add_argument("-ip", "--ip", action="store", default="")
    parser.add_argument("-p", "--port", action="store", type=int, default=8080)
    parser.add_argument("-grurl", "--get_redirect-url", action="store")
    parser.add_argument("-prurl", "--post_redirect-url", action="store")

    my_arguments = parser.parse_args()
    PORT = my_arguments.port
    IP = my_arguments.ip
    GET_REDIRECT_URL = my_arguments.get_redirect_url
    POST_REDIRECT_URL = my_arguments.post_redirect_url
    GET_REDIRECT = False if GET_REDIRECT_URL is None else True
    POST_REDIRECT = False if POST_REDIRECT_URL is None else True

    print(f"Servering at {IP} on port: {PORT}")

    handler = Handler(GET_REDIRECT, POST_REDIRECT, GET_REDIRECT_URL, POST_REDIRECT_URL)
    server = socketserver.TCPServer((IP, PORT), handler)
    server.serve_forever()


if __name__ == '__main__':
    main()
