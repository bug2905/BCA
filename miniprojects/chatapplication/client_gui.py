# client_gui.py
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("LAN Chat Application")
        self.master.geometry("400x500")

        # Chat display area
        self.chat_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, state="disabled")
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Message entry
        self.entry = tk.Entry(self.master, width=40)
        self.entry.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.send_message)

        # Send button
        self.send_button = tk.Button(self.master, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Ask for server IP & username
        self.server_ip = simpledialog.askstring("Server IP", "Enter server IP:")
        self.username = simpledialog.askstring("Username", "Choose a username:")

        # Connect to server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, 12345))

        # Start listening thread
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self, event=None):
        message = f"{self.username}: {self.entry.get()}"
        try:
            self.client_socket.send(message.encode("utf-8"))
            self.display_message(message)  # <-- show own message instantly
            self.entry.delete(0, tk.END)
        except:
            self.display_message("❌ Message not sent (connection error)")


    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode("utf-8")
                self.display_message(message)
            except:
                break

    def display_message(self, message):
        self.chat_area.config(state="normal")
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.yview(tk.END)
        self.chat_area.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
