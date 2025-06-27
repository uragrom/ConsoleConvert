import os
import cv2
import numpy as np
import pyperclip
from PIL import Image, ImageOps
import sys
import time

# Конфигурация
ASCII_CHARS = "@%#*+=-:. "  # Градиент от темного к светлому (можно добавить свои символы и они отобразатся в арте)
FRAME_SIZE = (80, 40)  # Ширина x Высота в символах
WEBCAM_MODE = False  # Режим реального времени с камеры

# Универсальный шрифт Block с поддержкой всех символов
ASCII_FONT = {
    'A': [' ▄▄▄ ', '▀▀▀█', '█  █', '█▀▀█', '█  █'],
    'B': ['▄▄▄ ', '█  █', '▄▄▄▀', '█  █', '▀▀▀▀'],
    'C': [' ▄▄▄', '▀  █', '█   ', '█   ', '▀▀▀▀'],
    'D': ['▄▄▄ ', '█  █', '█  █', '█  █', '▀▀▀ '],
    'E': ['▄▄▄▄', '█   ', '▄▄▄▀', '█   ', '▀▀▀▀'],
    'F': ['▄▄▄▄', '█   ', '▄▄▄▀', '█   ', '█   '],
    'G': [' ▄▄▄▄ ', '█     ', '█  ▄▄▄', '█    █', ' ▀▀▀▀ '],
    'H': ['█  █', '█  █', '▀▀▀█', '█  █', '█  █'],
    'I': ['▄▄▄', ' █ ', ' █ ', ' █ ', '▀▀▀'],
    'J': ['   █', '   █', '   █', '█  █', '▀▀▀ '],
    'K': ['█  █', '█ █ ', '▀▀  ', '█ █ ', '█  █'],
    'L': ['█   ', '█   ', '█   ', '█   ', '▀▀▀▀'],
    'M': ['█▄▄█', '█▀▀█', '█  █', '█  █', '█  █'],
    'N': ['█▄  █', '█▀█ █', '█ ▀██', '█  ▀█', '█   █'],
    'O': [' ▄▄▄▄ ', '█    █', '█    █', '█    █', ' ▀▀▀▀ '],
    'P': ['▄▄▄ ', '█  █', '▀▀▀ ', '█   ', '█   '],
    'Q': [' ▄▄▄ ', '█  █', '█  █', '█  █ ', '▀▀▀▀█'],
    'R': ['▄▄▄ ', '█  █', '▀▀▀ ', '█ █ ', '█  █'],
    'S': [' ▄▄▄▄ ', '█    ', ' ▄▄▄▄ ', '    █', ' ▀▀▀▀ '],
    'T': ['▄▄▄▄▄', '  █  ', '  █  ', '  █  ', '  █  '],
    'U': ['█   █', '█   █', '█   █', '█   █', '▀▀▀▀'],
    'V': ['█   █', '█   █', ' █ █ ', ' █ █ ', '  █  '],
    'W': ['█   █', '█   █', '█ █ █', '█▀ ▀█', ' █ █ '],
    'X': ['█   █', ' █ █ ', '  █  ', ' █ █ ', '█   █'],
    'Y': ['█   █', ' █ █ ', '  █  ', '  █  ', '  █  '],
    'Z': ['▄▄▄▄', '   █', '  █ ', ' █  ', '▀▀▀▀'],
    '0': [' ▄▄▄ ', '█  ▀█', '█ ▄ █', '▀█  █', ' ▀▀▀ '],
    '1': ['  █  ', '▀█  ', ' █  ', ' █  ', '▀▀▀▀'],
    '2': [' ▄▄▄ ', '█   █', '  ▄▀ ', ' █   ', '▀▀▀▀'],
    '3': ['▄▄▄▄', '    █', '  ▀▀ ', '    █', '▀▀▀▀'],
    '4': ['   █▄', '  █ █', ' █  █', '▀▀▀▀█', '    █'],
    '5': ['▄▄▄▄▄', '█    ', '▀▀▀▄', '    █', '▀▀▀▀'],
    '6': [' ▄▄▄▄', '█    ', '▀▀▀▄', '█   █', ' ▀▀▀ '],
    '7': ['▄▄▄▄▄', '    █', '   █ ', '  █  ', ' █   '],
    '8': [' ▄▄▄ ', '█   █', ' ▀▀▀ ', '█   █', ' ▀▀▀ '],
    '9': [' ▄▄▄ ', '█   █', ' ▀▀▀█', '    █', ' ▀▀▀ '],
    ' ': ['     ', '     ', '     ', '     ', '     '],
    '!': [' █ ', ' █ ', ' █ ', '   ', ' █ '],
    '"': ['▄ ▄ ', ' █ █ ', '     ', '     ', '     '],
    '#': ['  █ █  ', ' █▀▀▀█ ', ' █ █ █ ', '▀█ █▀ ', '  █ █  '],
    '$': ['  █  ', ' █▀▀▄', ' ▀▀▀ ', '▄▀▀█ ', '  █  '],
    '%': ['█   █', '   █ ', '  █  ', ' █   ', '█   █'],
    '&': [' ▄▄  ', '█  █ ', ' ▄▄▀ ', '█  █▄', ' ▀▀▀█'],
    "'": ['▄▄ ', ' ▀▀', '   ', '   ', '   '],
    '(': ['  █', ' █ ', ' █ ', ' █ ', '  █'],
    ')': ['█  ', ' █ ', ' █ ', ' █ ', '█  '],
    '*': ['    ', '█ ██', ' ██ ', '█ ██', '    '],
    '+': ['     ', '  █  ', ' █▀█▄', '  █  ', '     '],
    ',': ['   ', '   ', '   ', ' █ ', '▀  '],
    '-': ['     ', '     ', ' ████', '     ', '     '],
    '.': ['   ', '   ', '   ', '   ', ' █ '],
    '/': ['    █', '   █ ', '  █  ', ' █   ', '█    '],
    ':': ['   ', ' █ ', '   ', ' █ ', '   '],
    ';': ['   ', ' █ ', '   ', ' █ ', '▀  '],
    '<': ['   █', '  █ ', ' █  ', '  █ ', '   █'],
    '=': ['     ', '▄▄▄▄▄', '     ', '▄▄▄▄▄', '     '],
    '>': ['█   ', ' █  ', '  █ ', ' █  ', '█   '],
    '?': [' ▄▄▄ ', '█   █', '  ▀▀ ', '     ', '  █  '],
    '@': [' ▄▄▄▄ ', '█ ▄ ▀█', '█ ▀ █', '█ ▄▄▀', ' ▀▀▀  '],
    '[': ['▄▄▄', '█  ', '█  ', '█  ', '▀▀▀'],
    '\\': ['█    ', ' █   ', '  █  ', '   █ ', '    █'],
    ']': ['▄▄▄', '  █', '  █', '  █', '▀▀▀'],
    '^': [' █  ', '█ █ ', '     ', '     ', '     '],
    '_': ['     ', '     ', '     ', '     ', '▄▄▄▄▄'],
    '`': ['▄▄ ', ' ▀█ ', '   ', '   ', '   '],
    '{': ['  █', ' █ ', '▄█ ', ' █ ', '  █'],
    '|': ['█', '█', '█', '█', '█'],
    '}': ['█  ', ' █ ', ' ▀█', ' █ ', '█  '],
    '~': ['     ', ' ▀█▄ ', '     ', '     ', '     ']
}


def text_to_ascii(text: str, copy: bool = False) -> str:
    """Преобразует текст в ASCII-арт с отступами"""
    text = text.upper()
    ascii_art = ""

    # Создаем по строкам
    for row in range(5):  # Каждый символ высотой 5 строк
        line = ""
        for char in text:
            # Получаем символ или заменяем на пробел если отсутствует
            char_data = ASCII_FONT.get(char, ASCII_FONT.get(' ', ['     '] * 5))
            # Добавляем символ + отступ
            line += char_data[row] + " "
        ascii_art += line.rstrip() + "\n"

    if copy:
        pyperclip.copy(ascii_art)
        print("✓ ASCII-текст скопирован в буфер!")

    return ascii_art


def image_to_ascii(image_path: str, copy_to_clipboard: bool = False) -> str:
    """Конвертирует изображение в ASCII с возможностью копирования"""
    try:
        image = Image.open(image_path)
        image = prepare_image(image)
        ascii_art = pixels_to_ascii(image)

        if copy_to_clipboard:
            pyperclip.copy(ascii_art)
            print("✓ ASCII art скопирован в буфер!")
        return ascii_art
    except Exception as e:
        print(f"Ошибка: {e}")
        return ""


def video_to_ascii(video_path: str, output_file: str = None):
    """Конвертирует видео в ASCII анимацию"""
    global WEBCAM_MODE

    try:
        if WEBCAM_MODE:
            cap = cv2.VideoCapture(0)
            print("\nВебкамера запущена. Нажмите 'q' для выхода...")
        else:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                print(f"Ошибка: Не удалось открыть видео {video_path}")
                return

        if output_file:
            f = open(output_file, 'w')

        try:
            frame_count = 0
            start_time = time.time()

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                frame = preprocess_frame(frame)
                ascii_frame = frame_to_ascii(frame)

                os.system('cls' if os.name == 'nt' else 'clear')
                print(ascii_frame)

                if output_file:
                    f.write(ascii_frame + "\n\n")

                frame_count += 1
                elapsed_time = time.time() - start_time
                fps = frame_count / elapsed_time if elapsed_time > 0 else 0

                print(f"FPS: {fps:.1f} | Кадров: {frame_count} | Нажмите 'q' для выхода")

                # Управление клавишами
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            cap.release()
            if output_file:
                f.close()
                print(f"\nАнимация сохранена в {output_file}")
            WEBCAM_MODE = False
    except Exception as e:
        print(f"Ошибка при обработке видео: {e}")


def prepare_image(image: Image) -> Image:
    """Подготовка изображения к конвертации"""
    image = ImageOps.exif_transpose(image)  # Исправление ориентации
    image = image.convert("L")  # В grayscale
    target_width = FRAME_SIZE[0]
    target_height = int(FRAME_SIZE[1] * 0.55)  # Учет пропорций символов
    return image.resize((target_width, target_height))


def preprocess_frame(frame: np.ndarray) -> np.ndarray:
    """Обработка кадра видео"""
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    height, width = frame.shape
    new_height = int(FRAME_SIZE[1] * height / width)
    return cv2.resize(frame, (FRAME_SIZE[0], new_height))


def pixels_to_ascii(image: Image) -> str:
    """Преобразование пикселей в ASCII символы"""
    pixels = np.array(image)
    ascii_str = ""
    for row in pixels:
        for pixel in row:
            index = int(pixel / 255 * (len(ASCII_CHARS) - 1))
            ascii_str += ASCII_CHARS[index]
        ascii_str += "\n"
    return ascii_str


def frame_to_ascii(frame: np.ndarray) -> str:
    """Конвертация кадра в ASCII"""
    return pixels_to_ascii(Image.fromarray(frame))


def text_conversion_menu():
    """Меню конвертации текста"""
    print("\n" + "=" * 50)
    print(" ТЕКСТ -> ASCII ART ".center(50))
    print("=" * 50)

    text = input("Введите текст: ").strip()
    if not text:
        print("Текст не может быть пустым!")
        return

    copy_choice = input("Копировать в буфер? (y/n): ").lower().strip()

    result = text_to_ascii(text, copy_choice == 'y')

    print("\nРезультат:\n")
    print(result)


def image_conversion_menu():
    """Меню конвертации изображений"""
    print("\n" + "=" * 50)
    print(" ИЗОБРАЖЕНИЕ -> ASCII ART ".center(50))
    print("=" * 50)

    path = input("Путь к изображению: ").strip()
    if not os.path.exists(path):
        print("Файл не найден!")
        return

    copy_choice = input("Копировать в буфер? (y/n): ").lower().strip()

    print("\nКонвертация...\n")
    result = image_to_ascii(path, copy_choice == 'y')
    print(result)


def video_conversion_menu():
    """Меню конвертации видео"""
    print("\n" + "=" * 50)
    print(" ВИДЕО -> ASCII АНИМАЦИЯ ".center(50))
    print("=" * 50)

    print("1. Из файла")
    print("2. С вебкамеры")
    choice = input("Выберите источник: ").strip()

    output_file = None
    save_choice = input("Сохранить в файл? (y/n): ").lower().strip()
    if save_choice == 'y':
        output_file = input("Имя выходного файла (например, animation.txt): ").strip()

    if choice == "1":
        path = input("Путь к видеофайлу: ").strip()
        if not os.path.exists(path):
            print("Файл не найден!")
            return
        video_to_ascii(path, output_file)
    elif choice == "2":
        global WEBCAM_MODE
        WEBCAM_MODE = True
        video_to_ascii(None, output_file)


def show_settings_menu():
    """Меню настроек"""
    global ASCII_CHARS, FRAME_SIZE

    while True:
        print("\n" + "═" * 50)
        print(" НАСТРОЙКИ ".center(50))
        print("═" * 50)
        print(f"1. Текущие символы: {ASCII_CHARS}")
        print(f"2. Размер вывода: {FRAME_SIZE[0]}x{FRAME_SIZE[1]}")
        print("3. Сбросить настройки")
        print("4. Вернуться в главное меню")

        choice = input("\nВыберите действие: ").strip()

        if choice == "1":
            new_chars = input("Введите новые символы (от темного к светлому): ").strip()
            if new_chars:
                ASCII_CHARS = new_chars
                print("Символы обновлены!")
            else:
                print("Нельзя использовать пустую строку!")
        elif choice == "2":
            try:
                width = int(input("Ширина (символов): ").strip())
                height = int(input("Высота (символов): ").strip())
                if width > 10 and height > 10:
                    FRAME_SIZE = (width, height)
                    print("Размер обновлен!")
                else:
                    print("Минимальный размер 10x10!")
            except ValueError:
                print("Некорректные значения!")
        elif choice == "3":
            ASCII_CHARS = "@%#*+=-:. "
            FRAME_SIZE = (80, 40)
            print("Настройки сброшены!")
        elif choice == "4":
            return
        else:
            print("Неверный выбор!")


def interactive_menu():
    """Интерактивное меню"""
    while True:
        print("\n" + "═" * 50)
        print(" ASCII VISION ".center(50))
        print("═" * 50)
        print("1. Конвертировать фото в ASCII")
        print("2. Конвертировать видео/вебкамеру в ASCII")
        print("3. Преобразовать текст в ASCII-арт")
        print("4. Настройки")
        print("5. Выход")

        try:
            choice = input("\nВыберите действие: ").strip()

            if choice == "1":
                image_conversion_menu()
            elif choice == "2":
                video_conversion_menu()
            elif choice == "3":
                text_conversion_menu()
            elif choice == "4":
                show_settings_menu()
            elif choice == "5":
                print("До свидания!")
                sys.exit(0)
            else:
                print("Неверный выбор!")
        except KeyboardInterrupt:
            print("\nВыход...")
            sys.exit(0)
        except Exception as e:
            print(f"Произошла ошибка: {e}")


def show_banner():
    """Показывает ASCII-баннер при запуске"""
    banner = r"""
▄▄▄▄▄ ▄▄▄▄ ▄▄▄  █▄▄█ ▄▄▄ █▄  █  ▄▄▄  █
  █   █    █  █ █▀▀█  █  █▀█ █ ▀▀▀█ █
  █   ▄▄▄▀ ▀▀▀  █  █  █  █ ▀██ █  █ █
  █   █    █ █  █  █  █  █  ▀█ █▀▀█ █
  █   ▀▀▀▀ █  █ █  █ ▀▀▀ █   █ █  █ ▀▀▀▀
    """
    print(banner)
    print(" Конвертер изображений, видео и текста в ASCII ".center(50))
    print("=" * 50)


if __name__ == "__main__":
    show_banner()
    interactive_menu()
