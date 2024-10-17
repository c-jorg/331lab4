from http.server import BaseHTTPRequestHandler, HTTPServer
import sys, time
from urllib import parse
import urllib.request

hostName = "localhost"
serverPort = 1111

class MyServer(BaseHTTPRequestHandler):
    
    tokens = {}
    
    # Set the HTTP status code and response headers
    def set_headers(self, responseCode):
        self.send_response(responseCode)
        self.send_header("Content-type", "text/html")
        self.send_header('Access-Control-Allow-Origin', "*")
        self.send_header('Access-Control-Allow-Headers', "*")
        self.end_headers()
    
    def do_GET(self):
        # TO-DO: Handle GET requests for our secure resource
        print("GET REQUEST SecureStorage.py")
        if self.getURI() == '/':
            self.set_headers(200)
            self.wfile.write(self.getURI().encode())
            html = open("TestAuth.html")
            htmlString = html.read()
            html.close()
            self.wfile.write(bytes(htmlString, "utf-8"))

    def getToken(self, token):
        # TO-DO: Fetches/caches a token for a set period of time, automatically re-fetches old tokens
        print("getTokens SecureStorage.py")
        
    # Gets the query parameters of a request and returns them as a dictionary
    def getParams(self):
        output = {}
        queryList = parse.parse_qs(parse.urlsplit(self.path).query)
        for key in queryList:
            if len(queryList[key]) == 1:
                output[key] = queryList[key][0]
        return output
    
    # Returns a string containing the page (path) that the request was for
    def getURI(self):
        return parse.urlsplit(self.path).path

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started at 127.0.0.1:1111")

    try:
        webServer.serve_forever()
    except:
        webServer.server_close()
        print("Server stopped.")
        sys.exit()

    webServer.server_close()
    print("Server stopped.")
    sys.exit()