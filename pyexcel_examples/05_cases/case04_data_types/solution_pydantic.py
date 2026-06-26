import csv
from datetime import datetime, date
from pydantic import BaseModel, Field, ValidationError, field_validator


class CleanRow(BaseModel):
    name: str = Field(alias="Name")
    age: int = Field(alias="Age")
    salary: float = Field(alias="Salary")

    # Изменили имя поля на payment_date, конфликт с типом date ушел!
    payment_date: date = Field(alias="Date")

    active: bool = Field(alias="Active")
    percentage: float = Field(alias="Percentage")

    @field_validator("name", mode="before")
    @classmethod
    def strip_string(cls, v: str) -> str:
        return v.strip() if isinstance(v, str) else v

    @field_validator("salary", mode="before")
    @classmethod
    def parse_salary(cls, v: str) -> str | float:
        """Удаляет пробелы-разделители тысяч перед парсингом во float"""
        if isinstance(v, str):
            return v.replace(" ", "").strip()
        return v

    # Привязали валидатор к новому имени поля payment_date
    @field_validator("payment_date", mode="before")
    @classmethod
    def parse_date(cls, v: str) -> date | str:
        """Перебирает известные маски дат"""
        if not isinstance(v, str):
            return v

        formats = [
            "%Y-%m-%d",  # 2020-01-15 (ISO)
            "%d.%m.%Y",  # 15.04.2018 (РФ/Европа)
            "%m/%d/%Y",  # 04/20/2017 (США)
        ]
        clean_data = v.strip()
        for fmt in formats:
            try:
                return datetime.strptime(clean_data, fmt).date()
            except ValueError:
                continue

        raise ValueError(f"date format '{clean_data}' is not supported.")


def process_dirty_csv(file_path: str) -> list[CleanRow]:
    cleaned_data: list[CleanRow] = []

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for idx, row in enumerate(reader, start=2):
            try:
                # Pydantic сам смапит колонку "Date" в поле "payment_date" благодаря alias
                clean_row = CleanRow.model_validate(row)
                cleaned_data.append(clean_row)

            except (ValidationError, KeyError) as e:
                print(f"Parse error at line {idx}: {e.errors(include_url=False)}. Line skipped.")
                continue

    return cleaned_data


if __name__ == "__main__":
    # Пример работы с фейковыми данными для проверки:
    dirty_rows = [
        {
            "Name": "  Иван  ",
            "Age": "30",
            "Salary": "150 000.50",
            "Date": "25.12.2025",
            "Active": "True",
            "Percentage": "14.5"
        },
        {
            "Name": "Анна",
            "Age": "25",
            "Salary": "80000",
            "Date": "2026-04-01",
            "Active": "false",
            "Percentage": "10.0"
        }
    ]

    print("--- Тест валидации строк ---")
    for row in dirty_rows:
        try:
            validated = CleanRow.model_validate(row)
            # Доступ к дате теперь через .payment_date
            print(
                f"Имя: {validated.name:<6} | ЗП: {validated.salary:<8} | Дата: {validated.payment_date} | Активен: {validated.active}")
        except ValidationError as e:
            print(f"Ошибка: {e.json()}")