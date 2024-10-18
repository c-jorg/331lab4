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
        if self.getURI() == '/lab4':
            self.set_headers(200)
            self.wfile.write(self.getURI().encode())
            html = open("TestAuth.html")
            htmlString = html.read()
            html.close()
            self.wfile.write(bytes(htmlString, "utf-8"))
            
        if self.getURI() == '/':
            print("checking tokens")
            parameters = self.getParams()
            if parameters.get('token'):
                clientIP = self.client_address[0]
                fetchedIP = self.getToken(parameters.get('token'))
                
                print("clientIP = " + clientIP + " fetchedIP = " + fetchedIP)
                
                if clientIP == fetchedIP:
                    self.set_headers(200)
                    self.wfile.write(self.getURI().encode())
                    html = open('success.html')
                    htmlString = html.read();
                    html.close()
                    self.wfile.write(bytes(htmlString, "utf-8"))
                else:
                    self.set_headers(401)
                    self.wfile.write(bytes("Client and token do not match!", "utf-8"))
            else:
                self.set_headers(401)
                self.wfile.write(bytes("No token provided!","utf-8"))
                    

    def getToken(self, token):
        # TO-DO: Fetches/caches a token for a set period of time, automatically re-fetches old tokens
        print("getTokens SecureStorage.py")
        
        if token == 'logout':
            return None
        if token not in self.tokens:
            try:
                fetchedIP = urllib.request.urlopen('http://127.0.0.1:8080/' + token).read()
                fetchedIP = fetchedIP.decode('utf-8')
                self.tokens[token] = [fetchedIP, time.time()]
                return fetchedIP
            except:
                return None
        else:
            tokenVals = self.tokens[token]
            if time.time() - tokenVals[1] > 300:
               del self.tokens[token]
               return self.getToken(token)
            else:
               return tokenVals[0]
        
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