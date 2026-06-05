"""Демонстрация: CSV часто читается как строки, даже когда значения похожи на числа/даты."""

import pyexcel as pe

print("ПРОБЛЕМА: данные в CSV часто воспринимаются как строки\n")

# читаем CSV с намеренно неоднородными форматами
sheet = pe.get_array(file_name='sample.csv')

headers = sheet[0]
print(f"Заголовки: {headers}\n")

# проходим по всем строкам данных и выводим тип каждого значения
print("Типы данных для каждого поля:\n")
for row_idx, row in enumerate(sheet[1:], start=1):
    print(f"Строка {row_idx}:")
    for name, value in zip(headers, row):
        py_type = type(value).__name__
        # если это строка и не Имя, показываем, что это проблема
        if isinstance(value, str) and name != "Name":
            mark = "⚠️ STR"
        else:
            mark = "✓ OK"
        print(f"  {name:11} {value!r:30} → {py_type:10} {mark}")
    print()
