import os
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk

import numpy as np
import pandas as pd

from src.distributor import Dist, OrderList
from src.helper import (
    FILESDIR,
    default_col_name,
    default_filename,
    default_invoice,
    default_start_string,
    ospath,
    type_invoice,
    write_to_dbf,
)


class GUI:
    """GUI to interface the bot"""

    TITLE = "Bäng Bot 2.0"
    GEOMETRY = "600x450"
    LOGO = ospath("./assets/bb_logo.png")
    ICON = ospath("./assets/bb_logo.ico")
    DIST_NAMES = [
        "DIAMOND",
        "DC",
        "PRH",
    ]

    def __init__(self):
        self.root = tk.Tk()
        root = self.root

        root.frame = tk.StringVar(root, name="frame")
        root.frame.trace_add(mode=("write"), callback=self.update_frame)

        root.title(f"{GUI.TITLE}")
        root.geometry(f"{GUI.GEOMETRY}")
        self.logo = tk.PhotoImage(file=f"{GUI.LOGO}")
        logo_label = ttk.Label(root, image=self.logo, padding=5)
        logo_label.pack()

        if os.name == "posix":
            root.iconphoto(False, self.logo)
        else:  # Windows
            root.iconbitmap(GUI.ICON)

        self.dists = list()
        self.dists_prepared = list()
        for i, dist_name in enumerate(self.DIST_NAMES):
            dist = Dist(dist_name, i)
            self.dists.append(dist)

    def run(self):
        self.current = HomeFrame(self.root)

        self.root.mainloop()

    def update_frame(self, a, b, c):
        self.current.destroy()
        match self.root.frame.get():
            case "Home":
                self.current = HomeFrame(self.root)
            case "Import":
                self.current = FilenameFrame(self.root, self.dists)
            case "Cols":
                if not self.dists:
                    self.dists = self.dists_prepared
                    self.finish_import()
                    self.root.quit()
                else:
                    if not self.dists_prepared:
                        self.dists.reverse()
                    dist = self.dists.pop()
                    self.current = ColsFrame(self.root, dist)
                    self.dists_prepared.append(dist)
            case "Lieferschein eintippen":
                self.current = TypeInFrame(self.root)

            # case "Export":
            #     self.current = ExportFrame(self.root, self.dists)
            case _:
                self.root.quit()

    def finish_import(self):
        self.add_mg_codes()
        for dist in self.dists:
            dist.process_import()
        write_to_dbf(self.dists)
        for dist in self.dists:
            dist.to_excel()
        tk.messagebox.showinfo(title=None, message="Import erfolgreich abgeschlossen!")

    def add_mg_codes(self):
        start = self.dists[0].orderlist.data.shape[0] + 1
        end = start + self.dists[1].orderlist.data.shape[0]
        mgcodes = list()
        for i in np.arange(start, end):
            mgcodes.append(f"{Dist.DATE}{i:04}")

        self.dists[1].orderlist.data = pd.concat(
            [
                self.dists[1].orderlist.data,
                pd.DataFrame(mgcodes, columns=["MgCode"]),
            ],
            axis=1,
        )
        start = end + 1
        end = start + self.dists[2].orderlist.data.shape[0]
        mgcodes = list()
        for i in np.arange(start, end):
            mgcodes.append(f"{Dist.DATE}{i:04}")

        self.dists[2].orderlist.data = pd.concat(
            [
                self.dists[2].orderlist.data,
                pd.DataFrame(mgcodes, columns=["MgCode"]),
            ],
            axis=1,
        )


class HomeFrame:
    def __init__(self, root):
        self.buttons = list()

        for button_text in ["Import", "Export", "Lieferschein eintippen"]:
            button = ttk.Button(
                root,
                text=button_text,
                command=lambda choice=button_text: root.frame.set(choice),
            )
            button.pack(expand=True)
            self.buttons.append(button)

    def destroy(self):
        for button in self.buttons:
            button.destroy()


class FilenameFrame:
    def __init__(self, root, dists):
        self.buttons = list()
        self.labels = list()
        self.spaces = list()
        for dist in dists:
            self.buttons.append(
                ttk.Button(
                    root,
                    text=f"Auswahl für {dist.name}-Datei ändern",
                    command=lambda d=dist: self.select_file(d),
                )
            )
            self.labels.append(
                tk.Label(root, text=f"{dist.name}: {default_filename(dist)}")
            )
            self.spaces.append(tk.Label(root, text=""))

        start_button = tk.Button(
            root,
            text="Weiter",
            command=lambda: self.import_selection(root, dists),
        )
        self.buttons.append(start_button)

        for dist in dists:
            self.labels[dist.id].pack(ipadx=10)
            self.buttons[dist.id].pack(ipadx=20)
            self.spaces[dist.id].pack()

        start_button.pack(expand=True)

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

    def import_selection(self, root, dists):
        for dist in dists:
            dist.load()
            if dist.orderlist.empty:
                error_text = f'"{dist.filename}" konnte nicht geöffnet werden.'
                tk.messagebox.showerror(title=None, message=error_text)
                root.frame.set("Import")
                return
        root.frame.set("Cols")

    def destroy(self):
        for element in self.buttons + self.labels + self.spaces:
            element.destroy()


class ExportFrame:
    def __init__(self, root, dists):
        pass

        # data = pd.read_csv(ospath("bin/PRH"),dtype=str,delimiter=";")
        # fn = os.path.join(FILESDIR, "MOD.DBF")
        # with dbf.Dbf(fn) as db:
        #     for record in db:
        #         data.loc[data['code'] == record['POCODE']]['Qty'][0] = record['Menge']


class ColsFrame:
    def __init__(self, root, dist):
        self.col_options = list()
        self.option_labels = list()
        self.option_vars = list()

        options = dist.orderlist.cols()

        for col in OrderList.COLUMN_NAMES:
            selected_option = tk.StringVar(value=default_col_name(dist, col))
            self.option_vars.append(selected_option)
            self.col_options.append(
                ttk.Combobox(root, textvariable=selected_option, state="readonly")
            )
            self.option_labels.append(tk.Label(root, text=f"{col}:"))

        for col in dist.colums():
            i = OrderList.COLUMN_NAMES.index(col)
            self.col_options[i]["values"] = options
            self.option_labels[i].pack()
            self.col_options[i].pack()

        cont_button = ttk.Button(
            root,
            text="Weiter",
            command=lambda: self.cont(dist, root.frame),
        )
        self.option_labels.append(cont_button)
        cont_button.pack(expand=True)

    def destroy(self):
        for element in self.col_options + self.option_labels:
            element.destroy()

    def cont(self, dist, frame):
        self.set_col_names(dist)
        frame.set("Cols")

    def set_col_names(self, dist):
        new_names = dict()
        for col in dist.colums():
            i = OrderList.COLUMN_NAMES.index(col)
            new_names[self.option_vars[i].get()] = col

        dist.rename_and_drop(new_names)


class TypeInFrame:
    def __init__(self, root):
        self.elements = list()
        self.invoice = default_invoice()
        self.elements.append(
            ttk.Button(
                root,
                text="Bitte Lieferschein wählen",
                command=lambda: self.select_file(),
            )
        )
        self.elements.append(tk.Label(root, text=f"{self.invoice}"))

        for element in self.elements:
            element.pack()

        tk.Label(root, text="", pady=10).pack()
        start_entry_label = tk.Label(root, text="Starte Eingabe ab:")
        start_entry_label.pack()
        self.start_entry = ttk.Entry(
            root,
        )
        self.start_entry.insert(0, default_start_string())
        self.start_entry.pack()
        start_button = tk.Button(
            root,
            text="Start",
            command=self.start,
        )
        self.elements.append(start_button)

        start_button.pack(expand=True)

    def select_file(self):
        filetypes = (
            ("Tabellen", "*.pdf"),
            ("All files", "*.*"),
        )

        filename = fd.askopenfilename(
            title="Bitte Lieferschein wählen",
            initialdir=FILESDIR,
            filetypes=filetypes,
        )
        self.invoice = filename
        self.elements[1].config(text=f"{self.invoice}")

    def start(self):
        if os.path.isfile(self.invoice):
            try:
                type_invoice(self.invoice, self.start_entry.get())
            except LookupError as err:
                tk.messagebox.showwarning(title=None, message=err.args[0])
        else:
            error_text = f'"{self.invoice}" ist kein gültiger Dateipfad.'
            tk.messagebox.showerror(title=None, message=error_text)

    def destroy(self):
        for element in self.elements + [self.start_entry]:
            element.destroy()


if __name__ == "__main__":
    GUI().run()
