from http.server import BaseHTTPRequestHandler, HTTPServer
import sys, uuid
from urllib import parse

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    
    tokens = {}
    logins = {"myUser":"myPassword"}
    
    # Set the HTTP status code and response headers
    def set_headers(self, responseCode):
        self.send_response(responseCode)
        self.send_header("Content-type", "text/html")
        self.send_header('Access-Control-Allow-Origin', "*")
        self.send_header('Access-Control-Allow-Headers', "*")
        self.end_headers()
    
    def do_GET(self):
        # TO-DO: Handle GET Requests
        
    def do_POST(self):
        # TO-DO: Handle POST Requests
        
    # Fetches the requested path
    def getPage(self):
        return parse.urlsplit(self.path).path
    
    # Fetches the request body data (i.e. POST request parameters)
    def getRequestData(self):
        body = self.rfile.read(int(self.headers.get('Content-Length')))
        body = body.decode("utf-8")
        return dict(parse.parse_qsl(body))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    try:
        webServer.serve_forever()
    except:
        webServer.server_close()
        print("Server stopped.")
        sys.exit()
    webServer.server_close()
    print("Server stopped.")
    sys.exit()