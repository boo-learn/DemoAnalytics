"""
Создаёт большой файл для case05 (производительность)
"""
import pyexcel as pe

# Создаём большой файл с 10000 строк
print("Создание большого файла (это может занять время)...")
data = [['ID', 'Name', 'Email', 'Department', 'Salary']]

# Генерируем 10000 строк данных
for i in range(1, 10001):
    data.append([
        i,
        f'Employee_{i}',
        f'emp{i}@company.com',
        f'Dept_{i % 5}',
        50000 + (i * 100),
    ])

sheet = pe.Sheet(data)
sheet.save_as('sample_large.xlsx')
print(f"✓ Файл sample_large.xlsx создан ({len(data)} строк)")

