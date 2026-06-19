from dataclasses import dataclass, field
import click


# Класс для хранения состояния нашего приложения
@dataclass
class TodoStore:
    tasks: list[str] = field(default_factory=lambda: ["Купить молоко", "Обновить Python"])


# pass_obj автоматически передает объект TodoStore в качестве первого аргумента всем подкомандам
pass_store = click.make_pass_decorator(TodoStore, ensure=True)


# Создаем главную группу команд
@click.group()
@click.version_option("1.0.0", prog_name="TodoCLI")
def cli() -> None:
    """Удобный To-Do менеджер прямо в вашем терминале."""
    pass


# Команда просмотра списка задач
@cli.command(name="list")
@pass_store
def list_tasks(store: TodoStore) -> None:
    """Показать все текущие задачи."""
    if not store.tasks:
        click.secho("📝 Ваш список задач пуст!", fg="yellow", bold=True)
        return

    click.secho("📋 Ваши задачи:", fg="cyan", bold=True, underline=True)
    for index, task in enumerate(store.tasks, start=1):
        # Используем click.style для комбинирования цветов в одной строке
        idx_str = click.style(f"{index}.", fg="black", bg="white", bold=True)
        task_str = click.style(task, fg="green")
        click.echo(f"{idx_str} {task_str}")


# Команда добавления задачи с валидацией
@cli.command(name="add")
@click.argument("task_text", type=str)
@click.option(
    "--priority",
    "-p",
    type=click.Choice(["low", "medium", "high"], case_sensitive=False),
    default="medium",
    help="Приоритет задачи.",
    show_default=True,
)
@pass_store
def add_task(store: TodoStore, task_text: str, priority: str) -> None:
    """Добавить новую задачу TASK_TEXT в список."""
    # Цветовое кодирование в зависимости от приоритета
    match priority.lower():
        case "high":
            prefix = click.style("[Срочно]", fg="red", bold=True)
        case "medium":
            prefix = click.style("[Нормально]", fg="yellow")
        case _:
            prefix = click.style("[Позже]", fg="blue", dim=True)

    full_task = f"{prefix} {task_text}"
    store.tasks.append(full_task)

    # Краткий вариант: click.secho заменяет click.echo(click.style(...))
    click.secho("✅ Задача успешно добавлена!", fg="green", bold=True)


# Команда удаления (требует подтверждения)
@cli.command(name="clear")
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="Удалить всё без подтверждения.",
)
@pass_store
def clear_tasks(store: TodoStore, force: bool) -> None:
    """Очистить весь список задач."""
    if not force:
        # Интерактивный вопрос прямо посреди выполнения
        confirm = click.confirm(
            click.style("⚠️ Вы уверены, что хотите удалить ВСЕ задачи?", fg="red", bold=True),
            default=False,
        )
        if not confirm:
            click.echo("Отменено.")
            return

    store.tasks.clear()
    click.secho("💥 Список задач полностью очищен!", fg="magenta", bg="black", blink=True)


if __name__ == "__main__":
    cli()
