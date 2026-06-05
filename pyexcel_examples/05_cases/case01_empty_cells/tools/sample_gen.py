"""Создаёт файл с пустыми ячейками и пробелами для case02"""
import pyexcel as pe

# Создаём файл с пропусками и пробелами
data = [
    ['Product', 'Q1', 'Q2', 'Q3', 'Q4'],
    ['Widget', 100, None, 150, 120],  # Пустая Q2
    ['Gadget', 200, 180, None, 210],  # Пустая Q3
    ['', 300, 290, 280, '  '],  # Пустое имя продукта и пробелы в Q4
    ['Doohickey', None, None, None, None],  # Все пустые
    ['Tool', 400, 420, '  ', 450],  # Пробелы вместо данных
]

sheet = pe.Sheet(data)
sheet.save_as('sample.xlsx')
print("✓ Файл sample.xlsx с пустыми ячейками создан")

