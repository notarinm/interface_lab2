import re
import os
import winreg


figures = []
errors = []

FIGURES_FILE = "figures.txt"
ERROR_FILE = "errors.txt"

REGISTRY_PATH = r"Software\FiguresProgram"


def read_file():
    with open(FIGURES_FILE, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, 1):
            line = line.strip()

            if not line:
                continue

            if re.fullmatch(
                r"Point\(-?\d+(\.\d+)?,\s*-?\d+(\.\d+)?\)",
                line
            ):
                figures.append(line)

            elif re.fullmatch(
                r"Line\(Point\(-?\d+(\.\d+)?,\s*-?\d+(\.\d+)?\),\s*"
                r"Point\(-?\d+(\.\d+)?,\s*-?\d+(\.\d+)?\)",
                line
            ):
                figures.append(line)

            elif re.fullmatch(
                r"Circle\(Point\(-?\d+(\.\d+)?,\s*-?\d+(\.\d+)?\),\s*"
                r"-?\d+(\.\d+)?\)",
                line
            ):
                figures.append(line)

            else:
                errors.append(f"Строка {line_number}: {line}")


def print_figures():
    for figure in figures:
        print(figure)


def count_figures():
    print("Количество объектов:", len(figures))


def write_errors():
    with open(ERROR_FILE, "w", encoding="utf-8") as file:
        for error in errors:
            file.write(error + "\n")


def print_errors():
    for error in errors:
        print(error)


def enable_log():
    key = winreg.CreateKey(
        winreg.HKEY_CURRENT_USER,
        REGISTRY_PATH
    )

    winreg.SetValueEx(
        key,
        "LogEnabled",
        0,
        winreg.REG_DWORD,
        1
    )

    winreg.SetValueEx(
        key,
        "ErrorFile",
        0,
        winreg.REG_SZ,
        ERROR_FILE
    )

    winreg.CloseKey(key)


def log_enabled():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            REGISTRY_PATH
        )

        value, _ = winreg.QueryValueEx(
            key,
            "LogEnabled"
        )

        winreg.CloseKey(key)

        return value == 1

    except FileNotFoundError:
        return False


def main():

    try:
        read_file()

    except FileNotFoundError:
        print("Файл figures.txt не найден.")
        return

    operation = input(
        "Введите операцию (print, count, --log): "
    ).strip()

    if operation == "--log":

        enable_log()
        write_errors()

        print("Логирование включено.")
        print("Ошибки записаны в errors.txt")

        return

    if operation == "print":
        print_figures()

    elif operation == "count":
        count_figures()

    else:
        print("Неизвестная операция.")
        return

    if errors:
        if log_enabled():
            write_errors()

        else:
            print("\nОшибки:")
            print_errors()


if __name__ == "__main__":
    main()