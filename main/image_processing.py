from PIL import Image, ExifTags
import numpy as np


class TransformImage:
    def __init__(self, image_path):
        self.orientation_rotation_mapping = {'2': [self.flip], '3': [self.rotate_180],
                                             '4': [self.flip, self.rotate_180],
                                             '5': [self.flip, self.rotate_cw], '6': [self.rotate_cw],
                                             '7': [self.flip, self.rotate_ccw], '8': [self.rotate_ccw]}
        self.image_path = image_path
        self.image_in = Image.open(image_path)
        self.image_in_array = self.load_image_as_array(image_path)
        self.orientation = self.get_orientation()
        self.image_out = None
        self.image_out_path = ''

        self.target_resolution = (0, 0)
        self.logo_banner_resolution = (0, 0)
        self.new_image_width = 0
        self.set_target_resolution(self.target_resolution)

    def set_target_resolution(self, value):
        self.target_resolution = (value[0], value[1])
        self.new_image_width = self.target_resolution[0] * 0.75

    def set_banner_resolution(self, value):
        self.logo_banner_resolution = (value[0], value[1])

    def get_orientation(self):
        exif = {ExifTags.TAGS[k]: v for k, v in self.image_in.getexif().items() if k in ExifTags.TAGS}
        return exif.get('Orientation', None)

    def rotate(self):
        if not self.orientation or self.orientation == '1':
            return False
        for func in self.orientation_rotation_mapping[str(self.orientation)]:
            self.image_in_array = func(self.image_in_array)
        self.save_image_from_array()

    @staticmethod
    def load_image_as_array(image_path):
        return np.asarray(Image.open(image_path))

    def save_image_from_array(self):
        self.image_out = Image.fromarray(self.image_in_array)
        self.image_out.save("main/static/top_bar_image.jpg")
        self.image_out_path = "main/static/top_bar_image.jpg"

    @staticmethod
    def flip(image):
        return np.fliplr(image)

    @staticmethod
    def rotate_cw(image):
        return np.rot90(image, -1)

    @staticmethod
    def rotate_ccw(image):
        return np.rot90(image)

    @staticmethod
    def rotate_180(image):
        return np.rot90(image, 2)

    def resize_top_image(self, image):
        blank_image = Image.new('RGB', (int(self.new_image_width), self.logo_banner_resolution[1]))
        new_image = Image.new('RGB', (int(self.new_image_width), self.logo_banner_resolution[1]))
        center_x = (self.new_image_width / 2) - (self.logo_banner_resolution[0] / 2)
        new_image.paste(image.convert('RGB'), (int(center_x), 0))
        new_image.save('main/static/resized_logo.jpg')
        return blank_image

    def resize(self):
        w, h = self.image_out.size
        new_height = h / w * self.new_image_width
        new_image = self.image_out.resize((int(self.new_image_width), int(new_height)))
        self.image_out = new_image
        new_image.save("main/static/top_bar_image.jpg")

    def make_top_bar(self):
        image_top = self.resize_top_image(Image.open("main/static/logo-white-black-background.jpg"))
        image_bottom = Image.open(self.image_out_path)
        self.logo_banner_resolution = (image_top.size[0], image_top.size[1])
        total_height = image_bottom.size[1] + image_top.size[1]
        new_image = Image.new('RGB', (int(self.new_image_width), total_height), (250, 250, 250))
        new_image.paste(image_top, (0, 0))
        new_image.paste(image_bottom, (0, image_top.size[1]))
        new_image.save("main/static/top_bar_image.jpg")
        self.image_out = new_image
