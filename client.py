# Student ID:220084
# Student Name:Roshani Shrestha
# Module: ST5062CEM Programming and Algorithms 2
# Hamro Secure Chatting System
import socket
import threading
import customtkinter as ct
from tkinter import messagebox
import tkinter as tk
import tkinter.scrolledtext
from tkinter import simpledialog
from PIL import Image, ImageTk

appearance_mode = 'dark'

HOST = '127.0.0.1'
PORT = 3030


class Client:

    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        window = ct.CTk()
        window.geometry("520x320")
        window.title("Hamro Secure Chatting System")
        window.wm_iconbitmap('3.ico')

        def switch_mode():
            global appearance_mode
            if appearance_mode == 'dark':
                appearance_mode = 'light'
                ct.set_appearance_mode('light')
            else:
                appearance_mode = 'dark'
                ct.set_appearance_mode('dark')

        def givechatboxname():
            chat_name = simpledialog.askstring(
                "Chat Name", "Please enter a Chat Name", parent=window)
            if chat_name is not None:
                # User clicked "OK" and provided a chat name
                self.chat_name = chat_name
                window.destroy()
            else:
                # User clicked "Cancel," handle this case with messagebox
                messagebox.showinfo(
                    "Cancelled", "Chat name input was cancelled.")
                self.chat_name = None

            

        msg_label = ct.CTkLabel(
            window, text="Welcome To", font=("Arial", 15))
        msg_label.pack(pady=15)

        msg_label = ct.CTkLabel(
            window, text="Hamro Secure Chatting System", font=("Arial", 15))
        msg_label.pack(pady=5)

        msg_label = ct.CTkLabel(
            window, text="अब सजिलै सुरक्षित कुराकानी गर्नुहोस् !!", font=("Arial", 20))
        msg_label.pack()
        # logo in body
        picture_image = Image.open("chatbox.ico")
        picture_image = picture_image.resize((70, 70))

        # Create a PhotoImage object from the PIL Image
        picture_ctk_image = ImageTk.PhotoImage(picture_image)

        # Create a label to display the image
        picture_label = tk.Label(window, image=picture_ctk_image)
        picture_label.image = picture_ctk_image
        picture_label.pack(pady=15)
        # logo ends
        chat_name_btn = ct.CTkButton(
            window, text="Start Chat!", command=givechatboxname, fg_color="#DE4249",
            hover_color=("maroon"),
            text_color=("white"))
        chat_name_btn.pack(pady=15)

        switch = ct.CTkSwitch(window, text="Mode", command=switch_mode)
        switch.pack(pady=10)
        window.mainloop()

# page 2


# page1 completely finish

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        listen_thread = threading.Thread(target=self.listen)

        gui_thread.start()
        listen_thread.start()

    def gui_loop(self):
        if self.chat_name is None:
               return
        self.win = ct.CTk()
        self.win.wm_iconbitmap('3.ico')
        self.win.title(f"Chat of {self.chat_name}")
        self.win.resizable(0, 0)

        self.chat_label = ct.CTkLabel(
            self.win, text="Chat Box", font=("Arial", 15))
        self.chat_label.pack(padx=20, pady=5)

        self.text_display = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_display.pack(padx=20, pady=5)
        self.text_display.config(state='disabled')

        self.chat_label = ct.CTkLabel(
            self.win, text="Message", font=("Arial", 15))
        self.chat_label.pack(padx=20, pady=5)

        self.type_area = tkinter.Text(self.win, height=3, bg="Pink")
        self.type_area.pack(padx=20, pady=5)

        self.button_frame = tkinter.Frame(self.win)
        self.button_frame.pack(padx=20, pady=5)

        self.send_button = ct.CTkButton(
            self.button_frame, text="Send", command=self.double_encoding, fg_color="blue",
            hover_color=("maroon"),
            text_color=("white"))
        self.send_button.grid(row=0, column=0, padx=20, pady=5)

        self.decrypt_button = ct.CTkButton(
            self.button_frame, text="Decrypt", command=self.decrypt_message, fg_color="green",
            hover_color=("maroon"),
            text_color=("white"))
        self.decrypt_button.grid(row=0, column=1, padx=20, pady=5)

        self.exit_btn = ct.CTkButton(
            self.button_frame, text="Exit", command=exit, fg_color="#DE4249",
            hover_color=("maroon"),
            text_color=("white"))
        self.exit_btn.grid(row=0, column=2, padx=20, pady=5)

        self.gui_done = True
        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        self.win.mainloop()

    

    def encode_rot13(self, text):
        result = ""
        for char in text:
            ascii_value = ord(char)
            if 32 <= ascii_value <= 126:  # Handle printable ASCII characters
                result += chr((ascii_value - 32 + 13) % 95 + 32)
            else:
                result += char
        return result

    def double_encoding(self):
        msg = f"{self.chat_name}: {self.type_area.get('1.0', 'end')}"
        msg = self.encode_rot13(msg)
        self.sock.send(msg.encode('utf-8'))
        self.type_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def decode_rot13(self, text):
        result = ""
        for char in text:
            ascii_value = ord(char)
            if 32 <= ascii_value <= 126:  
                result += chr((ascii_value - 32 - 13) % 95 + 32)
            else:
                result += char
        return result

    def decrypt_message(self):
        texts = self.text_display.get(1.0, tkinter.END)
        decrypt_message = self.decode_rot13(texts)
        self.text_display.config(state='normal', bg="#C0C0C0")
        self.text_display.delete(1.0, tkinter.END)
        self.text_display.insert('end', decrypt_message)
        self.text_display.yview('end')
        self.text_display.config(state='disabled', bg="#C0C0C0")

    def listen(self):
        while self.running:
            try:
                msg = self.sock.recv(1024).decode('utf-8')

                if msg == 'CHAT':
                    self.sock.send(self.chat_name.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_display.config(state='normal', bg="#C0C0C0")
                        self.text_display.insert('end', msg)
                        self.text_display.yview('end')
                        self.text_display.config(
                            state='disabled', bg="#C0C0C0")
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break


client = Client(HOST, PORT)
