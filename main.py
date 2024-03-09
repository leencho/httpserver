#!/bin/env python3


import socketserver
import threading
import signal


class MyTCPRequestHandler(socketserver.StreamRequestHandler, socketserver.ThreadingTCPServer):

    def handle(self):
        print("recieced request from {}".format(self.client_address[0]))
        msg = self.rfile.readline().strip().split()
        print(msg)
        recv_data = {
            "method": msg[0],
            "path": msg[1],
            "protocol": msg[2]
        }
        if recv_data["protocol"] == b'HTTP/1.1' or recv_data["protocol"] == b'HTTP/1.0':
            while len(msg) != 0 and msg != b"\r\n":
                msg = self.rfile.readline().split()
                if len(msg) != 0:
                    recv_data[msg[0].strip(b":")] = msg[1]
            if recv_data["method"] == b"POST":
                self.post_request(recv_data)
            elif recv_data["method"] == b"GET":
                self.get_Request(recv_data)
        else:
            response = b"505 HTTP Version Not Supported\r\n"
            self.wfile.write(response)

    def post_request(self, recv_data):
        print(recv_data)
        print("the protocol", recv_data["protocol"])
        if recv_data["path"] == b"/" or recv_data["path"] == b"/test.txt":
            try:
                data_length = int(recv_data[b'Content-Length'].decode("utf-8"))
            except KeyError:
                data_length = int(recv_data[b'content-length'].decode("utf-8"))
            try:
                message = self.rfile.read(data_length)
                print("THIS IS THE MESSAGE: ", message)

                with open("test.txt", "w") as file:
                    file.write(message.decode("utf-8"))
            finally:
                response = b"%b 200 OK\r\n" % recv_data['protocol']
                response += b"Content-Type: text/html\r\n"
                response += b"\r\n"
                response += b"<h1> the post has been created</h1>"
                self.wfile.write(response)
        else:
            response = b"403 - Forbidden\r\n"
            self.wfile.write(response)

    def get_Request(self, recv_data):
        if recv_data["path"] == b"/" or recv_data["path"] == b"/index":
            with open("index.html", "r") as file:
                file_content = file.read()
            content_len = len(file_content)
            response = b"%b 200 OK\r\n" % recv_data['protocol']
            response += b"Content-Type: text/html\r\n"
            response += b"Content-Length: %d\r\n" % content_len
            response += b"\r\n"
            response += file_content.encode("utf-8")
            self.wfile.write(response)
        else:
            response = b"404 error\r\n"
            self.wfile.write(response)


if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 9000
    with socketserver.TCPServer((HOST, PORT), MyTCPRequestHandler) as server:
        try:
            thread = threading.Thread(target=server.serve_forever)
            print("connected to {}:{}".format(HOST, PORT))
            thread.start()
            thread.join()
        except:
            print("shutting down!")
