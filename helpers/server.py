import socketserver
from inifile import IniFile


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def setup(self):
        print('{}:{} connected'.format(*self.client_address))

    def handle(self):
        try:
            while True:
                # self.request is the TCP socket connected to the client
                self.data = self.request.recv(1024).strip()  # (b"\n\r")
                print("{} wrote:".format(self.client_address[0]))
                print(self.data)
                reply = self.decode_reply()
                print(f"reply:{reply}")
                # just send back the same data, but upper-cased
                # self.request.sendall(self.data.upper())
                self.request.sendall(bytes(reply, 'utf-8'))
        except ConnectionAbortedError:
            print("Client {}:{} Connection Abort".format(*self.client_address))

    def finish(self):
        print('{}:{} disconnected'.format(*self.client_address))

    def decode_reply(self):
        """
            Row1in=Z
            Row1out=R
            Row1EOL=CR
        """
        parser = IniFile('d:/testconfig/config.ini')

        num_reply = parser.get_int('Setting', 'Number Of Reply', 40)
        reply = 'R'  # default 'R'

        for x in range(num_reply):
            in_reply = parser.get_string('Setting', f'Row{x + 1}in', '')

            if bytes(in_reply, 'utf-8') == self.data:
                reply = parser.get_string('Setting', f'Row{x + 1}out', 'R')
                crlf = parser.get_string('Setting', f'Row{x + 1}eol', 'CR')
                if crlf == 'CR':
                    reply += '\r'
                elif crlf == 'CRLF':
                    reply += '\r\n'
                else:
                    reply += '\r'
                break

        crlf = parser.get_bool('Setting', 'CRLF', False)

        return reply


if __name__ == "__main__":
    HOST, PORT = "localhost", 700

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
