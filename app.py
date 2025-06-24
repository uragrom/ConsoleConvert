import os
import cv2
import numpy as np
import pyperclip
from PIL import Image, ImageOps
from pynput import keyboard

# Конфигурация
ASCII_CHARS = "@%#*+=-:. "  # Градиент от темного к светлому
FRAME_SIZE = (80, 40)  # Ширина x Высота в символах
WEBCAM_MODE = False  # Режим реального времени с камеры


def image_to_ascii(image_path: str, copy_to_clipboard: bool = False) -> str:
    """Конвертирует изображение в ASCII с возможностью копирования"""
    image = Image.open(image_path)
    image = prepare_image(image)
    ascii_art = pixels_to_ascii(image)

    if copy_to_clipboard:
        pyperclip.copy(ascii_art)
        print("✓ ASCII art скопирован в буфер!")
    return ascii_art


def video_to_ascii(video_path: str, output_file: str = None):
    """Конвертирует видео в ASCII анимацию"""
    cap = cv2.VideoCapture(video_path if not WEBCAM_MODE else 0)

    if output_file:
        f = open(output_file, 'w')

    try:
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

            # Управление клавишами
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        if output_file:
            f.close()


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


def interactive_menu():
    """Интерактивное меню"""
    print("═" * FRAME_SIZE[0])
    print("ASCII VISION".center(FRAME_SIZE[0]))
    print("═" * FRAME_SIZE[0])
    print("1. Конвертировать фото\n2. Конвертировать видео\n3. Вебкам-режим\n4. Выход")

    choice = input("> ")
    if choice == "1":
        path = input("Путь к изображению: ")
        result = image_to_ascii(path, True)
        print("\n" + result)
    elif choice == "2":
        path = input("Путь к видео: ")
        video_to_ascii(path, "output_animation.txt")
    elif choice == "3":
        global WEBCAM_MODE
        WEBCAM_MODE = True
        video_to_ascii(None)
    elif choice == "4":
        exit()


if __name__ == "__main__":
    interactive_menu()