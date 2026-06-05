"""
Создаёт файлы в разных форматах (XLSX и ODS) для case04
"""
import pyexcel as pe

# Создаём одни и те же данные
data = [
    ['Region', 'Sales Q1', 'Sales Q2', 'Sales Q3', 'Sales Q4'],
    ['North', 100000, 120000, 115000, 130000],
    ['South', 80000, 85000, 90000, 95000],
    ['East', 110000, 105000, 120000, 125000],
    ['West', 95000, 100000, 105000, 110000],
]

# Создаём XLSX
sheet = pe.Sheet(data)
sheet.save_as('sample.xlsx')
print("✓ Файл sample.xlsx создан")

# Создаём ODS
sheet = pe.Sheet(data)
sheet.save_as('sample.ods')
print("✓ Файл sample.ods создан")

