"""
ПРОБЛЕМА: Производительность при работе с большими файлами

pyexcel загружает весь файл в память сразу, что может быть проблемой
для больших файлов (1000+ строк). Для файлов с сотнями тысяч строк
это может привести к:
- Медленной загрузке
- Большому потреблению памяти
- Зависанию приложения
"""

import pyexcel as pe
import time
import pandas as pd

print("=" * 60)
print("ПРОБЛЕМА: Производительность на больших файлах")
print("=" * 60)

# ❌ Проблемный подход 1: pyexcel загружает всё в память
print("\n1. Чтение большого файла с pyexcel (медленно):")
start = time.time()
try:
    sheet = pe.get_sheet(file_name='sample_large.xlsx')
    elapsed = time.time() - start
    print(f"  Время загрузки: {elapsed:.2f} сек")
    print(f"  Количество строк: {len(sheet)}")
    print(f"  Память: весь файл в памяти")
except Exception as e:
    print(f"  ❌ Ошибка: {e}")

# ❌ Проблемный подход 2: Преобразование всех данных в списки
print("\n2. Конвертация всех данных в список (очень медленно):")
start = time.time()
try:
    sheet = pe.get_sheet(file_name='sample_large.xlsx')
    all_rows = list(sheet.rows())  # ❌ Преобразует всё в список в памяти
    elapsed = time.time() - start
    print(f"  Время обработки: {elapsed:.2f} сек")
    print(f"  Количество строк в памяти: {len(all_rows)}")
except Exception as e:
    print(f"  ❌ Ошибка: {e}")

# ⚠️ Проблема: обработка строка за строкой
print("\n3. Попытка обработать строку за строкой:")
start = time.time()
try:
    sheet = pe.get_sheet(file_name='sample_large.xlsx')
    count = 0
    total_salary = 0

    for row in sheet.rows():
        if len(row) > 4:
            try:
                total_salary += float(row[4])  # Суммируем зарплаты
                count += 1
            except:
                pass

    elapsed = time.time() - start
    print(f"  Время обработки: {elapsed:.2f} сек")
    print(f"  Обработано строк: {count}")
    print(f"  Сумма зарплат: {total_salary:,.0f}")
except Exception as e:
    print(f"  ❌ Ошибка: {e}")

print("\n⚠️ ПРОБЛЕМЫ с pyexcel на больших файлах:")
print("  - Медленная загрузка (весь файл в памяти)")
print("  - Высокое потребление памяти")
print("  - Нет встроенной потоковой обработки")
print("  - Сложно работать с файлами > 100k строк")

