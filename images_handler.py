import glob
import os
import PIL.JpegImagePlugin
from PIL import Image

class ImagesHandler:
    ImageFile = PIL.JpegImagePlugin.JpegImageFile
    ImageCropped = PIL.Image.Image

    def __init__(self, path_image_directory, BASEWIDTH=800):
        """
        :BASEWIDTH - необходимая ширина картинки, по умолчанию 800px
        :param path_image_directory: 'images/*/*'
        """
        self.path_image_directory = path_image_directory
        self.BASEWIDTH = BASEWIDTH

    # Обработать все изображения из директории
    def process_images(self) -> None:
        paths = self._load_file_paths()
        for path_current_img in paths:
            adapt_directory = self._create_new_adapt_directory(path_current_img)
            self._prepare_img(path_current_img, adapt_directory)

    # Загружаем имена исходных файлов изображений
    def _load_file_paths(self) -> list:
        return glob.glob(self.path_image_directory)

    # Создаем новую директорию для оптимизированных изображений
    def _create_new_adapt_directory(self, path: str) -> str:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        current_directory = path.split('/')
        new_directory = dir_path + '/' + current_directory[0] + '/' + current_directory[1] + '_adapt'

        if not os.path.isdir(new_directory):
            os.mkdir(new_directory)
        return new_directory

    # Обрабатываем изображения
    def _prepare_img(self, path_current_img: str, adapt_directory: str) -> None:
        with Image.open(path_current_img) as img:
            # Если размер изображения больше необходимого, то обрезаем его и сжимаем
            if img.size[0] > self.BASEWIDTH:
                img = self._cut_image(img)
                filename = path_current_img.split('/')[-1]
                self._compress_image(adapt_directory, filename, img)
            else:
                filename = path_current_img.split('/')[-1]
                self._compress_image(adapt_directory, filename, img)

    # Обрезаем изображение с сохранением пропорций
    def _cut_image(self, image: ImageFile) -> ImageCropped:
        wpercent = (self.BASEWIDTH / float(image.size[0]))
        hsize = int((float(image.size[1]) * float(wpercent)))
        return image.resize((self.BASEWIDTH, hsize), Image.Resampling.LANCZOS)

    # Функция сжатия изображения и сохранения в требуемом формате
    def _compress_image(self, adapt_directory: str, filename: str, img: ImageFile) -> None:
        if img.mode != "RGB":
            img = img.convert("RGB")

        filename = filename.split('.')[0]
        adapt_path = adapt_directory + '/' + filename + '.jpeg'
        img.save(adapt_path, "JPEG", optimize=True, quality=80)

        # adapt_path = adapt_directory + '/' + filename + '.webp'
        # img.save(adapt_path, "webp", quality=80, method=6)
