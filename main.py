import tkinter as tk
import socketserver
import logging
import threading
import time

# imports classes under helpers folder
from helpers.server import MyTCPHandler
from helpers.inifile import IniFile

x = threading.Thread()

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # init Button
        self.listen = tk.Button(self)
        self.listen["text"] = "Listen"
        self.listen["command"] = self.start_server
        self.listen.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def start_server(self):
        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO,
                            datefmt="%H:%M:%S")
        global x
        logging.info("Main    : before creating thread")
        x = threading.Thread(target=thread_function, args=(1,))
        logging.info("Main    : before running thread")
        x.start()

        print("hi there, everyone!")

def thread_function(name):
    logging.info("Thread %s: starting", name)
    parser = IniFile('../playground/config.ini')
    HOST, PORT = "localhost", 700

    HOST = parser.get_string('Connection', 'ServerIPAddress', 'localhost')
    PORT = parser.get_int('Setting', 'ServerPort', 700)

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
    logging.info("Thread %s: finishing", name)

root = tk.Tk()
app = Application(master=root)
app.mainloop()

logging.info("Main    : wait for the thread to finish")
x.join()
logging.info("Main    : all done")


