"""
РЕШЕНИЕ: Правильная работа с пустыми ячейками и whitespace

Стратегия: проверяем значения перед использованием и очищаем пробелы.
"""

import pyexcel as pe
import pandas as pd
import numpy as np

print("=" * 60)
print("РЕШЕНИЕ: Работа с пустыми ячейками")
print("=" * 60)

# ✓ ВАРИАНТ 1: Очистка и валидация данных
print("\n✓ ВАРИАНТ 1: Очистка данных при чтении")
sheet = pe.get_sheet(file_name='sample.xlsx')

def clean_value(value):
    """Очищает значение от пробелов и преобразует пустоты в None"""
    if value is None:
        return None
    if isinstance(value, str):
        stripped = value.strip()
        return stripped if stripped else None
    return value

# Функция для проверки пустой строки
def is_empty_row(row):
    """Проверяет, является ли строка полностью пустой"""
    return all(clean_value(cell) is None for cell in row)

print("\nОчищенные данные:")
headers = sheet.row[0]
print(f"Заголовки: {headers}")

cleaned_data = []
for idx, row in enumerate(sheet.rows()):
    if idx == 0:
        continue

    # Очищаем каждое значение
    cleaned_row = [clean_value(cell) for cell in row]

    # Пропускаем полностью пустые строки
    if is_empty_row(cleaned_row):
        print(f"Строка {idx}: [ПРОПУЩЕНА - полностью пуста]")
        continue

    print(f"Строка {idx}: {cleaned_row}")
    cleaned_data.append(cleaned_row)

# ✓ ВАРИАНТ 2: Использование pandas для работы с пропусками
print("\n✓ ВАРИАНТ 2: Использование pandas.fillna()")
df = pd.read_excel('sample.xlsx')

print("\nОригинальный DataFrame:")
print(df)

print("\nОбработка None/NaN:")
print(f"Пропуски в каждом столбце:\n{df.isnull().sum()}")

# Удаляем полностью пустые строки
df_clean = df.dropna(how='all')
print(f"\nПосле удаления полностью пустых строк:")
print(df_clean)

# Заполняем пропуски нулями или предыдущим значением
df_filled = df.fillna(0)  # или .fillna(method='ffill')
print(f"\nПосле заполнения пробелов нулями:")
print(df_filled)

# ✓ ВАРИАНТ 3: Селективное удаление строк с пропусками
print("\n✓ ВАРИАНТ 3: Удаление строк с пропусками в критических столбцах")
critical_columns = ['Product', 'Q1']
df_valid = df.dropna(subset=critical_columns)
print(f"Строки с непустыми [{critical_columns}]:")
print(df_valid)

# ✓ ВАРИАНТ 4: Работа с whitespace
print("\n✓ ВАРИАНТ 4: Очистка от пробелов в строках")
df_stripped = df.copy()
for col in df_stripped.columns:
    df_stripped[col] = df_stripped[col].astype(str).str.strip()
print("После очистки пробелов:")
print(df_stripped)

print("\n✓ РЕКОМЕНДАЦИЯ: Всегда очищайте данные после чтения")
print("  1. Удаляйте полностью пустые строки: df.dropna(how='all')")
print("  2. Очищайте пробелы в строковых столбцах: df[col] = df[col].str.strip()")
print("  3. Заполняйте или удаляйте пропуски в нужных столбцах")
