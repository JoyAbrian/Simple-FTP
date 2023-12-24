import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import socket
import os
import struct
import time

def send() :
    window = Toplevel(root)
    window.title("Send File")
    window.geometry("250x200")
    window.resizable(False,False)

    iconSend = PhotoImage(file= "images/btnSend.png")
    window.iconphoto(False, iconSend)

    host = socket.gethostname()
    Label(window, text=f"Sending file by {host}...", font=("Arial", 9, 'bold')).place(x=0, y=0)

    def select_file() :
        global filename
        file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select File", filetypes=(('All Files', '*.*'),))
        filename = os.path.basename(file_path)

    def send_file() :
        TCP_IP = socket.gethostbyname(host)
        TCP_PORT = 1456
        BUFFER_SIZE = 1024
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("Sending server request...")
        try:
            s.connect((TCP_IP, TCP_PORT))
            print("Connection successful")
        except:
            print("Connection unsuccessful. Make sure the server is online.")

        print("\nUploading file: {}...".format(filename))
        try:
            s.recv(BUFFER_SIZE)
            s.send(struct.pack("h", len(filename)))
            s.send(filename.encode())
            s.recv(BUFFER_SIZE)
            s.send(struct.pack("i", os.path.getsize(filename)))
        except:
            print("Error sending file details")
        try:
            content = open(filename, "rb")
            l = content.read(BUFFER_SIZE)
            print("\nSending...")
            while l:
                s.send(l)
                l = content.read(BUFFER_SIZE)
            content.close()
            upload_time = struct.unpack("f", s.recv(4))[0]
            upload_size = struct.unpack("i", s.recv(4))[0]
            print("\nSent file: {}\nTime elapsed: {}s\nFile size: {}b".format(filename, upload_time, upload_size))
        except:
            print("Error sending file")
            return


    Button(window, text="Select File", bg="#FFFFFF", width=20, height=3, command=select_file).place(x=30, y=30)
    Button(window, text="Send File", bg="#63C5DA", width=20, height=3, command=send_file).place(x=30, y=100)

    window.mainloop()

def receive():
    main = Toplevel(root)
    main.title("Receive File")
    main.geometry("250x200")
    main.resizable(False, False)

    iconSend = PhotoImage(file= "images/btnReceive.png")
    main.iconphoto(False, iconSend)

    host = socket.gethostname()
    Label(main, text=f"{host} is receiving file...", font=("Arial", 9, 'bold')).place(x=0, y=0)

    def receive_file():
        TCP_IP = socket.gethostbyname(host)
        TCP_PORT = 1456
        BUFFER_SIZE = 1024
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(1)
        conn, addr = s.accept()

        conn.send(b"1")
        file_name_size = struct.unpack("h", conn.recv(2))[0]
        file_name = conn.recv(file_name_size).decode().replace('\x00', '')
        conn.send(b"1")
        file_size = struct.unpack("i", conn.recv(4))[0]
        start_time = time.time()
        output_file = open(file_name, "wb")
        bytes_received = 0
        print("\nReceiving...")
        while bytes_received < file_size:
            l = conn.recv(BUFFER_SIZE)
            output_file.write(l)
            bytes_received += len(l)
        output_file.close()
        print("\nReceived file: {}".format(file_name))
        conn.send(struct.pack("f", time.time() - start_time))
        conn.send(struct.pack("i", file_size))
        return

    Label(main, text="Input Sender ID :").place(x=0, y=30)
    senderID = Entry(main, width=30, fg="black", border=2).place(x=5, y=50)
    
    Label(main, text="File Name :").place(x=0, y=80)
    fileName = Entry(main, width=30, fg="black", border=2).place(x=5, y=100)

    Button(main, text="Receive File", bg="#63C5DA", command=receive_file).place(x=120, y=140)

    main.mainloop()

root = Tk()
root.title("File Transfer")
root.geometry("400x600")
root.configure(bg="#FFFFFF")
root.resizable(False,False)

icon = PhotoImage(file = "images/icon.png")
root.iconphoto(False, icon)

Label(root, text="File Transfer Protocol", font=("Georgia", 20, "bold"),bg="#FFFFFF").place(x=45, y=30)

Label(root, text="Send", font=("Georgia", 14),bg="#FFFFFF").place(x=170, y=100)
sendImage = PhotoImage(file= "images/btnSend.png")
sendBtn = Button(root, image=sendImage, bg="#FFFFFF", bd = 0, command=send)
sendBtn.place(x=135,y=150)

Label(root, text="Receive", font=("Georgia", 14),bg="#FFFFFF").place(x=160, y=330)
receiveImage1 = PhotoImage(file= "images/btnReceive.png")
receiveBtn = Button(root, image=receiveImage1, bg="#FFFFFF", bd = 0, command=receive)
receiveBtn.place(x=135,y=380)

root.mainloop()