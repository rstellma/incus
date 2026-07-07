#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess

import incus as inc
import classify as cls

class IncusManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Incus Instance Launcher")

        # MUST EXIST BEFORE UI CALLBACKS
        self.sort_reverse = {
            "name": False,
            "status": False,
            "type": False,
        }

        self.build_ui()
        self.refresh()

    def build_ui(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill="both", expand=True)

        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("name", "status", "type"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=self.tree.yview)

        self.tree.heading("name", text="Name", command=lambda: self.sort_by("name"))
        self.tree.heading("status", text="Status", command=lambda: self.sort_by("status"))
        self.tree.heading("type", text="Type", command=lambda: self.sort_by("type"))

        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.tree.configure(height=15)

        btns = ttk.Frame(frame)
        btns.pack(fill="x", pady=(10, 0))

        self.desk_btn = ttk.Button(btns,text="Desktop",command=self.start_desktop,)
        self.desk_btn.pack(side="left", padx=2)

        self.start_btn = ttk.Button(btns, text="Start", command=self.start)
        self.start_btn.pack(side="left", padx=2)

        self.stop_btn =  ttk.Button(btns, text="Stop", command=self.stop)
        self.stop_btn.pack(side="left", padx=2)

        self.shell_btn = ttk.Button(btns, text="Shell", command=self.shell)
        self.shell_btn.pack(side="left")

        ttk.Button(btns, text="Refresh", command=self.refresh).pack(side="right")

    def sort_by(self, col):
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]

        # numeric-safe fallback (alles als string)
        items.sort(reverse=self.sort_reverse[col])

        for index, (_, k) in enumerate(items):
            self.tree.move(k, "", index)

        self.sort_reverse[col] = not self.sort_reverse[col]


    def refresh(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        try:
            instances = inc.list_instances()
        except Exception as e:
            messagebox.showerror("Incus Error", str(e))
            return

        for inst in instances:
            name = inst["name"]
            status = inst["status"]

            profiles = inst.get("profiles", [])
            ctype = cls.classify(profiles)

            self.tree.insert(
                "",
                "end",
                iid=name,
                values=(name, status, ctype)
            )

        self.update_buttons()


    def update_buttons(self):
        name = self.selected()
        if not name:
            self.start_btn.state(["disabled"])
            self.stop_btn.state(["disabled"])
            self.shell_btn.state(["disabled"])
            self.desk_btn.state(["disabled"])
            return

        status = self.tree.set(name, "status").lower()
        ctype = self.tree.set(name, "type").lower()

        is_running = status == "running"
        is_desktop = ctype == "desktop"

        # Start
        if is_running:
            self.start_btn.state(["disabled"])
        else:
            self.start_btn.state(["!disabled"])

        # Stop + Shell
        if is_running:
            self.stop_btn.state(["!disabled"])
            self.shell_btn.state(["!disabled"])
        else:
            self.stop_btn.state(["disabled"])
            self.shell_btn.state(["disabled"])

        # Desktop
        if is_running and is_desktop:
            self.desk_btn.state(["!disabled"])
        else:
            self.desk_btn.state(["disabled"])


    def selected(self):
        sel = self.tree.selection()
        if not sel:
            return None
        return sel[0]


    def start_desktop(self):
        name = self.selected()
        if not name:
            return

        try:
            inst = inc.get_instance(name)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        status = inst["status"].lower()
        profiles = inst.get("profiles", [])
        ctype = cls.classify(profiles)

        if status != "running":
            messagebox.showwarning(
                "Instance not running",
                "Desktop can only be started for running instances."
            )
            return

        if ctype != "desktop":
            messagebox.showwarning(
                "Not a desktop",
                "Selected instance is not classified as desktop."
            )
            return

        # Display + auth handling (vereinfachte Variante)
        display = ":1"  # oder später dynamisch aus manager state

        xauth_file = f"/tmp/xephyr.{name}.Xauthority"

        cmd = [
            "xterm",
            "-e",
            "bash",
            "-c",
            (
                f"export DISPLAY={display} && "
                f"export XAUTHORITY={xauth_file} && "
                f"incus exec {name} -- startfluxbox"
            )
        ]

        subprocess.Popen(cmd)


    def start(self):
        name = self.selected()
        if not name:
            return

        try:
            inc.start_instance(name)
        except Exception as e:
            messagebox.showerror("Start failed", str(e))

        self.refresh()


    def stop(self):
        name = self.selected()
        if not name:
            return

        try:
            inc.stop_instance(name)
        except Exception as e:
            messagebox.showerror("Stop failed", str(e))

        self.refresh()


    def shell(self):
        name = self.selected()
        if not name:
            return

        subprocess.Popen([
            "xterm",
            "-e",
            "incus",
            "exec",
            name,
            "--",
            "bash"
        ])


    def on_select(self, event=None):
        #pass  # bewusst leer gehalten (keine Business Logik hier)
        self.update_buttons()

def main():
    root = tk.Tk()
    app = IncusManagerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
