import os
import tkinter as tk
from tkinter import ttk


class GUI:
    """GUI to interface the bot"""

    TITLE = "Bäng Bot 2.0"
    # GEOMETRY = "300x200"
    LOGO = "./assets/bb_logo.png"
    ICON = "./assets/bb_logo.ico"

    def __init__(self):
        self.root = tk.Tk()
        root = self.root

        root.title(f"{self.TITLE}")
        # root.geometry(f"{self.GEOMETRY}")

        self.message = tk.Label(root, text="Hello, World!")
        self.logo = tk.PhotoImage(file=f"{self.LOGO}")
        self.logo_label = ttk.Label(root, image=self.logo, padding=5)

    def run(self):
        root = self.root

        if os.name == "posix":
            root.iconphoto(False, self.logo)
        else:  # Windows
            root.iconbitmap("./assets/bb_logo.ico")

        # There are three geometry managers: pack, grid, place
        self.logo_label.pack()
        self.message.pack()

        root.mainloop()


if __name__ == "__main__":
    GUI().run()
