import pandas as pd



class OrderList:
    COLUMN_NAMES = [
            "Title",
            "Issure",
            "Price",
            "Code",
            ]
    def __init__(self, filename):
        self.data = pd.DataFrame()
        try:
            self.data = pd.read_excel(filename)
        except Exception:
            # No Problem here, caller receives an empty DataFrame
            pass
        self.empty = self.data.empty
        self.colums = []

    def cols(self):
        return self.data.columns

    def reduce(self, needed_cols):
        all_cols = set(self.data.columns)
        drop_list = list(all_cols.difference(set(needed_cols)))
        self.data.drop(drop_list, axis='columns')
        self.data.dropna()


