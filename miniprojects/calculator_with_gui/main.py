import tkinter as tk
import calculator

def click(event):
    global expression
    text = event.widget.cget("text")
    
    if text == "=": 
        try:
            result = eval(expression)
            entry_var.set(result)
            expression = str(result)
        except Exception:
            entry_var.set("Error")
            expression = ""
    elif text == "C":
        expression = ""
        entry_var.set("")
    else:
        expression += text
        entry_var.set(expression)

root = tk.Tk()
root.title("GUI Calculator")
expression = ""
entry_var = tk.StringVar()

entry = tk.Entry(root, textvar=entry_var, font="Arial 20", bd=10, relief="sunken")
entry.pack(fill="both", ipadx=8)

buttons = [
    ["7", "8", "9", "+"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "*"],
    ["0", "C", "=", "/"]
]

for row in buttons:
    frame = tk.Frame(root)
    frame.pack()
    for text in row:
        b = tk.Button(frame, text=text, font="Arial 18", width=5, height=2)
        b.pack(side="left")
        b.bind("<Button-1>", click)

root.mainloop()
