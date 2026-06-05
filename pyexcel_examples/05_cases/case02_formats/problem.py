"""
ПРОБЛЕМА: Различия между форматами (XLSX, XLS, ODS, CSV)

Разные форматы имеют разные возможности:
- XLSX (moderna Excel): лучше всего поддерживается
- XLS (старый Excel): могут быть проблемы с кодировкой
- ODS (OpenDocument): может быть медленнее
- CSV: теряет форматирование, может быть проблемы с кодировкой
pyexcel должен иметь установлены нужные драйверы для каждого формата.
"""

import pyexcel as pe

print("=" * 60)
print("ПРОБЛЕМА: Различия между форматами")
print("=" * 60)

# ✓ Попытка открыть XLSX
print("\n1. Чтение XLSX:")
try:
    sheet_xlsx = pe.get_sheet(file_name='sample.xlsx')
    print(f"  ✓ XLSX работает: {len(sheet_xlsx)} строк, {len(sheet_xlsx.columns)} столбцов")
except Exception as e:
    print(f"  ❌ Ошибка: {e}")

# ✓ Попытка открыть ODS
print("\n2. Чтение ODS:")
try:
    sheet_ods = pe.get_sheet(file_name='sample.ods')
    print(f"  ✓ ODS работает: {len(sheet_ods)} строк, {len(sheet_ods.columns)} столбцов")
except Exception as e:
    print(f"  ❌ Ошибка ODS: {e}")
    print("     Нужно установить pyexcel-ods: pip install pyexcel-ods")

# ✓ Сравнение данных из разных форматов
print("\n3. Сравнение содержимого:")
try:
    sheet_xlsx = pe.get_sheet(file_name='sample.xlsx')
    sheet_ods = pe.get_sheet(file_name='sample.ods')

    xlsx_data = list(sheet_xlsx.rows())
    ods_data = list(sheet_ods.rows())

    print(f"  XLSX первая строка: {xlsx_data[0]}")
    print(f"  ODS первая строка:  {ods_data[0]}")
    print(f"  Данные одинаковы: {xlsx_data == ods_data}")
except Exception as e:
    print(f"  Ошибка при сравнении: {e}")

# ❌ Проблемы с конвертацией
print("\n4. Проблемы при конвертации форматов:")
print("  - При сохранении CSV теряется форматирование")
print("  - При сохранении ODS могут быть проблемы с совместимостью")
print("  - Разные драйверы дают разные результаты")
print("  - Кодировка может отличаться между форматами")

print("\n⚠️ ВЫВОД:")
print("  - XLSX наиболее универсален (рекомендуется)")
print("  - ODS требует доп. библиотеку и может быть медленнее")
print("  - CSV хорош только для простых текстовых данных")
print("  - Всегда проверяйте поддержку нужного формата!")

