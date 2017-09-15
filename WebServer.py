import http.server
import socketserver
import os
from threading import Thread
import sys, os, socket
from socketserver import ThreadingMixIn
from http.server import SimpleHTTPRequestHandler, HTTPServer

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

def init_Webserver():
  PORT = 80
  web_dir = os.path.join(os.path.dirname(__file__), 'www')
  os.chdir(web_dir)

  global httpd 
  httpd = ThreadingSimpleServer(('0.0.0.0', PORT), SimpleHTTPRequestHandler)
  print("**************************************")
  print("* Web Server BOT Roy serving at port", PORT)
  print("\n *   http://localhost/index.html")

def start_Webserver():
  try:
    #httpd.serve_forever()
    sys.stdout.flush()
    httpd.handle_request()
  except KeyboardInterrupt:
    httpd.shutdown()

def stop_Webserver():
  httpd.shutdown()
