# Developed by Preston Turner
# PyWebPlug v1.0

# This server serves the webpages. It does not interact with the websockets.

import string, cgi, time
import json
from neuralnet import *
from os import curdir, sep
from http.server import BaseHTTPRequestHandler, HTTPServer

# This is a simple server and is not very safe in its current form.
class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path == '/':
                self.path = "/index.html"
            f = open(curdir + sep + self.path)
            out = f.read()
            ext = self.path.split('.')
            ext = ext[len(ext)-1]
            if (ext != '.ico'):
                out = bytes(out, 'utf-8')
            self.gen_headers(ext)
            self.wfile.write(out)
            f.close()
            return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def gen_headers(self, ext):
        self.send_response(200)
        contentType = 'text/html'
        if (ext == "css"):
            contentType = 'text/css'
        elif (ext == "js"):
            contentType = 'application/javascript'
        self.send_header('Content-type', contentType)
        self.end_headers()

    def do_POST(self):
        # post method
        path = self.path#[4:] # end of the URL
        length = int(self.headers['Content-Length'])
        body = json.loads(self.rfile.read(length).decode("utf-8"))
        print(path)
        if path == "/visualization/nnet":
            arr = body["array"]
            print(arr)
            v = predict(arr)
            #item1 = body["array"][1]
            print(v)
            out = {"predicition": v[0]}
            self.send_response(200)
            self.send_header('Contant-type', 'application/json')
            self.end_headers()
            self.write_out(out)

    def write_out(self, obj):
        out = json.dumps(obj)#, default=encode_complex)
        self.wfile.write(bytes(out, 'utf-8'))
        

def main():
    try:
        # Server on the standard webserver port of 80.
        server = HTTPServer(('', 8001), MyHandler)
        print("Starting webpage server...")
        # Create nerual net
        nnetBegin()
        # end NN creation
        server.serve_forever()
    except KeyboardInterrupt:
        print(' received, closing server.')
        server.socket.close()

if __name__ == '__main__':
    main()