import os
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk


class Dist:
    def __init__(self, name, index, filename=""):
        self.name = name
        self.id = index
        self.filename = filename


class GUI:
    """GUI to interface the bot"""

    TITLE = "Bäng Bot 2.0"
    GEOMETRY = "600x400"
    LOGO = "./assets/bb_logo.png"
    ICON = "./assets/bb_logo.ico"

    # Button texts
    SELECT_DC = "Wähle DC-Datei"
    SELECT_MAR = "Wähle Marvel-Datei"

    DIST = [
        "Marvel",
        "Lunar",
        "Previews",
    ]

    def __init__(self):
        self.root = tk.Tk()
        root = self.root

        root.title(f"{self.TITLE}")
        root.geometry(f"{self.GEOMETRY}")

        self.logo = tk.PhotoImage(file=f"{self.LOGO}")
        self.logo_label = ttk.Label(root, image=self.logo, padding=5)

        self.select_buttons = list()
        self.dists = list()
        self.labels = list()
        self.start_button = tk.Button(
            root, text="Starte Import", command=lambda: print("start")
        )

        for i, dist_name in enumerate(self.DIST):
            dist = Dist(dist_name, i)
            self.dists.append(dist)
            self.select_buttons.append(
                ttk.Button(
                    root,
                    text=f"Öffne {dist_name}-Datei",
                    command=lambda: self.select_file(dist),
                )
            )
            self.labels.append(tk.Label(root, text=f"Noch keine Datei gewählt."))

    def run(self):
        root = self.root

        if os.name == "posix":
            root.iconphoto(False, self.logo)
        else:  # Windows
            root.iconbitmap("./assets/bb_logo.ico")

        # There are three geometry managers: pack, grid, place
        self.logo_label.pack()
        for dist in self.dists:
            self.select_buttons[dist.id].pack(ipadx=20)
            self.labels[dist.id].pack()

        self.start_button.pack(expand=True)
        root.mainloop()

    def select_file(self, dist):
        filetypes = (
            ("text files", "*.md"),
            ("All files", "*.*"),
        )

        filename = fd.askopenfilename(
            title="Bitte Datei wählen",
            initialdir="./",
            filetypes=filetypes,
        )
        dist.filename = filename
        self.labels[dist.id].config(text=filename)


if __name__ == "__main__":
    GUI().run()
