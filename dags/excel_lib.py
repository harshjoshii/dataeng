import xlrd3 as xlrd
import csv

def csv_from_excel(xlsx_file, sheet_index, csv_file):
    wb = xlrd.open_workbook(xlsx_file)
    sh = wb.sheet_by_index(sheet_index)
    your_csv_file = open(csv_file, 'w')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()