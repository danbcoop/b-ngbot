import os

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
