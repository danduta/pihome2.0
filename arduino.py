#!/usr/bin/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import serial

host_addr = '0.0.0.0'
host_port = 4769
index_path = '/home/pi/work/led-server/index.html'

ser = serial.Serial('/dev/ttyUSB0')

class RequestHandler(BaseHTTPRequestHandler):
    def show_index(self):
        f = open(index_path, 'rb')

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(f.read())

        f.close()

    def do_GET(self):
        colors = parse_qs(urlparse(self.path).query)
        if len(colors) == 0:
            self.show_index()
            return

        red_value = int(colors['r'][0])
        green_value = int(colors['g'][0])
        blue_value = int(colors['b'][0])

        print('COLORS RECEIVED:', red_value, green_value, blue_value, 'PWM DUTY CYCLES', red_value / 255 * 100, green_value / 255 * 100,blue_value / 255 * 100)

        message = '{:03d}#{:03d}#{:03d}\n'.format(red_value, green_value, blue_value);
        message = message.encode()
        message = bytearray(message)
        ser.write(message)

        print(message)

        self.show_index()
        return

if __name__ == '__main__':
    try:
        server = HTTPServer((host_addr, host_port), RequestHandler)
        print('Starting server at http://{}:{}'.format(host_addr, host_port))
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nClosing server...')
        ser.close()
        exit()
