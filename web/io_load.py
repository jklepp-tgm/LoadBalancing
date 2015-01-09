from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
import fnmatch
import os
import time

class LoadHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super(LoadHandler, self).__init__(request, client_address, server)

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path != '/':
            message = '<h1>400 Bad Request</h1>\r\n'
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(message.encode('utf-8'))
            return
            
        start = time.time()
        port = 0
        
        for name, value in sorted(self.headers.items()):
            if name.lower() != 'host':
                continue
            value = value.rstrip()
            port = int(value[value.index(':')+1:len(value)])
        
        response = [
                    '<html>',
                    '<head><title>I/O load test</title></head><body>',
                    '<h1>I/O load test</h1>',
                    '<br>Server port: %s' % (port),
                    '<br>Client address: %s (%s)' % (self.client_address,
                                                    self.address_string()),
                    '<br>Server version: %s' % self.server_version,
                    '<br>System version: %s' % self.sys_version,
                    '<br>Protocol version: %s' % self.protocol_version,
        ]
        
        for root, dirnames, filenames in os.walk('/'):
            stop = time.time() - start
            if stop >= 3.0:
                response.append('<br>Execution stopped after %f seconds.' % (stop))
                break; 
            for filename in fnmatch.filter(filenames, 'test.txt'):
                response.append('<br>File: '+os.path.join(root, filename))
                response.append('<br>-> Match!')
        response.append('</body>')
        response.append('</html>')
        
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
