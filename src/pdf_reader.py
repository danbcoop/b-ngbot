from pypdf import PdfReader


def read_pdf(filename: str, start_string: str) -> list():
    reader = PdfReader(filename)
    for page in reader.pages:
        buf = page.extract_text()
        found = False
        items = list()
        for line in buf.split("\n"):

            if start_string in line:
                found = True
            if not found:
                continue
            try:
                item = dict()
                item["Menge"] = line[: line.index(" ")]
                line = line[line.index(" ") + 1 :]
                if not item["Menge"].isdigit():
                    continue

                item["Code"] = line[: line.index(" ")]
                line = line[line.index(" ") + 1 :]

                item["Price"] = line[: line.index(" ")].replace(",", ".")

                item["Title"] = line[line.index(" ") + 1 :]
                if "-" in item["Price"]:
                    continue

                items.append(item)

            except Exception:
                continue

    return items
