"""
ПРОБЛЕМА: Работа с пустыми ячейками и пробелами

pyexcel не различает пустые ячейки и ячейки с пробелами.
Нет встроенной фильтрации пустых строк.
Может быть сложно определить действительно ли ячейка пуста или
содержит только whitespace.
"""

import pyexcel as pe

print("=" * 60)
print("ПРОБЛЕМА: Пустые ячейки и пробелы")
print("=" * 60)

# Читаем файл
sheet = pe.get_sheet(file_name='sample.xlsx')

print("\n1. Исходные данные 'как есть':")
for idx, row in enumerate(sheet.rows()):
    print(f"Строка {idx}: {row}")

print("\n2. Проблемы при обработке:")
print("\nПопытка вычислить среднее для столбца Q2:")
q2_values = [row[1] for row in list(sheet.rows())[1:]]
print(f"Значения Q2: {q2_values}")
print(f"Типы: {[type(v) for v in q2_values]}")

try:
    # Это вызовет ошибку из-за None
    average = sum([v for v in q2_values if v is not None]) / len([v for v in q2_values if v is not None])
    print(f"Среднее: {average}")
except Exception as e:
    print(f"❌ Ошибка: {e}")

print("\n3. Проблема с пробелами:")
product_names = [row[0] for row in list(sheet.rows())[1:]]
print(f"Названия продуктов: {product_names}")
print(f"Длины строк: {[len(str(name)) if name else 0 for name in product_names]}")

print("\n⚠️ ПРОБЛЕМЫ:")
print("  - Пустые ячейки возвращаются как None")
print("  - Пробелы '  ' воспринимаются как данные")
print("  - Пустые строки остаются в данных")
print("  - Нельзя автоматически фильтровать пустые ячейки")

