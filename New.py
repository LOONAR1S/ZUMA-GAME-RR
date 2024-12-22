def main():
    # Установка зеленого и белого цвета текста
    GREEN = '\033[92m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

    # Вывод в консоль
    print(f"{GREEN}user@raspberrypi:~ $ vcgencmd measure_temp")
    print(f"{WHITE}temp=48.1'C")
    print(f"{GREEN}user@raspberrypi:~ $ {RESET}")

    # Добавляем отступы
    print("\n\n\n\n\n")

    # Ожидание нажатия клавиши для завершения
    input("Нажмите Enter, чтобы закрыть это окно...")

if __name__ == "__main__":
    main()
