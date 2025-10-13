import os
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk

from src.distributor import Dist


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

        if os.name == "posix":
            root.iconphoto(False, self.logo)
        else:  # Windows
            root.iconbitmap("./assets/bb_logo.ico")

        self.home_buttons = list()
        self.home_button_names = ["Import", "Export"]
        self.select_buttons = list()
        self.dists = list()
        self.labels = list()
        self.dists = list()
        self.start_button = tk.Button(
            root,
            text="Starte Import",
            command=lambda d=self.dists: print(
                f"{d[0].name}: {d[0].filename}\n"
                f"{d[1].name}: {d[1].filename}\n"
                f"{d[2].name}: {d[2].filename}"
            ),
        )

        for i, dist_name in enumerate(self.DIST):
            dist = Dist(dist_name, i)
            self.dists.append(dist)
            self.select_buttons.append(
                ttk.Button(
                    root,
                    text=f"Öffne {dist_name}-Datei",
                    command=lambda d=dist: self.select_file(d),
                )
            )
            self.labels.append(tk.Label(root, text=f"Noch keine Datei gewählt."))

    def run(self):
        root = self.root

        # There are three geometry managers: pack, grid, place
        self.logo_label.pack()

        for i, button_name in enumerate(self.home_button_names):
            self.home_buttons.append(
                ttk.Button(
                    root,
                    text=button_name,
                    command=lambda name=button_name: self.route_request(name),
                )
            )

        for button in self.home_buttons:
            button.pack(expand=True)

        root.mainloop()

    def show_import_frame(self):
        root = self.root

        for dist in self.dists:
            self.select_buttons[dist.id].pack(ipadx=20)
            self.labels[dist.id].pack()

        self.start_button.pack(expand=True)
        root.mainloop()

    def show_export_frame(self):
        pass

    def select_file(self, dist):
        filetypes = (
            ("text files", "*.md"),
            ("All files", "*.*"),
        )

        filename = fd.askopenfilename(
            title="Bitte Importdatei wählen",
            initialdir="./",
            filetypes=filetypes,
        )
        dist.filename = filename
        self.labels[dist.id].config(text=f"{dist.name}: {filename}")

    def route_request(self, request):
        print(request)
        match request:
            case "Import":
                for button in self.home_buttons:
                    button.forget()
                self.show_import_frame()
            case "Export":
                for button in self.home_buttons:
                    button.forget()
                self.show_export_frame()


if __name__ == "__main__":
    GUI().run()
