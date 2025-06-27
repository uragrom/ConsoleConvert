import os
import re
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2
from tqdm import tqdm
import argparse


def create_frame(ascii_frame, font, char_width, char_height, text_color, bg_color):
    """Создает изображение из ASCII кадра"""
    lines = ascii_frame.strip().split('\n')
    height = len(lines)
    width = max(len(line) for line in lines) if lines else 0

    # Создаем изображение с белым фоном
    img = Image.new('RGB', (width * char_width, height * char_height), bg_color)
    draw = ImageDraw.Draw(img)

    # Рисуем текст
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            draw.text((x * char_width, y * char_height), char, fill=text_color, font=font)

    return img


def ascii_to_video(input_file, output_file, fps=10, font_size=10,
                   text_color=(255, 255, 255), bg_color=(0, 0, 0)):
    """Конвертирует ASCII анимацию в видео MP4"""

    # Загрузка файла
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Разделение на кадры (разделитель - три пустые строки)
    frames = [frame.strip() for frame in re.split(r'\n{3,}', content) if frame.strip()]

    if not frames:
        print("Ошибка: В файле не найдены кадры для воспроизведения")
        return

    # Загрузка моноширинного шрифта
    try:
        font = ImageFont.truetype("cour.ttf", font_size)  # Courier New для Windows
    except:
        try:
            font = ImageFont.truetype("DejaVuSansMono.ttf", font_size)  # Для Linux/Mac
        except:
            print("Предупреждение: Не найден моноширинный шрифт, используется системный по умолчанию")
            font = ImageFont.load_default()

    # Определяем размер символа (совместимость с новыми версиями Pillow)
    try:
        # Для старых версий Pillow
        char_width, char_height = font.getsize("X")
    except AttributeError:
        # Для новых версий Pillow (>=9.0.0)
        left, top, right, bottom = font.getbbox("X")
        char_width = right - left
        char_height = bottom - top

    # Создаем первый кадр для определения размера видео
    first_frame = create_frame(frames[0], font, char_width, char_height, text_color, bg_color)
    width, height = first_frame.size

    # Создаем видеопоток
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    # Обрабатываем все кадры
    for ascii_frame in tqdm(frames, desc="Создание видео"):
        img = create_frame(ascii_frame, font, char_width, char_height, text_color, bg_color)
        video.write(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))

    # Завершаем запись видео
    video.release()
    print(f"Видео успешно сохранено: {output_file}")


def parse_color(color_str):
    """Парсит цвет из строки в формате R,G,B"""
    try:
        r, g, b = map(int, color_str.split(','))
        return (r, g, b)
    except:
        return (0, 0, 0)  # Черный по умолчанию


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Конвертер ASCII-анимации в MP4 видео')
    parser.add_argument('input', help='Входной файл с ASCII анимацией')
    parser.add_argument('output', help='Выходной MP4 файл')
    parser.add_argument('--fps', type=int, default=10, help='Кадров в секунду (по умолчанию: 10)')
    parser.add_argument('--font_size', type=int, default=10, help='Размер шрифта (по умолчанию: 10)')
    parser.add_argument('--text_color', type=str, default='255,255,255',
                        help='Цвет текста в формате R,G,B (по умолчанию: 255,255,255 - белый)')
    parser.add_argument('--bg_color', type=str, default='0,0,0',
                        help='Цвет фона в формате R,G,B (по умолчанию: 0,0,0 - черный)')

    args = parser.parse_args()

    # Преобразуем цвета
    text_color = parse_color(args.text_color)
    bg_color = parse_color(args.bg_color)

    ascii_to_video(
        input_file=args.input,
        output_file=args.output,
        fps=args.fps,
        font_size=args.font_size,
        text_color=text_color,
        bg_color=bg_color
    )
