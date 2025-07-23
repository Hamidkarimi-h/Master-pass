import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip  

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Password Generator")
        self.root.geometry("450x350")
        self.root.resizable(False, False)

        # title
        ttk.Label(root, text="Password Generator", font=("Helvetica", 18, "bold")).pack(pady=10)

        #  password length
        length_frame = ttk.Frame(root)
        length_frame.pack(pady=5)
        ttk.Label(length_frame, text="Password Length: ").pack(side=tk.LEFT)
        self.length_var = tk.IntVar(value=12)
        self.length_spinbox = ttk.Spinbox(length_frame, from_=8, to=30, textvariable=self.length_var, width=5)
        self.length_spinbox.pack(side=tk.LEFT)

        # choose character
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_lowercase = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)

        char_frame = ttk.Frame(root)
        char_frame.pack(pady=10)

        ttk.Checkbutton(char_frame, text="Uppercase (A-Z)", variable=self.use_uppercase).grid(row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(char_frame, text="Lowercase (a-z)", variable=self.use_lowercase).grid(row=1, column=0, sticky=tk.W)
        ttk.Checkbutton(char_frame, text="Digits (0-9)", variable=self.use_digits).grid(row=0, column=1, sticky=tk.W)
        ttk.Checkbutton(char_frame, text="Symbols (!@#$)", variable=self.use_symbols).grid(row=1, column=1, sticky=tk.W)

        # generate password
        self.generate_btn = ttk.Button(root, text="Generate Password", command=self.generate_password)
        self.generate_btn.pack(pady=10)

        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(root, textvariable=self.password_var, font=("Helvetica", 14), width=30, state="readonly")
        self.password_entry.pack(pady=5)

        # copy
        self.copy_btn = ttk.Button(root, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_btn.pack(pady=5)

        
        self.strength_label = ttk.Label(root, text="Password Strength: ")
        self.strength_label.pack(pady=5)

    def generate_password(self):
        length = self.length_var.get()
        char_pool = ""

        if self.use_uppercase.get():
            char_pool += string.ascii_uppercase
        if self.use_lowercase.get():
            char_pool += string.ascii_lowercase
        if self.use_digits.get():
            char_pool += string.digits
        if self.use_symbols.get():
            char_pool += "!@#$%^&*()-_=+[]{}|;:,.<>?/"

        if not char_pool:
            messagebox.showerror("Error", "Please select at least one character set!")
            return

        password = "".join(random.choice(char_pool) for _ in range(length))
        self.password_var.set(password)

        strength = self.check_strength(password)
        self.strength_label.config(text=f"Password Strength: {strength}")

    def check_strength(self, password):
        length = len(password)
        categories = 0
        categories += any(c.islower() for c in password)
        categories += any(c.isupper() for c in password)
        categories += any(c.isdigit() for c in password)
        categories += any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for c in password)

        score = length + categories * 5

        if score < 15:
            return "Weak"
        elif score < 25:
            return "Medium"
        else:
            return "Strong"

    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No password to copy!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
