import os
from PIL import Image
from contextlib import contextmanager

@contextmanager
def ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        print(f"Directory '{directory_path}' does not exist.")
        return
    yield

def compress_image(input_path, max_width=1000, max_size=256, step=2):
    """Compress an image, keeping its aspect ratio."""
    quality = 90  # Исходное качество сжатия

    with Image.open(input_path) as img:
        # Рассчитываем высоту, чтобы сохранить соотношение сторон
        w, h = img.size
        if w > max_width:
            h = max_width * h // w
            w = max_width

        # Изменение размера изображения
        img = img.resize((w, h), Image.LANCZOS)
        
        if img.mode in ('P', 'RGBA'):
            img = img.convert('RGB')

        # Сохранение изображение с пониженным качеством
        while quality >= step and os.path.getsize(input_path) > max_size * 256:
            img.save(input_path, "JPEG", optimize=True, quality=quality)
            quality -= step
        print(f"Сжатие и сохранение {input_path}")

def compress_images_in_directory(directory_path):
    for root, _, files in os.walk(directory_path):
        for filename in files:
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                input_path = os.path.join(root, filename)
                compress_image(input_path)

if __name__ == "__main__":
    directory_path = input("Укажи путь к каталогу, содержащему изображения: ")
    with ensure_directory_exists(directory_path):
        compress_images_in_directory(directory_path)
