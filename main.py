import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import webbrowser
import re
import json
import os


# ===============================
# Config
# ===============================

JSON_FILE = "UserNames.json"


# ===============================
# Launcher Class
# ===============================

class CPLauncher:

    def __init__(self, root):
        self.root = root

        self.root.title("CP Launcher")
        self.root.geometry("500x280")
        self.root.configure(bg="#181825")
        self.root.resizable(False, False)

        self.setup_style()
        self.create_ui()

        self.json_file = JSON_FILE
        self.ensure_json_exists()

    # ===============================
    # JSON System
    # ===============================

    def ensure_json_exists(self):
        if not os.path.exists(self.json_file):
            data = {
                "CF": "",
                "LOJ": "",
                "LC": "",
                "CC": "",
                "AT": "",
                "HR": "",
                "CSES": ""
            }

            with open(self.json_file, "w") as f:
                json.dump(data, f, indent=4)

    def load_accounts(self):
        with open(self.json_file) as f:
            return json.load(f)

    def save_accounts(self, data):
        with open(self.json_file, "w") as f:
            json.dump(data, f, indent=4)

    # ===============================
    # Style (Ultra Clean Theme)
    # ===============================

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background="#181825")

        style.configure("TLabel",
                        background="#181825",
                        foreground="#cdd6f4",
                        font=("Segoe UI", 11))

        style.configure("TEntry",
                        fieldbackground="#1e1e2e",
                        foreground="#cdd6f4",
                        insertcolor="#89b4fa")

        style.configure("TButton",
                        font=("Segoe UI", 10, "bold"),
                        padding=6)

    # ===============================
    # UI
    # ===============================

    def create_ui(self):

        ttk.Label(
            self.root,
            text="CP Launcher",
            font=("Segoe UI", 18, "bold"),
            foreground="#89b4fa"
        ).pack(pady=18)

        # Input box
        frame = ttk.Frame(self.root)
        frame.pack(fill="x", padx=60)

        self.entry = ttk.Entry(frame, justify="center")
        self.entry.pack(fill="x", ipady=6)

        self.entry.insert(0, "CF 1985F")
        self.entry.bind("<Return>", lambda e: self.open_any())

        # Buttons
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=20)

        ttk.Button(
            btn_frame,
            text="Open Problem",
            command=self.open_any
        ).pack(pady=4)

        ttk.Button(
            btn_frame,
            text="Link Account",
            command=self.link_account_dialog
        ).pack(pady=4)

        ttk.Button(
            btn_frame,
            text="Open Profile",
            command=self.open_profile
        ).pack(pady=4)

        self.status = ttk.Label(self.root, text="")
        self.status.pack()

    # ===============================
    # Account Linking
    # ===============================

    def link_account_dialog(self):

        platform = simpledialog.askstring(
            "Platform",
            "Enter platform (CF/LOJ/LC/CC/AT/HR/CSES)"
        )

        if not platform:
            return

        username = simpledialog.askstring(
            "Username",
            "Enter username or ID"
        )

        if not username:
            return

        data = self.load_accounts()
        data[platform.upper()] = username
        self.save_accounts(data)

        messagebox.showinfo("Success", "Account Linked")

    # ===============================
    # Problem Opening
    # ===============================

    def open_any(self):

        text = self.entry.get().strip()
        parts = text.split(maxsplit=1)

        if len(parts) < 2:
            return

        platform = parts[0].upper()
        code = parts[1]

        accounts = self.load_accounts()

        url = None

        if platform == "CF":
            m = re.match(r"(\d+)([A-Za-z]+)", code)

            if m:
                contest, letter = m.groups()

                handle = accounts.get("CF", "")

                base = f"https://codeforces.com/problemset/problem/{contest}/{letter.upper()}"

                url = base + (f"?handle={handle}" if handle else "")

        elif platform == "LOJ":
            url = f"https://lightoj.com/problem/{code}"

        elif platform == "LC":
            url = f"https://leetcode.com/problems/{code.lower().replace(' ', '-')}"

        elif platform == "CC":
            url = f"https://www.codechef.com/problems/{code.upper()}"

        elif platform == "AT":
            url = f"https://atcoder.jp/contests/{code.split('_')[0]}/tasks/{code.lower()}"

        elif platform == "HR":
            url = f"https://www.hackerrank.com/challenges/{code.lower().replace(' ', '-')}"

        elif platform == "CSES":
            if code.isdigit():
                url = f"https://cses.fi/problemset/task/{code}"

        if url:
            webbrowser.open_new_tab(url)
            self.status.config(text="Opened ✔", foreground="#a6e3a1")

    # ===============================
    # Profile Open
    # ===============================

    def open_profile(self):

        platform = simpledialog.askstring(
            "Profile",
            "Platform?"
        )

        if not platform:
            return

        platform = platform.upper()

        accounts = self.load_accounts()
        username = accounts.get(platform)

        if not username:
            messagebox.showinfo("Info", "Account not linked")
            return

        urls = {
            "CF": f"https://codeforces.com/profile/{username}",
            "LOJ": f"https://lightoj.com/user/{username}",
            "LC": f"https://leetcode.com/{username}",
            "CC": f"https://www.codechef.com/users/{username}",
            "AT": f"https://atcoder.jp/users/{username}",
            "HR": f"https://www.hackerrank.com/{username}",
            "CSES": f"https://cses.fi/user/{username}"
        }

        if platform in urls:
            webbrowser.open_new_tab(urls[platform])


# ===============================
# MAIN
# ===============================

if __name__ == "__main__":
    root = tk.Tk()
    CPLauncher(root)
    root.mainloop()
