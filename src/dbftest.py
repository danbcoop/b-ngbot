"""
from dbfpy3 import dbf



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
    """
