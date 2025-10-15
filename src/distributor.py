import pandas as pd


class Dist:
    def __init__(self, name, index, filename=""):
        self.name = name
        self.id = index
        self.filename = filename
        self.orderlist = OrderList("")

    def load(self):
        self.orderlist = OrderList(self.filename)

    def to_excel(self):
        self.orderlist.to_excel(self.filename)


class OrderList:
    COLUMN_NAMES = [
        "Title",
        "Issue",
        "Price",
        "Code",
    ]

    def __init__(self, filename):
        self.data = pd.DataFrame()
        try:
            self.data = pd.read_excel(filename, dtype=str)

            # Some order lists tend to use the first row for infos.
            if (
                self.data.columns[0].find("Unnamed") >= 0
                or self.data.columns[1].find("Unnamed") >= 0
            ):
                self.data = pd.read_excel(filename, header=1, dtype=str)

        except Exception:
            # No Problem here, caller receives an empty DataFrame
            pass
        self.empty = self.data.empty

    def cols(self):
        return self.data.columns

    def reduce(self, needed_cols):
        all_cols = set(self.data.columns)
        drop_list = list(all_cols.difference(set(needed_cols)))
        self.data = self.data.drop(drop_list, axis="columns")
        self.data = self.data.dropna()

    def to_excel(self, filename):
        self.data.to_csv(f"{filename}_changed.xlsx", index=False)

    def get(self):
        return self.data.get(["MainIdentifier"])
