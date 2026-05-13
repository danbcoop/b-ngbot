import pandas as pd
# from dbf import dbf
from dbfread import DBF


def poc_to_lunar(s: str) -> str:
    # DC1050005 -> DC0005
    return s[:2] + s[-4:]


def read_dbf(fn: str, ispep: bool):
    order_list = pd.read_excel("files/DC-ORDERDATEI 1025.xlsx", dtype=str)
    order_list = order_list.to_dict()
    table = DBF(fn)

    try:
        for record in table:
            if ispep:
                code = poc_to_lunar(str(record["POCODE"]))
            else:
                code = poc_to_prh(str(record["POCODE"]))
            qty = str(record["GESAMTBEST"])
            order_list_index = 0
            for index in order_list["Code"]:
                if pd.isna(order_list["Code"][index]):
                    continue
                if code in order_list["Code"][index]:
                    order_list_index = index
            order_list["Qty"][order_list_index] = qty
    except Exception:
        # No problem here, the dbf files were working with use faulty flags
        pass
    order_list = pd.DataFrame.from_dict(order_list)
    order_list.to_excel("test.xlsx", index=False)
    # adjust_column_width("text.xlsx")


def write_to_dbf(order: OrderList, mode="a"):
    match mode:
        case "a":
            with dbf.Dbf("ami.dbf") as db:
                for row in order.data.iterrow():
                    add_record(db, row, order.name)
        case "w":
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
                for row in order.data.iterrow():
                    add_record(db, row, order.name)


def add_record(db, row, order):
    rec = db.new()
    match order:
        case "DIAMOND":
            rec["POCODE"] = row["Code"]
            rec["TITLE"] = row["Title"]
            rec["ISSUE"] = row["Issue"]
            rec["PRICE"] = row["Price"]
            rec["SUPPLIER"] = "DIA"
        case "DC":
            rec["POCODE"] = row["MgCode"]
            rec["TITLE"] = row["Title"]
            rec["ISSUE"] = row["Issue"]
            rec["PRICE"] = row["Price"]
            rec["SUPPLIER"] = "PEP"
        case "PRH":
            rec["POCODE"] = row["MgCode"]
            rec["TITLE"] = row["Title"]
            rec["ISSUE"] = row["Issue"]
            rec["PRICE"] = row["Price"]
            rec["SUPPLIER"] = "MOD"

    db.write(rec)


if __name__ == "__main__":
    read_dbf("PEP.DBF")
