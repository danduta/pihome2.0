#!/usr/bin/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
import serial
import RPi.GPIO as GPIO

host_addr = '0.0.0.0'
host_port = 4769
index_path = '/home/pi/work/led-server/index.html'

red_pin = 13
green_pin = 12
blue_pin = 19
pwm_freq = 490

GPIO.setmode(GPIO.BCM)

GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)
GPIO.setup(blue_pin, GPIO.OUT)

red_pwm = GPIO.PWM(red_pin, pwm_freq)
green_pwm = GPIO.PWM(green_pin, pwm_freq)
blue_pwm = GPIO.PWM(blue_pin, pwm_freq)

red_pwm.start(0)
green_pwm.start(0)
blue_pwm.start(0)

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

        red_pwm.ChangeDutyCycle(red_value / 255 * 100)
        green_pwm.ChangeDutyCycle(green_value / 255 * 100)
        blue_pwm.ChangeDutyCycle(blue_value / 255 * 100)
        print('COLORS RECEIVED:', red_value, green_value, blue_value, 'PWM DUTY CYCLES', red_value / 255 * 100, green_value / 255 * 100, blue_value / 255 * 100)

        self.show_index()
        return

if __name__ == '__main__':
    try:
        server = HTTPServer((host_addr, host_port), RequestHandler)
        print('Starting server at http://{}:{}'.format(host_addr, host_port))
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nClosing server...')
        red_pwm.stop()
        green_pwm.stop()
        blue_pwm.stop()
        GPIO.cleanup()
        exit()
