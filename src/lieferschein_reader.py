import pandas as pd


def load_lieferschein(filename: str, start_string: str) -> list():
    data = pd.read_excel(filename, header=None)
    col_names = {0: "Menge", 1: "Code", 2: "Price", 3: "Title"}
    data.rename(columns=col_names, inplace=True)
    lieferschein = data.to_dict()
    index_range = []
    for i in lieferschein["Title"]:
        if lieferschein["Title"][i] == start_string:
            index_range = range(i + 1, len(lieferschein["Title"]))
            break

    items = list()
    for i in index_range:
        item = dict()
        item["Menge"] = lieferschein["Menge"][i]
        item["Code"] = lieferschein["Code"][i]
        item["Price"] = lieferschein["Price"][i]
        item["Title"] = lieferschein["Title"][i]
        if item["Price"] < 0:
            continue
        items.append(item)

    return items


if __name__ == "__main__":
    print(read_pdf("files/BÄNGBÄNG-LIEFERSCHEIN.pdf", "NEUHEITEN"))
