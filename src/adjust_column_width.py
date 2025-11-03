import openpyxl

def adjust_column_width(fn : str):
    wb = openpyxl.load_workbook(fn)
    worksheet = wb.active
    for col in worksheet.columns:
         max_length = 0
         column = col[0].column_letter # Get the column name
         for cell in col:
             try: # Necessary to avoid error on empty cells
                 max_length = max(len(str(cell.value)), max_length)
             except:
                 pass
         adjusted_width = (max_length + 2) * 1.2
         worksheet.column_dimensions[column].width = adjusted_width

    wb.save(fn)
