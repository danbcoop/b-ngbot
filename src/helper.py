import os

from dbfpy3 import dbf
from src.distributor import Dist


def ospath(path: str) -> str:
    if os.name == "posix":
        return path
    else:  # Windows
        return path.replace("/", "\\")


FILESDIR = ospath("./files")


def default_filename(dist: Dist) -> str:
    ls = os.listdir(FILESDIR)
    for filename in ls:
        if candidate_found(filename, [dist.name]):
            filename = os.path.join(FILESDIR, filename)
            dist.filename = filename
            return filename
    return "Bitte eine Bestellliste wählen."


def default_col_name(dist: Dist, col_name: str) -> str:
    for col in dist.orderlist.cols():
        if candidate_found(col, dist.col_names[col_name]):
            return col
    return "Spaltennamen wählen."


def candidate_found(find_in: str, find: list[str]) -> bool:
    for s in find:
        if find_in.find(s) >= 0:
            return True
    return False


def code_remove_year(s: str) -> str:
    # 1025DC0050 -> 105DC005
    return s[:2] + s[3:]


def lunar_to_poc(s: str) -> str:
    if len(s) > 9:
        s = code_remove_year(s)
    # 105DC005 -> DC105005
    return s[3:5] + s[:3] + s[5:]


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
            rec["POCODE"] = lunar_to_poc(row.at["Code"])
            rec["TITLE"] = row.at["Title"]
            rec["ISSUE"] = row.at["Issue"]
            rec["PRICE"] = float(row.at["Price"])
            rec["SUPPLIER"] = "PEP"
        case "PRH":
            rec["POCODE"] = row.at["MgCode"]
            rec["TITLE"] = row.at["Title"]
            rec["ISSUE"] = row.at["Issue"]
            rec["PRICE"] = float(row.at["Price"])
            rec["SUPPLIER"] = "MOD"

    db.write(rec)
