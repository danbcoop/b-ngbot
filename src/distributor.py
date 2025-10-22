import os

import numpy as np
import pandas as pd

CROSSOUT = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"


class Dist:
    DATE = ""

    def __init__(self, name, index, filename=""):
        self.name = name
        self.id = index
        self.filename = filename
        self.orderlist = OrderList("", "")
        self.col_names = {
            "Code": ["Code", "MainIdentifier", "DIAMD_NO"],
            "Title": ["Title", "FULL_TITLE"],
            "Issue": ["IssueNumber", "SeriesNumber"],
            "Price": ["PriceUSD", "Retail", "PRICE"],
            "Incentives": ["RATIO VARIANTS"],
        }

    def load(self):
        self.orderlist = OrderList(self.filename, self.name)

    def rename_and_drop(self, new_names):
        self.orderlist.rename_and_drop(new_names, self.name)
        if self.name == "DIAMOND":
            date = self.orderlist.data.at[0, "Code"]
            Dist.DATE = date[:5]

    def to_excel(self):
        self.orderlist.to_excel(self.filename)

    def reduce(self):
        self.orderlist.reduce(self.colums())

    def colums(self):
        match self.name:
            case "DIAMOND":
                return [
                    "Title",
                    "Price",
                    "Code",
                ]
            case "DC":
                return [
                    "Title",
                    "Issue",
                    "Price",
                    "Code",
                ]
            case "PRH":
                return [
                    "Title",
                    "Issue",
                    "Price",
                    "Code",
                    "Incentives",
                ]

    def process_import(self):
        self.orderlist.process_import()


class OrderList:
    COLUMN_NAMES = [
        "Title",
        "Issue",
        "Price",
        "Code",
        "Incentives",
    ]

    def __init__(self, filename, name):
        self.data = pd.DataFrame()
        self.name = name
        self.filename = filename
        try:
            self.data = pd.read_excel(filename, dtype=str)

            # Some order lists tend to use the first row for infos.
            if (
                self.data.columns[0].find("Unnamed") >= 0
                or self.data.columns[1].find("Unnamed") >= 0
            ):
                self.data = pd.read_excel(filename, header=1, dtype=str)

        except Exception:
            # No problem here, caller receives an empty DataFrame
            pass
        self.empty = self.data.empty
        if filename == "DIAMOND":
            print(self.data)

    def cols(self):
        return self.data.columns.values.tolist()

    def print_order(self):
        match self.name:
            case "DIAMOND":
                return ["Qty", "Code", "Price", "Title", "Issue"]
            case _:
                return ["Qty", "MgCode", "Code", "Price", "Title", "Issue"]

    def reduce(self, colums):
        self.data = self.data.drop(drop_list, axis="columns")
        # self.data = self.data.dropna()

    def to_excel(self, filename):
        self.fix_price()
        (*path, filename) = os.path.split(filename)
        (filename, extension) = filename.split(".")
        filename = os.path.join(path, filename)
        self.data.to_excel(
            f"{self.filename}_.xlsx",
            columns=self.print_order(),
            index=False,
        )
        if self.name == "PRH":
            self.data.to_csv(
                f"./bin/{self.name}",
                sep=";",
                lineterminator="\r\n",
                header=False,
                index=False,
                decimal=",",
                columns=["Qty", "MgCode", "Code", "Price", "Title", "Issue"],
                mode="w",
            )
            self.data.to_csv(
                "./bin/mar_mg",
                sep=";",
                lineterminator="\r\n",
                header=False,
                index=False,
                decimal=",",
                columns=["Qty", "MgCode", "Code", "Price", "Title", "Issue"],
                mode="a",
            )
        if self.name == "DC":
            self.data.to_csv(
                f"./bin/{self.name}",
                sep=";",
                lineterminator="\r\n",
                header=False,
                index=False,
                decimal=",",
                columns=["Qty", "MgCode", "Code", "Price", "Title", "Issue"],
                mode="w",
            )

    def get(self):
        return self.data.get(["MainIdentifier"])

    def rename_and_drop(self, new_names, dist_name):
        self.data.rename(columns=new_names, inplace=True)
        all_cols = set(self.data.columns)
        drop_list = list(all_cols.difference(set(new_names.values())))
        self.data.drop(drop_list, axis="columns", inplace=True)
        match dist_name:
            case "DIAMOND":
                self.data.dropna(inplace=True)
                self.data.reset_index(drop=True, inplace=True)
                self.data = pd.concat(
                    [
                        self.data,
                        pd.DataFrame([""] * self.data.shape[0], columns=["Qty"]),
                    ],
                    axis=1,
                )
            case "DC":
                self.data.replace({"Issue": np.nan}, 1, inplace=True)
                self.data.dropna(inplace=True)
                self.data.reset_index(drop=True, inplace=True)

                self.data = pd.concat(
                    [
                        self.data,
                        pd.DataFrame([""] * self.data.shape[0], columns=["Qty"]),
                    ],
                    axis=1,
                )
            case "PRH":
                self.data["Title"] = self.data["Title"].mask(
                    self.data["Incentives"].notna()
                )
                self.data.loc[self.data["Incentives"].notna(), "Title"] = CROSSOUT
                self.data.replace({"Issue": np.nan}, 1, inplace=True)
                self.data.drop("Incentives", axis="columns", inplace=True)
                self.data.dropna(inplace=True)
                self.data.reset_index(drop=True, inplace=True)
                self.data = pd.concat(
                    [
                        self.data,
                        pd.DataFrame([""] * self.data.shape[0], columns=["Qty"]),
                    ],
                    axis=1,
                )

    def process_import(self):
        match self.name:
            case "DIAMOND":
                issues = list()
                for i, row in self.data.iterrows():
                    issues.append(parse_issue(row.at["Title"]))

                self.data = pd.concat(
                    [
                        self.data,
                        pd.DataFrame(issues, columns=["Issue"], dtype=str),
                    ],
                    axis=1,
                )

    def fix_price(self):
        df = self.data
        df["Price"] = (
            df["Price"]
            .astype(float)
            .round(2)
            .map("{:.2f}".format)
            .apply(lambda s: s.replace(".", ","))
        )


def parse_issue(s):
    issue = "1"
    index = s.find("#")
    if index > 0:
        issue = s[index:].split()[0][1:]
    index = s.find("VOL")
    if index > 0:
        issue = s[index:].split()[1]

    if not issue.isdigit():
        issue = "1"

    return issue
