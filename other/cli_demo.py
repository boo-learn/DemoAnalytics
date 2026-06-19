import click


@click.command()
@click.option(
    "--count",
    "-c",
    default=1,
    help="Количество повторений приветствия.",
    show_default=True,
)
@click.option(
    "--shout",
    "-s",
    is_flag=True,
    help="Громкий режим (капсом).",
)
@click.argument("name")
def greet(count: int, shout: bool, name: str) -> None:
    """Простая утилита, которая приветствует пользователя NAME."""
    message = f"Привет, {name}!"

    if shout:
        message = message.upper()

    for _ in range(count):
        click.echo(message)


if __name__ == "__main__":
    greet()