import customtkinter as ctk
from tkinter import filedialog
import sys, io

# --- Sample Data ---
topics = {
    "If-Else": {
        "definition": "Decision making statement in Python.",
        "syntax": "if condition:\n    # code\nelse:\n    # code"
    },
    "Loop": {
        "definition": "Used for repeating tasks.",
        "syntax": "for i in range(5):\n    print(i)"
    }
}

# --- Functions ---
def show_topic(topic):
    def_text.configure(state="normal")
    def_text.delete("1.0", "end")
    def_text.insert("end", f"Definition:\n{topics[topic]['definition']}\n\nSyntax:\n{topics[topic]['syntax']}")
    def_text.configure(state="disabled")

def run_code():
    code = code_editor.get("1.0", "end")
    output_text.configure(state="normal")
    output_text.delete("1.0", "end")
    
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
    file_path = filedialog.asksaveasfilename(
        defaultextension=".py",
        filetypes=[("Python Files", "*.py"), ("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code_editor.get("1.0", "end"))

def load_code():
    file_path = filedialog.askopenfilename(
        filetypes=[("Python Files", "*.py"), ("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            code_editor.delete("1.0", "end")
            code_editor.insert("end", f.read())

# --- App Window ---
ctk.set_appearance_mode("dark")   # "light", "dark", or "system"
ctk.set_default_color_theme("blue")  

root = ctk.CTk()
root.title("Modern Learning App")
root.geometry("1000x600")

# Grid config
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=2)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# --- Part 1: Topics (Top-left) ---
frame1 = ctk.CTkFrame(root, corner_radius=15)
frame1.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

ctk.CTkLabel(frame1, text="📚 Topics", font=("Arial", 16, "bold")).pack(pady=5)
for t in topics:
    ctk.CTkButton(frame1, text=t, command=lambda x=t: show_topic(x)).pack(fill="x", pady=5, padx=10)

# --- Part 2: Definition + Syntax (Top-right) ---
frame2 = ctk.CTkFrame(root, corner_radius=15)
frame2.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

ctk.CTkLabel(frame2, text="📖 Definition + Syntax", font=("Arial", 16, "bold")).pack(pady=5)
def_text = ctk.CTkTextbox(frame2, wrap="word", height=200)
def_text.pack(fill="both", expand=True, padx=10, pady=10)
def_text.insert("end", "Select a topic to view details...")
def_text.configure(state="disabled")

# --- Part 3: Code Editor (Bottom-left) ---
frame3 = ctk.CTkFrame(root, corner_radius=15)
frame3.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

ctk.CTkLabel(frame3, text="💻 Code Editor", font=("Arial", 16, "bold")).pack(pady=5)
code_editor = ctk.CTkTextbox(frame3, wrap="word")
code_editor.pack(fill="both", expand=True, padx=10, pady=10)

btn_frame = ctk.CTkFrame(frame3)
btn_frame.pack(pady=5)

ctk.CTkButton(btn_frame, text="💾 Save", command=save_code, width=80).pack(side="left", padx=5)
ctk.CTkButton(btn_frame, text="📂 Load", command=load_code, width=80).pack(side="left", padx=5)
ctk.CTkButton(btn_frame, text="▶ Run", command=run_code, width=80).pack(side="left", padx=5)

# --- Part 4: Output (Bottom-right) ---
frame4 = ctk.CTkFrame(root, corner_radius=15)
frame4.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

ctk.CTkLabel(frame4, text="🖥 Output", font=("Arial", 16, "bold")).pack(pady=5)
output_text = ctk.CTkTextbox(frame4, wrap="word", fg_color="black", text_color="lime")
output_text.pack(fill="both", expand=True, padx=10, pady=10)
output_text.insert("end", "Output will appear here...")
output_text.configure(state="disabled")

root.mainloop()
