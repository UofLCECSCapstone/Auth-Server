import http.server
import random
import datetime
import hashlib

class AuthServer(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            self.log(self.path)
            if self.path   == "/get_current_auth_token":
                self.log("Valid request!")
                responseText = getCurrentAuthToken()
                self.send_valid_response(responseText)
                return
        except IOError:
            self.send_error(404, 'file not found')
        # TODO How do I handle other types of errors?

    def send_valid_response(self, responseText):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.log("Response: " + responseText)
        self.wfile.write(bytes(responseText, "utf-8"))

    def log(self, message):
        print("AuthServer::" + message)

def StartServer():
    print("Auth server starting...")
    #ip and port of server
    server_address = ('127.0.0.1', 8081)
    httpd = http.server.HTTPServer(server_address, AuthServer)
    print('auth server is running...')
    httpd.serve_forever()

def getCurrentAuthToken():
    ###########################################
    ##### Generates an auth token to pair #####
    ##### a device with the hub.          #####
    ###########################################
    #token = random.randrange(1, 9999)
    # TODO Just storing the secret key in the source is probably a bad idea...
    SecretKey = "12d10588-67c9-4963-811a-60609a520c02"

    currentTime = datetime.datetime.now().timetuple()
    year   = currentTime[0]
    month  = currentTime[1]
    day    = currentTime[2]
    hour   = currentTime[3]
    minute = currentTime[4]

    dateTimeString = str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(minute)

    print("Datetime string: " + dateTimeString)

    hashInput = dateTimeString + SecretKey
    print("Hash input: " + hashInput)

    hashObject = hashlib.sha512(bytes(hashInput, 'utf-8'))
    hex_dig = hashObject.hexdigest()
    print(hex_dig)
    truncated_hex_dig = hex_dig[:6]

    return truncated_hex_dig

########################################################################
##### Starts the Auth server which returns the current auth token. #####
########################################################################
def main():
    StartServer()

if __name__ == "__main__":
    main()
