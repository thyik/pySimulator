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
                data_str = str(self.data, 'utf-8')
                # decode individual token cmd
                for cmd in data_str.split('\r'):
                    reply = self.decode_reply(cmd)
                    for each_reply in reply.split('\r'):
                        print(f"reply:{each_reply}")
                    # just send back the same data, but upper-cased
                    # self.request.sendall(self.data.upper())
                    self.request.sendall(bytes(reply, 'utf-8'))
        except ConnectionAbortedError:
            print("Client {}:{} Connection Abort".format(*self.client_address))

    def finish(self):
        print('{}:{} disconnected'.format(*self.client_address))

    def decode_reply(self, cmd: str):
        """
            Row1in=Z
            Row1out=R
            Row1EOL=CR
        """
        parser = IniFile('d:/testconfig/config.ini')

        num_reply = parser.get_int('Setting', 'Number Of Reply', 40)
        reply = 'R\r'  # default 'R'

        for x in range(num_reply):
            number = x + 1
            in_reply = parser.get_string('Setting', f'Row{number}in', '')

            num_of_chars = cmd.__len__()
            partial_str = in_reply[0:num_of_chars]
            if partial_str == cmd:
            # if bytes(in_reply, 'utf-8') == self.data:
                crlf = parser.get_string('Setting', f'Row{number}eol', 'CR')
                check_file = parser.get_bool('Setting', f'row{number}filechk')
                if check_file:
                    # get reply from .txt
                    txtfile = parser.get_string('Setting', f'row{number}file')
                    reply = self.txt_reply(txtfile, crlf)
                else:
                    reply = parser.get_string('Setting', f'Row{number}out', 'R')
                    reply += self.eol(crlf)

                break

        return reply

    def txt_reply(self, filepath: str, eol: str) -> str:
        reply = ''
        crlf = self.eol(eol)
        with open(filepath, "r") as reader:
            for line in reader.readlines():
                line = line.rstrip('\r\n')
                reply += line + crlf

        return reply

    def eol(self, eol_type: str):
        if eol_type == 'CR':
            eol_str = '\r'
        elif eol_type == 'CRLF':
            eol_str = '\r\n'
        else:
            eol_str = '\r'
        return eol_str

if __name__ == "__main__":
    HOST, PORT = "localhost", 700

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
