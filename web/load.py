from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
import base64

from cpu_load import LoadHandler as CpuLoadHandler
from io_load import LoadHandler as IoLoadHandler
from memory_load import LoadHandler as MemoryLoadHandler


paths = {
    '/cpu': CpuLoadHandler,
    '/io': IoLoadHandler,
    '/memory': MemoryLoadHandler,}


class LoadHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super(LoadHandler, self).__init__(request, client_address, server)
        self.request = request
        self.client_address = client_address
        self.server = server

    def do_GET(self):
        path = self.path
        if path in paths.keys():
            paths[path].do_GET(self)
        else:
            message_parts = """<!doctype html public>
                               <html>
                               <head>
                                   <title>Welcome to Server """ + sys.argv[1] + """!</title>
                                   <style>
                                       body {
                                           -webkit-animation: myfirst 5s; /* Chrome, Safari, Opera */
                                           animation: myfirst 5s;
                                           background: yellow;}
                                       /* Chrome, Safari, Opera */
                                       @-webkit-keyframes myfirst {
                                           from {background: red;}
                                           to {background: yellow;}}
                                       /* Standard syntax */
                                       @keyframes myfirst {
                                           from {background: red;}
                                           to {background: yellow;}} 
                                   </style>
                               </head>
                               <body>
                               <div id="wrapper" style="width: 100%; margin: auto auto auto auto;">
                                   <marquee direction="down" width="100%" height="50%" behavior="alternate" >
                                       <marquee behavior="alternate">
                                           <h1>Welcome to Server """ + sys.argv[1] + """!</h1>
                                       </marquee>
                                   </marquee>
                               </div>
                               
                               </body>
                               </html>"""
            #print(sys.argv[1])
            #print(base64.b64encode(sys.argv[1].encode('utf8')))
            message_parts = message_parts.split('\n')
            #for name, value in sorted(self.headers.items()):
            #    message_parts.append('%s=%s' % (name, value.rstrip()))
            message_parts.append('')
            message = '\r\n'.join(message_parts)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(message.encode('utf-8'))

if __name__ == '__main__':
    import sys
    port = int(sys.argv[1])
    httpd = HTTPServer(('0.0.0.0', port), LoadHandler)
    httpd.serve_forever()
