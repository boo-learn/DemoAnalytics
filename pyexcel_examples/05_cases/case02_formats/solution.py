"""
РЕШЕНИЕ: Правильная работа с разными форматами

Стратегия:
1. Используйте XLSX как основной формат
2. Убедитесь, что установлены нужные драйверы
3. При конвертации проверяйте результат
4. Используйте pandas для кроссплатформенности
"""

import pyexcel as pe
import pandas as pd
import os

print("=" * 60)
print("РЕШЕНИЕ: Работа с разными форматами")
print("=" * 60)

# ✓ ВАРИАНТ 1: Проверка установленных драйверов
print("\n✓ ВАРИАНТ 1: Проверка поддерживаемых форматов")
print("\nУстановленные плагины pyexcel:")
try:
    # Проверяем что работает
    formats = {
        'xlsx': 'XLSX (Excel 2007+)',
        'xls': 'XLS (Excel 97-2003)',
        'ods': 'ODS (OpenDocument)',
        'csv': 'CSV (Comma-separated)',
    }

    for fmt, name in formats.items():
        try:
            # Проверяем читаем ли мы файл нужного формата
            if os.path.exists(f'sample.{fmt}'):
                sheet = pe.get_sheet(file_name=f'sample.{fmt}')
                print(f"  ✓ {name}: поддерживается")
            else:
                print(f"  - {name}: файл не найден")
        except Exception as e:
            print(f"  ⚠️ {name}: {str(e)[:50]}")
except Exception as e:
    print(f"  Ошибка: {e}")

# ✓ ВАРИАНТ 2: Конвертация между форматами
print("\n✓ ВАРИАНТ 2: Конвертация между форматами")

# Читаем из XLSX
sheet = pe.get_sheet(file_name='sample.xlsx')
print(f"  Прочитано из sample.xlsx: {len(sheet)} строк")

# Сохраняем в ODS
try:
    sheet.save_as('sample_converted.ods')
    print("  ✓ Сохранено в sample_converted.ods")
except Exception as e:
    print(f"  ⚠️ Ошибка при сохранении ODS: {e}")

# Сохраняем в CSV
sheet.save_as('sample_converted.csv')
print("  ✓ Сохранено в sample_converted.csv")

# ✓ ВАРИАНТ 3: Использование pandas для универсальности
print("\n✓ ВАРИАНТ 3: Использование pandas (рекомендуется)")

# Pandas автоматически определяет формат по расширению
formats_to_read = ['sample.xlsx']
if os.path.exists('sample.ods'):
    formats_to_read.append('sample.ods')

for file in formats_to_read:
    try:
        if file.endswith('.ods'):
            df = pd.read_excel(file, engine='odf')
        else:
            df = pd.read_excel(file)
        print(f"  ✓ Pandas прочитал {file}: {len(df)} строк, {len(df.columns)} столбцов")
    except Exception as e:
        print(f"  ⚠️ Ошибка при чтении {file}: {e}")

# ✓ ВАРИАНТ 4: Безопасное чтение с проверками
print("\n✓ ВАРИАНТ 4: Безопасное чтение с обработкой ошибок")

def safe_read_sheet(filename):
    """Безопасно читает файл в зависимости от формата"""
    try:
        if filename.endswith('.csv'):
            return pd.read_csv(filename), 'CSV (pandas)'
        elif filename.endswith('.ods'):
            return pd.read_excel(filename, engine='odf'), 'ODS'
        else:  # XLSX, XLS
            return pd.read_excel(filename), 'Excel'
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None, None

df, format_name = safe_read_sheet('sample.xlsx')
if df is not None:
    print(f"  ✓ Успешно прочитано как {format_name}")
    print(f"    Данные: {df.shape}")

# ✓ ВАРИАНТ 5: Единообразное сохранение
print("\n✓ ВАРИАНТ 5: Сохранение в нужный формат")

def save_sheet(df, filename, format_type='xlsx'):
    """Сохраняет DataFrame в нужный формат"""
    try:
        if format_type == 'csv':
            df.to_csv(filename, index=False)
        elif format_type == 'ods':
            df.to_excel(filename, engine='odf', index=False)
        else:  # xlsx по умолчанию
            df.to_excel(filename, index=False)
        print(f"  ✓ Сохранено в {filename} ({format_type})")
        return True
    except Exception as e:
        print(f"  ❌ Ошибка при сохранении: {e}")
        return False

# Сохраняем в разные форматы
if df is not None:
    save_sheet(df, 'output.xlsx', 'xlsx')
    save_sheet(df, 'output.csv', 'csv')
    # save_sheet(df, 'output.ods', 'ods')  # Требует odfpy

print("\n✓ РЕКОМЕНДАЦИИ:")
print("  1. Для основной работы используйте XLSX")
print("  2. Для совместимости с LibreOffice используйте ODS")
print("  3. Для обмена данными используйте CSV")
print("  4. Используйте pandas для универсальности")
print("  5. Всегда проверяйте результат после конвертации")

