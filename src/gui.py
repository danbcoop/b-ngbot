import os
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk

from src.distributor import Dist


def ospath(path: str) -> str:
    if os.name == "posix":
        return path
    else:  # Windows
        return path.replace("/", "\\")


FILESDIR = ospath("./files")


class GUI:
    """GUI to interface the bot"""

    TITLE = "Bäng Bot 2.0"
    GEOMETRY = "600x400"
    LOGO = ospath("./assets/bb_logo.png")
    ICON = ospath("./assets/bb_logo.ico")
    DIST_NAMES = [
        "DC",
        "DIAMOND",
        "PRH",
    ]

    def __init__(self):
        self.root = tk.Tk()
        root = self.root

        root.title(f"{self.TITLE}")
        root.geometry(f"{self.GEOMETRY}")

        self.home_buttons = list()
        self.home_button_names = ["Import", "Export"]
        self.select_buttons = list()
        self.dists = list()
        self.labels = list()

        self.logo = tk.PhotoImage(file=f"{self.LOGO}")
        self.logo_label = ttk.Label(root, image=self.logo, padding=5)

        if os.name == "posix":
            root.iconphoto(False, self.logo)
        else:  # Windows
            root.iconbitmap(LOGO)

    def run(self):
        root = self.root

        # There are three geometry managers: pack, grid, place
        self.logo_label.pack()

        for button_name in self.home_button_names:
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

        self.status = tk.Label(root, text="Wähle Importdateien und drücke Start.")

        for i, dist_name in enumerate(self.DIST_NAMES):
            dist = Dist(dist_name, i)
            self.dists.append(dist)
            self.select_buttons.append(
                ttk.Button(
                    root,
                    text=f"Wähle {dist_name}-Datei",
                    command=lambda d=dist: self.select_file(d),
                )
            )
            self.labels.append(
                tk.Label(root, text=f"{dist_name}: {default_filename(dist)}")
            )

        self.start_button = tk.Button(
            root,
            text="Weiter",
            command=self.import_order_files,
        )

        for dist in self.dists:
            self.labels[dist.id].pack()
            self.select_buttons[dist.id].pack(ipadx=20)

        self.start_button.pack(expand=True)
        self.status.pack()
        root.mainloop()

    def show_export_frame(self):
        pass

    def select_file(self, dist):
        filetypes = (
            ("Tabellen", "*.xls*"),
            ("All files", "*.*"),
        )

        filename = fd.askopenfilename(
            title="Bitte Importdatei wählen",
            initialdir=FILESDIR,
            filetypes=filetypes,
        )
        dist.filename = filename
        self.labels[dist.id].config(text=f"{dist.name}: {filename}")

    def route_request(self, request):
        match request:
            case "Import":
                for button in self.home_buttons:
                    button.forget()
                self.show_import_frame()
            case "Export":
                for button in self.home_buttons:
                    button.forget()
                self.show_export_frame()

    def import_order_files(self):
        for dist in self.dists:
            dist.load()
            if dist.orderlist.empty:
                self.status.config(text=f"{dist.filename} konnte nicht geladen werden")
                return
        self._import_order_files()


    def _import_order_files(self):
        root = self.root

        status = tk.Label(root, text="Wähle Importdateien und drücke Start.")

        for button in self.select_buttons:
            button.forget()

        for label in self.labels:
            label.forget()

        def show_selection(option):
            print(f"Selected option: {option.get()}")

        self.dists[0].orderlist.reduce(["Code", "Retail", "Title", "IssueNumber"])
        # self.dists[2].to_excel()
        # x=self.dists[2].orderlist.get()
        # static NDEX=0
        # x=x.map(lambda _: INDEX+1)
        for i, row in self.dists[0].orderlist.data.iterrows():
            code = row.at['Code']
            row.at['Code'] = f"{code[4:6]}{code[0:4]}{code[6:]}"
        for i, row in self.dists[0].orderlist.data.iterrows():
            print(row.at['Code'])
        options = self.dists[2].orderlist.cols()
        selected_option = tk.StringVar(value=options[2])

        option_menu = tk.OptionMenu(
            root,
            selected_option,
            *options,
            command=lambda option: show_selection(selected_option),
        )
        option_menu.pack()
        # self.start_button.config(text="Starte Import", command=lambda: print("TODO"))

        root.mainloop()


def default_filename(dist: Dist) -> str:
    ls = os.listdir(FILESDIR)
    for filename in ls:
        if candidate_found(filename, [dist.name]):
            filename = os.path.join(FILESDIR, filename)
            dist.filename = filename
            return filename

    return "Bitte eine Bestellliste wählen."


def candidate_found(find_in: str, find: list[str]) -> bool:
    for s in find:
        print(f"suche {s} in {find_in}")
        if find_in.find(s) >= 0:
            return True
    return False


if __name__ == "__main__":
    GUI().run()
