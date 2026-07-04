#!/usr/bin/env python3

import csv
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
#import yaml
import json

PROFILE_CLASSES = [
    ("10-Env_Desktop", "desktop"),
    ("20-Apps_", "app"),
    ("30-Dev_", "development"),
]

def classify_profiles(profiles):
    """
    Determine the logical container type from its assigned profiles.

    Returns:
        "desktop"
        "app"
        "development"
        None        -> container shall not be shown
    """
    for prefix, kind in PROFILE_CLASSES:
        if prefix.endswith("_"):
            if any(p.startswith(prefix) for p in profiles):
                return kind
        else:
            if prefix in profiles:
                return kind

    return None


class IncusDesktopManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Incus Desktop Manager")

        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            frame,
            columns=("status", "type"),
            show="headings",
            height=15,
        )
        self.tree.bind(
	    "<<TreeviewSelect>>",
	    self.on_container_selected
	)

        self.tree.heading("status", text="Status")
        self.tree.heading("type", text="Type")

        self.tree.column("status", width=100, anchor="center")
        self.tree.column("type", width=100, anchor="center")

        self.tree["show"] = "tree headings"
        self.tree.heading("#0", text="Container")

        self.tree.pack(fill="both", expand=True)

        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", pady=(10, 0))

        self.desk_btn = ttk.Button(
            button_frame,
            text="Start Desktop",
            command=self.start_desktop,
        )
        self.desk_btn.pack(side="left", padx=2)

        self.start_btn = ttk.Button(
            button_frame,
            text="Start",
            command=self.start_container,
        )
        self.start_btn.pack(side="left", padx=2)

        self.stop_btn = ttk.Button(
            button_frame,
            text="Stop",
            command=self.stop_container,
        )
        self.stop_btn.pack(side="left", padx=2)

        self.shell_btn = ttk.Button(
            button_frame,
            text="Shell",
            command=self.open_shell,
        )
        self.shell_btn.pack(side="left", padx=2)

        self.refresh_btn = ttk.Button(
            button_frame,
            text="Refresh",
            command=self.refresh,
        )
        self.refresh_btn.pack(side="right", padx=2)

    def on_container_selected(self, event=None):
        selection = self.tree.selection()
        status = self.selected_container_status()
        cnt_type = self.selected_container_type()

        if status == "running":
            self.start_btn.state(["disabled"])
            self.stop_btn.state(["!disabled"])
            self.shell_btn.state(["!disabled"])
            if cnt_type == "desktop":
                self.desk_btn.state(["!disabled"])
            else:
                self.desk_btn.state(["disabled"])
        elif status == "stopped":
            self.start_btn.state(["!disabled"])
            self.stop_btn.state(["disabled"])
            self.shell_btn.state(["disabled"])
            self.desk_btn.state(["disabled"])
        else:
            self.start_btn.state(["disabled"])
            self.stop_btn.state(["disabled"])
            self.shell_btn.state(["disabled"])
            self.desk_btn.state(["disabled"])

    def selected_container(self):
        selection = self.tree.selection()

        if not selection:
            messagebox.showwarning(
                "No selection",
                "Please select a container."
            )
            return None

        return selection[0]

    def selected_container_status(self):
        cur_item = self.tree.selection()

        if not cur_item:
            return None

        values = self.tree.item(cur_item[0])["values"]

        if not values:
            return None

        return values[0].lower()

    def selected_container_type(self):
        cur_item = self.tree.selection()

        if not cur_item:
            return None

        values = self.tree.item(cur_item[0])["values"]

        if not values:
            return None

        return values[1].lower()

    def run_command(self, cmd):
        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
        )

    def refresh(self):
        for item in list(self.tree.get_children()):
            self.tree.delete(item)

        result = self.run_command(
            [
                "incus",
                "list",
                "--format=json",
            ]
        )

        if result.returncode != 0:
            messagebox.showerror(
                "Incus Error",
                result.stderr,
            )
            return

        try:
            containers = json.loads(result.stdout)
        except json.JSONDecodeError:
            messagebox.showerror(
                "Parse Error",
                "Invalid JSON from incus list",
            )
            return

        for c in containers:
            name = c.get("name")
            status = c.get("status", "").lower()
            profiles = c.get("profiles", [])

            if not name:
                continue

            ctype = classify_profiles(profiles)
            if ctype is None:
                continue

            self.tree.insert(
                "",
                "end",
                iid=name,
                text=name,
                values=(status, ctype),
            )

        self.start_btn.state(["disabled"])
        self.stop_btn.state(["disabled"])
        self.shell_btn.state(["disabled"])
        self.desk_btn.state(["disabled"])

    def start_desktop(self):
        name = self.selected_container()

        if not name:
            return

        subprocess.Popen(
            [
                "xterm",
                "-e",
                "incus-orchestrator",
                name,
            ]
        )

    def start_container(self):
        name = self.selected_container()
        status = self.selected_container_status()

        if not name:
            return

        result = self.run_command(
            [
                "incus",
                "start",
                name,
            ]
        )

        if result.returncode != 0:
            messagebox.showerror(
                "Start failed",
                result.stderr,
            )
            return

        self.refresh()

    def stop_container(self):
        name = self.selected_container()

        if not name:
            return

        result = self.run_command(
            [
                "incus",
                "stop",
                name,
            ]
        )

        if result.returncode != 0:
            messagebox.showerror(
                "Stop failed",
                result.stderr,
            )
            return

        self.refresh()

    def open_shell(self):
        name = self.selected_container()

        if not name:
            return

        subprocess.Popen(
            [
                "xterm",
                "-e",
                "incus",
                "exec",
                name,
                "--",
                "bash",
            ]
        )


def main():
    root = tk.Tk()

    try:
        root.tk.call("tk", "scaling", 1.25)
    except Exception:
        pass

    app = IncusDesktopManager(root)

    root.mainloop()


if __name__ == "__main__":
    main()
