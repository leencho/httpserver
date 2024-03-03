import socketserver


def file_read(filename):
    with open(filename, "r") as file:
        return file.read()


def file_write(filename, msg):
    with open(filename, "w") as file:
        file.write(msg)


class MyTCPRequestHandler(socketserver.StreamRequestHandler):

    def handle(self):
        print("recieced request from {}".format(self.client_address[0]))
        msg = self.rfile.readline().strip()
        print(msg)
        file_content = file_read("index.html")
        file_length = len(file_content)

        # handling get request
        if msg.startswith(b"GET"):
            if msg.decode("utf-8") == "GET / HTTP/1.1":
                response = "HTTP/1.1 200 ok\r\n"
                response += "Content-Type: text/html\r\n"
                response += "Content-Length: {}".format(
                    len(file_content)) + "\r\n"
                response += "\r\n"
                response += file_content
                self.wfile.write(response.encode("utf-8"))
            elif msg == b"GET /index HTTP/1.1":
                response = "HTTP/1.1 200 OK \r\n"
                resp_len = len(response)
                content_length = resp_len + file_length
                response += "Content-Length: {}".format(file_length) + "\r\n"
                response += "\r\n"
                response += file_content
                self.wfile.write(response.encode("utf-8"))
            else:
                response = "HTTP/1.1 400 error\r\n"
                response += "Content-Type: text/html\r\n"
                response += "\r\n"
                response += "<h1> 404 NOT FOUND </h>"
                file_write("hello.txt", response)
                self.wfile.write(response.encode("utf-8"))
        else:
            response = "HTTP/1.1 400 error\r\n"
            self.wfile.write(response.encode("utf-8"))


if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 9001
    server = socketserver.TCPServer((HOST, PORT), MyTCPRequestHandler)
    print("serving msg... on {}:{}".format(HOST, PORT))
    try:
        server.serve_forever()
    except:
        print("shutting down the")
