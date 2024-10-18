from http.server import BaseHTTPRequestHandler, HTTPServer
import sys, uuid
from urllib import parse

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    
    tokens = {}
    logins = {"myUser":"myPassword","test":"letmein"}
    
    # Set the HTTP status code and response headers
    def set_headers(self, responseCode):
        self.send_response(responseCode)
        self.send_header("Content-type", "text/html")
        self.send_header('Access-Control-Allow-Origin', "*")
        self.send_header('Access-Control-Allow-Headers', "*")
        self.end_headers()
    
    def do_GET(self):
        # TO-DO: Handle GET Requests
        print("GET request Authenticator.py")
        if self.getURI()[1:] in self.tokens.keys():
            self.set_headers(200)
            self.wfile.write(bytes(self.tokens[self.getURI()[1:]] + " is the token", "utf-8"))
            
        elif self.getURI() == '/logout':
            clientIP = self.client_address[0]
            for key, value in dict(self.tokens).items():
                del self.tokens[key]
                self.set_headers(200)
                self.wfile.write(bytes("logout succesful \n" + clientIP, "utf-8"))
        else:
            self.set_headers(404)
            self.wfile.write(bytes("404 URI not found", "utf-8"))
            
    def do_POST(self):
        # TO-DO: Handle POST Requests
        print("POST REQUEST Authenticator.py")
        if self.getURI() == '/login':
            requestData = self.getRequestData()
            if requestData['username'] in self.logins.keys():
                if self.logins[requestData['username']] == requestData['password']:
                    clientIP = self.client_address[0]
                    if clientIP not in self.tokens.values():
                        token = str(uuid.uuid4())
                        self.tokens[token] = clientIP
                        self.set_headers(200)
                        self.wfile.write(bytes("Login successful, your token: " + token, "utf-8"))
                    else:
                        self.set_headeres(409)
                        self.wfile.write(bytes("Login failed: IP already in use","utf-8"))
                else:
                    self.set_headers(401)
                    self.wfile.write(bytes("Login failed: username or password incorrect", "utf-8"))
            else:
                self.set_headers(401)
                self.wfile.write(bytes("Login failed: username does not exist", "utf-8"))
        else:
            self.set_headers(404)
            self.wfile.write("page not found", "utf-8")
        
    # Fetches the requested path
    def getURI(self):
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