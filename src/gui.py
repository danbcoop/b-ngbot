import os
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk

import numpy as np
import pandas as pd
from dbfpy3 import dbf

from src.distributor import Dist, OrderList
from src.helper import *


class GUI:
    """GUI to interface the bot"""

    TITLE = "Bäng Bot 2.0"
    GEOMETRY = "600x400"
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

        root.title(f"{self.TITLE}")
        root.geometry(f"{self.GEOMETRY}")

        self.home_buttons = list()
        self.home_button_names = ["Import", "Export", "Lieferschein eingeben"]
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

        # self.status = tk.Label(root, text="Wähle die Bestelllisten und drücke Start.")

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
        # self.status.pack()
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
                error_text = f'"{dist.filename}" konnte nicht geöffnet werden.'
                tk.messagebox.showerror(title=None, message=error_text)
                self.status.config(text=error_text)
                return
        self._import_order_files()

    def _import_order_files(self):
        root = self.root

        # status = tk.Label(root, text="Wähle Importdateien und drücke Start.")

        for button in self.select_buttons:
            button.destroy()

        for label in self.labels:
            label.destroy()

        self.start_button.forget()
        self.col_options = list()
        self.option_labels = list()
        self.option_vars = list()

        dist = self.dists[0]
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

        self.start_button.config(command=lambda d=dist: self.next_frame(d))
        self.start_button.pack(expand=True)

        # self.dists[0].orderlist.reduce(["Code", "Retail", "Title", "IssueNumber"])
        # # self.dists[2].to_excel()
        # # x=self.dists[2].orderlist.get()
        # # static NDEX=0
        # # x=x.map(lambda _: INDEX+1)
        #
        # self.dists[0].orderlist.data.replace({"IssueNumber": np.nan}, 1, inplace=True)
        # self.dists[0].orderlist.data.dropna(inplace=True)
        # self.dists[0].orderlist.data.rename(
        #     columns={"IssueNumber": "Issue", "Retail": "Price"}, inplace=True
        # )
        # for i, row in self.dists[0].orderlist.data.iterrows():
        #     code = row.at["Code"]
        #     print(row)
        #     row.at["Code"] = remove_year(f"{code[4:6]}{code[0:4]}{code[6:]}")
        # # for i, row in self.dists[0].orderlist.data.iterrows():
        # #     print(row.at["Code"])
        #
        # # self.dists[0].to_excel()
        # options = self.dists[2].orderlist.cols()
        # selected_option = tk.StringVar(value=options[2])
        #
        # option_menu = tk.OptionMenu(
        #     root,
        #     selected_option,
        #     *options,
        #     command=lambda option: show_selection(selected_option),
        # )
        # option_menu.pack()
        # # self.start_button.config(text="Starte Import", command=lambda: print("TODO"))

        root.mainloop()

    def next_frame(self, dist):
        root = self.root
        self.start_button.forget()
        self.set_col_names(dist)
        try:
            dist = self.dists[dist.id + 1]
        except Exception:
            # Add MgCode
            self.start_button.destroy()
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
            for dist in self.dists:
                dist.process_import()
            write_to_dbf(self.dists)
            for dist in self.dists:
                dist.to_excel()
            tk.messagebox.showinfo(
                title=None, message="Import erfolgreich abgeschlossen!"
            )
            root.destroy()
            return

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
            self.col_options[i].set(default_col_name(dist, col))
            self.option_labels[i].pack()
            self.col_options[i].pack()

        self.start_button.config(command=lambda d=dist: self.next_frame(d))
        self.start_button.pack(expand=True)

    def set_col_names(self, dist):
        new_names = dict()
        for col in dist.colums():
            i = OrderList.COLUMN_NAMES.index(col)
            new_names[self.option_vars[i].get()] = col
            self.col_options[i].forget()
            self.option_labels[i].forget()

        dist.rename_and_drop(new_names)


def remove_year(s: str) -> str:
    return s[:4] + s[5:]


def write_to_dbf(orders):
    with dbf.Dbf("ami.dbf", new=True) as db:
        db.add_field(
            ("C", "POCODE", 9),
            ("C", "TITLE", 50),
            ("C", "ISSUE", 10),
            ("N", "PRICE", 9, 2),
            ("C", "SUPPLIER", 3),
            ("N", "GESAMTBEST", 5, 0),
            ("N", "TEMPORARY", 3, 0),
            ("C", "DISCCODE", 2),
        )
        for order in orders:
            for i, row in order.orderlist.data.iterrows():
                add_record(db, row, order.name)


def add_record(db, row, order):
    rec = db.new()
    match order:
        case "DIAMOND":
            rec["POCODE"] = row.at["Code"]
            rec["TITLE"] = row.at["Title"]
            rec["ISSUE"] = row.at["Issue"]
            rec["PRICE"] = float(row.at["Price"])
            rec["SUPPLIER"] = "DIA"
        case "DC":
            rec[b"POCODE"] = row.at["MgCode"]
            rec[b"TITLE"] = row.at["Title"]
            rec[b"ISSUE"] = row.at["Issue"]
            rec[b"PRICE"] = float(row.at["Price"])
            rec[b"SUPPLIER"] = "PEP"
        case "PRH":
            rec["POCODE"] = row.at["MgCode"]
            rec["TITLE"] = row.at["Title"]
            rec["ISSUE"] = row.at["Issue"]
            rec["PRICE"] = float(row.at["Price"])
            rec["SUPPLIER"] = "MOD"

    db.write(rec)


if __name__ == "__main__":
    GUI().run()
