from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
import fnmatch
import os
import time
import sys


def file_walk():
    response = []

    start = time.time()

    for root, dirnames, filenames in os.walk('/'):
        stop = time.time() - start
        if stop >= 3.0:
            response.append('<br>Execution stopped after %f seconds.' % (stop))
            break; 
        for filename in fnmatch.filter(filenames, 'test.txt'):
            response.append('<br>File: '+os.path.join(root, filename))
            response.append('<br>-> Match!')

    return response


class LoadHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super(LoadHandler, self).__init__(request, client_address, server)

    def do_GET(self):
        print("io_load.py got a request")
            
        start = time.time()
        
        response = [
                    '<html>',
                    '<head><title>I/O load test</title></head><body>',
                    '<h1>I/O load test</h1>',
                    '<br>Server port: %s' % (sys.argv[1]),
                    '<br>Client address: %s (%s)' % (self.client_address,
                                                    self.address_string()),
                    '<br>Server version: %s' % self.server_version,
                    '<br>System version: %s' % self.sys_version,
                    '<br>Protocol version: %s' % self.protocol_version,
        ]
        
        fw = file_walk()

        for l in fw:
            response.append(l)

        response.append('</body>')
        response.append('</html>')
        response.append('')
        
        message = '\r\n'.join(response)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))
        return

if __name__ == '__main__':
    import sys
    port = 8080
    if len(sys.argv) >= 2:
        port = int(sys.argv[1])
    httpd = HTTPServer(('0.0.0.0', port), LoadHandler)
    httpd.serve_forever()
