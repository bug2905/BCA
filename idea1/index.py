import customtkinter as ctk
from tkinter import filedialog
import sys, io

# Sample topics
topics = {
    "If-Else": {
        "definition": "Decision making statement in Python. Executes code based on condition.",
        "syntax": "if condition:\n    # code\nelse:\n    # code"
    },
    "For Loop": {
        "definition": "Used for iterating over a sequence (like list, tuple, string).",
        "syntax": "for i in range(5):\n    print(i)"
    },
    "While Loop": {
        "definition": "Executes a block of code while a condition is true.",
        "syntax": "i = 1\nwhile i <= 5:\n    print(i)\n    i += 1"
    },
    "Functions": {
        "definition": "A block of reusable code in Python.",
        "syntax": "def function_name(params):\n    # code\n    return value"
    },
    "Lambda Function": {
        "definition": "Anonymous function defined using lambda keyword.",
        "syntax": "square = lambda x: x*x\nprint(square(5))"
    },
    "List": {
        "definition": "Collection which is ordered and changeable. Allows duplicates.",
        "syntax": "mylist = [1, 2, 3]\nprint(mylist[0])"
    },
    "Tuple": {
        "definition": "Ordered collection which is immutable. Allows duplicates.",
        "syntax": "mytuple = (1, 2, 3)\nprint(mytuple[0])"
    },
    "Set": {
        "definition": "Unordered collection which is unindexed. No duplicates.",
        "syntax": "myset = {1, 2, 3}\nprint(myset)"
    },
    "Dictionary": {
        "definition": "Stores data in key:value pairs. Unordered and changeable.",
        "syntax": "mydict = {'name':'Kushal','age':21}\nprint(mydict['name'])"
    },
    "Strings": {
        "definition": "Sequence of characters. Immutable.",
        "syntax": "name = 'Python'\nprint(name[0])"
    },
    "Class & Object": {
        "definition": "Class is a blueprint for creating objects.",
        "syntax": "class Person:\n    def __init__(self, name):\n        self.name = name\np1 = Person('Kushal')\nprint(p1.name)"
    },
    "Inheritance": {
        "definition": "Mechanism to inherit properties/methods from parent class.",
        "syntax": "class Parent:\n    def func(self):\n        print('Parent')\nclass Child(Parent):\n    pass\nc = Child()\nc.func()"
    },
    "Polymorphism": {
        "definition": "Ability to take many forms. Method overriding example.",
        "syntax": "class A:\n    def show(self):\n        print('A')\nclass B(A):\n    def show(self):\n        print('B')\nb = B()\nb.show()"
    },
    "Encapsulation": {
        "definition": "Restrict access to methods/variables using _ or __",
        "syntax": "class Test:\n    __private = 10\n    def get_val(self):\n        return self.__private\nt = Test()\nprint(t.get_val())"
    },
    "Exception Handling": {
        "definition": "Handle runtime errors using try-except blocks.",
        "syntax": "try:\n    print(5/0)\nexcept ZeroDivisionError:\n    print('Cannot divide by zero')"
    },
    "File Handling": {
        "definition": "Read/write files using open() function.",
        "syntax": "f = open('file.txt','w')\nf.write('Hello')\nf.close()"
    },
    "Modules & Packages": {
        "definition": "Organize code into modules and packages.",
        "syntax": "import math\nprint(math.sqrt(16))"
    },
    "Decorators": {
        "definition": "Function that modifies another function.",
        "syntax": "def decorator(func):\n    def wrapper():\n        print('Before')\n        func()\n        print('After')\n    return wrapper\n@decorator\ndef say():\n    print('Hello')\nsay()"
    },
    "Generators": {
        "definition": "Function that yields values lazily using yield keyword.",
        "syntax": "def gen():\n    for i in range(5):\n        yield i\nfor val in gen():\n    print(val)"
    },
    "List Comprehension": {
        "definition": "Shorter way to create lists.",
        "syntax": "squares = [x*x for x in range(5)]\nprint(squares)"
    },
    "Regular Expressions": {
        "definition": "Pattern matching in strings using re module.",
        "syntax": "import re\npattern = r'\\d+'\ntext = 'There are 12 cats'\nprint(re.findall(pattern,text))"
    }
}

# Functions
def show_topic(topic):
    def_text.configure(state="normal")
    def_text.delete("1.0", "end")
    def_text.insert("end", f"Definition:\n{topics[topic]['definition']}\n\nSyntax:\n{topics[topic]['syntax']}")
    def_text.configure(state="disabled")

def run_code():
    code = code_editor.get("1.0","end")
    output_text.configure(state="normal")
    output_text.delete("1.0","end")
    
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    try:
        exec(code, {}, {})
        sys.stdout = old_stdout
        output_text.insert("end", redirected_output.getvalue())
    except Exception as e:
        sys.stdout = old_stdout
        output_text.insert("end", f"Error: {e}")
    output_text.configure(state="disabled")

def save_code():
    file_path = filedialog.asksaveasfilename(defaultextension=".py",
                                             filetypes=[("Python Files","*.py"),("Text Files","*.txt")])
    if file_path:
        with open(file_path,"w",encoding="utf-8") as f:
            f.write(code_editor.get("1.0","end"))

def load_code():
    file_path = filedialog.askopenfilename(filetypes=[("Python Files","*.py"),("Text Files","*.txt")])
    if file_path:
        with open(file_path,"r",encoding="utf-8") as f:
            code_editor.delete("1.0","end")
            code_editor.insert("end",f.read())

# App Window
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title("Modern Learning App")
root.geometry("1000x600")

# Grid config
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=2)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# --- Part 1: Topics (Top-left, Scrollable) ---
frame1 = ctk.CTkFrame(root, corner_radius=15)
frame1.grid(row=0,column=0, sticky="nsew", padx=10,pady=10)

ctk.CTkLabel(frame1, text="📚 Topics", font=("Arial",16,"bold")).pack(pady=5)

scrollable_frame = ctk.CTkScrollableFrame(frame1)
scrollable_frame.pack(fill="both", expand=True, padx=5, pady=5)

for t in topics:
    ctk.CTkButton(scrollable_frame, text=t, command=lambda x=t: show_topic(x)).pack(fill="x", pady=2, padx=5)

# --- Part 2: Definition + Syntax (Top-right) ---
frame2 = ctk.CTkFrame(root, corner_radius=15)
frame2.grid(row=0,column=1, sticky="nsew", padx=10,pady=10)
ctk.CTkLabel(frame2, text="📖 Definition + Syntax", font=("Arial",16,"bold")).pack(pady=5)
def_text = ctk.CTkTextbox(frame2, wrap="word", height=15)
def_text.pack(fill="both", expand=True, padx=10,pady=10)
def_text.insert("end", "Select a topic to view details...")
def_text.configure(state="disabled")

# --- Part 3: Code Editor (Bottom-left) ---
frame3 = ctk.CTkFrame(root, corner_radius=15)
frame3.grid(row=1,column=0, sticky="nsew", padx=10,pady=10)
ctk.CTkLabel(frame3, text="💻 Code Editor", font=("Arial",16,"bold")).pack(pady=5)
code_editor = ctk.CTkTextbox(frame3, wrap="word")
code_editor.pack(fill="both", expand=True, padx=10,pady=5)

btn_frame = ctk.CTkFrame(frame3)
btn_frame.pack(pady=5)
ctk.CTkButton(btn_frame, text="💾 Save", command=save_code, width=80).pack(side="left", padx=5)
ctk.CTkButton(btn_frame, text="📂 Load", command=load_code, width=80).pack(side="left", padx=5)
ctk.CTkButton(btn_frame, text="▶ Run", command=run_code, width=80).pack(side="left", padx=5)

# --- Part 4: Output (Bottom-right) ---
frame4 = ctk.CTkFrame(root, corner_radius=15)
frame4.grid(row=1,column=1, sticky="nsew", padx=10,pady=10)
ctk.CTkLabel(frame4, text="🖥 Output", font=("Arial",16,"bold")).pack(pady=5)
output_text = ctk.CTkTextbox(frame4, wrap="word", fg_color="black", text_color="lime")
output_text.pack(fill="both", expand=True, padx=10,pady=10)
output_text.insert("end", "Output will appear here...")
output_text.configure(state="disabled")

root.mainloop()
