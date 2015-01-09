from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
import psutil
from time import sleep
from random import randint


class LoadHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super(LoadHandler, self).__init__(request, client_address, server)

    def do_GET(self):
        port = 0
        
        for name, value in sorted(self.headers.items()):
            if name.lower() != 'host':
                continue
            value = value.rstrip()
            port = int(value[value.index(':')+1:len(value)])

        if psutil.phymem_usage().percent < 80:
        
            # allocate 50MiB
            memory = ' ' * 52428800
            
            # wait a bit
            duration = randint(0, 1)
            sleep(duration)
            
            # free up the memory again
            memory = None
           
               
            response = [
                    '<html>',
                    '<head><title>Memory load test</title></head><body>',
                    '<h1>Memory load test</h1>',
                    'Allocated memory: %d bytes' % (52428800),
                    '<br>Server port: %s' % (port),
                    '<br>Client address: %s (%s)' % (self.client_address,
                                                    self.address_string()),
                    '<br>Server version: %s' % self.server_version,
                    '<br>System version: %s' % self.sys_version,
                    '<br>Protocol version: %s' % self.protocol_version,
                    '</body></html>',
                    ]
            
        else:
            usage = psutil.phymem_usage()
            
            response = [
                '<html>',
                '<head><title>Memory load test</title></head><body>',
                '<h1>Memory load test</h1>',
                'Unable to allocate enough memory for the test, host memory full.',
                '<br><h2>Memory usage</h2>',
                '<br>total: %d, available: %d, percent: %d, used: %d, free: %d' % (usage.total, usage.available, usage.percent, usage.used, usage.free),
                '<br>Server port: %s' % (port),
                '<br>Client address: %s (%s)' % (self.client_address,
                                                self.address_string()),
                '<br>Server version: %s' % self.server_version,
                '<br>System version: %s' % self.sys_version,
                '<br>Protocol version: %s' % self.protocol_version,
                '</body></html>',
                ]
            
            message = '\r\n'.join(response)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(message.encode('utf-8'))

if __name__ == '__main__':
    import sys
    port = 8080
    if len(sys.argv) >= 2:
        port = int(sys.argv[1])
    httpd = HTTPServer(('0.0.0.0', port), LoadHandler)
    httpd.serve_forever()
