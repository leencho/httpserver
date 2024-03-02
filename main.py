import socketserver


def file_read(filename):
    with open(filename, "r") as file:
        return file.read()


def file_write(filename, msg):
    with open(filename, "w") as file:
        file.write(msg)


# def http_response(request):
#    if request == "GET / HTTP/1.1":
#        response = "HTTP/1.1 200 0k \r\n\n"
#    return response


class MyTCPRequestHandler(socketserver.StreamRequestHandler):

    def handle(self):
        print("recieced request from {}".format(self.client_address[0]))
        msg = self.rfile.readline().strip()
        print(msg)
        file_content = file_read("index.html")
        file_length = len(file_content)
        if msg.decode("utf-8") == "hello":
            self.wfile.write("hello back to you\n".encode("utf-8"))
        # elif msg == b"GET /index HTTP/1.1":
        #    self.wfile.write(file_content.encode("utf-8"))
        elif msg.decode("utf-8") == "GET / HTTP/1.1":
            self.wfile.write("HTTP/1.1 200 OK \n\n\r".encode("utf-8"))
        elif msg == b"GET /index HTTP/1.1":
            print("correct!")
            response = "HTTP/1.1 200 OK \r\n"
            resp_len = len(response)
            content_length = resp_len + file_length
            response += "Content-Length: {}".format(file_length) + "\r\n"
            response += "\r\n"
            response += file_content
            self.wfile.write(response.encode("utf-8"))
        else:
            file_write("hello.txt", msg.decode("utf-8"))
            self.wfile.write("hello from server!\n".encode("utf-8"))


if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 9001
    server = socketserver.TCPServer((HOST, PORT), MyTCPRequestHandler)
    print("serving msg... on {}:{}".format(HOST, PORT))
    try:
        server.serve_forever()
    except:
        print("shutting down the")
