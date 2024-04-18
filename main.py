import os
from PIL import Image

IMAGE_EXTENSIONS = ['.jpg', '.png', '.jpeg']

# Удаляем изображения с дополнительными размерами в названиях, но сохраняем оригиналы
def delete_images(rootDir):
    all_files = {fname for fname in os.listdir(rootDir) if any(ext in fname for ext in IMAGE_EXTENSIONS)}
    resized_to_original = {}
    
    for fname in all_files:
        if 'x' in fname:
            parts = fname.rsplit('-', 1)
            if len(parts) > 1 and parts[-1].count('x') == 1 and parts[-1].split('x')[0].isdigit() and parts[-1].split('x')[1].split('.')[0].isdigit():
                original_fname = parts[0] + fname[-4:]
                if original_fname in all_files:
                    resized_to_original[fname] = original_fname
    
    for dirName, _, fileList in os.walk(rootDir):
        for fname in fileList:
            if fname in resized_to_original:
                # Если файл представляет собой размер, то удаляем
                try:
                    os.remove(os.path.join(dirName, fname))
                    print(f'Удалено: {fname}')
                except OSError as e:
                    print(f"Error: {e.strerror}")
            else:
                # Если файл не является измененным изображением, не удаляем
                print(f'Сохранилось: {fname}')


def delete_images_size(rootDir):
    for dirName, _, fileList in os.walk(rootDir):
        for fname in fileList:
            if fname.count('x') == 2 and any(ext in fname for ext in IMAGE_EXTENSIONS):
                original_fname = fname.rsplit('_', 1)[0] + fname[-4:]
                if original_fname not in fileList:
                    try:
                        os.remove(os.path.join(dirName, fname))
                        print(f'Удалено: {fname}')
                    except OSError as e:
                        print(f"Error: {e.strerror}")

                    
# Создаем новые изображения с определенными размерами на основе исходного изображения
def create_images(rootDir, dimensions):
    for dirName, subdirList, fileList in os.walk(rootDir):
        for fname in fileList:
            if ('.jpg' in fname or '.png' in fname or '.jpeg' in fname) and fname.count('x') == 0:
                original_image = Image.open(os.path.join(dirName, fname))
                for dimension in dimensions:
                    new_image = original_image.resize(dimension)
                    new_image.save(f'{fname[:-4]}-{dimension[0]}x{dimension[1]}{fname[-4:]}')
                    print(f'Создал: {fname[:-4]}-{dimension[0]}x{dimension[1]}{fname[-4:]}')

def main():
    while True:
        rootDir = input("Введи путь: ")
        
        while True:
            print("1. Удалить изображения")
            print("2. Удалить изображения с двумя размерами")
            print("3. Создать изображения")
            print("4. Выход")
            choice = input("Введи число: ")

            if choice == '1':
                delete_images(rootDir)
            elif choice == '2':
                 delete_images_size(rootDir)
            elif choice == '3':
                width = int(input("Ширина: "))
                height = int(input("Высота: "))
                create_images(rootDir, [(width, height)])
            elif choice == '4':
                break  
            else:
                print("Введи число от 1 до 4")

        restart = input("Стартанем ещё? (y/no): ")
        if restart.lower() != 'y':
            break 

if __name__ == "__main__":
    main()
