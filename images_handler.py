from PIL import Image
import os
import glob

# Устанавливаем требуемую максимальную ширину изображения
BASEWIDTH = 800

# Загружаем имена исходных файлов изображений
def get_files():
    return glob.glob("images/*/*")

# Создаем новую директорию для оптимизированных изображений
def create_new_adapt_directory(path):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    current_directory = path.split('/')
    new_directory = dir_path + '/' + current_directory[0] + '/' + current_directory[1] + '_adapt'

    if not os.path.isdir(new_directory):
        os.mkdir(new_directory)
    return new_directory

# Обрезаем изображение с сохранением пропорций
def cut_image(image):
    wpercent = (BASEWIDTH / float(image.size[0]))
    hsize = int((float(image.size[1]) * float(wpercent)))
    return image.resize((BASEWIDTH, hsize), Image.Resampling.LANCZOS)

# Основная функция обработки изображения
def prepare_img(path_current_img, adapt_directory):
    with Image.open(path_current_img) as img:
        # Если размер изображения больше необходимого, то обрезаем его и сжимаем
        if img.size[0] > BASEWIDTH:
            img = cut_image(img)
            filename = path_current_img.split('/')[-1]
            compress_image(adapt_directory, filename, img)
        else:
            filename = path_current_img.split('/')[-1]
            compress_image(adapt_directory, filename, img)

# Функция сжатия изображения и сохранения в требуемом формате
def compress_image(adapt_directory, filename, img):
        if img.mode != "RGB":
            img = img.convert("RGB")
        filename = filename.split('.')[0]

        adapt_path = adapt_directory + '/' + filename + '.jpeg'
        img.save(adapt_path, "JPEG", optimize=True, quality=80)

        # adapt_path = adapt_directory + '/' + filename + '.webp'
        # img.save(adapt_path, "webp", quality=80, method=6)

def main():
    paths = get_files()
    for path_current_img in paths:
        adapt_directory = create_new_adapt_directory(path_current_img)
        prepare_img(path_current_img, adapt_directory)

if __name__ == '__main__':
    main()