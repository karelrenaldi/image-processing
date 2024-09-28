from PIL import Image
from typing import Tuple
from math import sin, cos, pi, radians

class ImageProcessing:
    def __init__(self, image_source: str):
        self.image_source = image_source

        self.rgb_image = Image.open(self.image_source)
        self.rgb_image_data = self.rgb_image.load()

        self.grayscale_image = Image.open(self.image_source).convert('L')
        self.grayscale_image_data = self.grayscale_image.load()

    def binary_image(self, threshold: int) -> Image.Image:
        new_image = Image.new("L", (self.grayscale_image.width, self.grayscale_image.height))
        new_image_data = new_image.load()

        for i in range(new_image.width):
            for j in range(new_image.height):
                if self.grayscale_image_data[i, j] < threshold:
                    new_image_data[i, j] = 0
                else:
                    new_image_data[i, j] = 255

        return new_image

    def negative_image(self) -> Image.Image:
        new_image = Image.new('RGB', (self.rgb_image.width, self.rgb_image.height))
        new_image_data = new_image.load()

        for i in range(new_image.width):
            for j in range(new_image.height):
                r, g, b = self.rgb_image_data[i, j][:3]

                new_r = 255 - r
                new_g = 255 - g
                new_b = 255 - b

                new_image_data[i, j] = (new_r, new_g, new_b)

        return new_image

    def clipping_value(self, value):
        return max(0, min(255, value))
    
    def is_out_of_index(self, x_value: int, y_value: int, x_min: int, y_min: int, x_max: int, y_max: int):
        return x_value >= x_max or x_value < x_min or y_value >= y_max or y_value < y_min

    def brightening_image(self, brightening_value: int) -> Image.Image:
        new_image = Image.new('RGB', (self.rgb_image.width, self.rgb_image.height))
        new_image_data = new_image.load()

        for i in range(new_image.width):
            for j in range(new_image.height):
                r, g, b = self.rgb_image_data[i, j][:3]

                new_r = self.clipping_value(r + brightening_value)
                new_g = self.clipping_value(g + brightening_value)
                new_b = self.clipping_value(b + brightening_value)

                new_image_data[i, j] = (new_r, new_g, new_b)

        return new_image
    
    def translate_image(self, x_offset: int, y_offset: int) -> Image.Image:
        new_image = Image.new('RGB', (self.rgb_image.width, self.rgb_image.height))
        new_image_data = new_image.load()

        x_start = x_offset if x_offset > 0 else 0
        y_start = y_offset if y_offset > 0 else 0

        for i in range(x_start, new_image.width):
            for j in range(y_start, new_image.height):
                i_new = i - x_offset
                j_new = j - y_offset

                if(self.is_out_of_index(i, j, 0, 0, new_image.width, new_image.height)):
                    new_image_data[i, j] = (0, 0, 0)
                else:
                    new_image_data[i, j] = self.rgb_image_data[i_new, j_new]

        return new_image
    
    def rotation_image(self, theta: int, rotation_point : Tuple[int, int] | None = None):
        new_image = Image.new('RGB', (self.rgb_image.width, self.rgb_image.height))
        new_image_data = new_image.load()

        theta_rad = radians(theta)
        sin_theta = sin(theta_rad)
        cos_theta = cos(theta_rad)

        pivot_point = (new_image.width // 2, new_image.height // 2) if rotation_point == None else rotation_point

        for i in range(0, new_image.width):
            for j in range(0, new_image.height):
                i_new = int(cos_theta * (i - pivot_point[0]) - sin_theta * (j - pivot_point[1]) + pivot_point[0])
                j_new = int(sin_theta * (i - pivot_point[0]) + cos_theta * (j - pivot_point[1]) + pivot_point[1])

                if(self.is_out_of_index(i_new, j_new, 0, 0, new_image.width, new_image.height)):
                    new_image_data[i, j] = (0, 0, 0)
                else:
                    new_image_data[i, j] = self.rgb_image_data[i_new, j_new]
        
        return new_image


if __name__ == "__main__":
    processor = ImageProcessing("assets/lena-512px.bmp")

    binary_image = processor.binary_image(threshold=128)
    binary_image.save("output/lena-512px-binary.bmp")
    binary_image.close()

    negative_image = processor.negative_image()
    negative_image.save("output/lena-512px-negative.bmp")
    negative_image.close()

    brightening_image1 = processor.brightening_image(120)
    brightening_image1.save("output/lena-512px-add-brightness-120.bmp")
    brightening_image1.close()

    brightening_image2 = processor.brightening_image(-120)
    brightening_image2.save("output/lena-512px-add-darkness-120.bmp")
    brightening_image2.close()

    translation_image = processor.translate_image(30, -30)
    translation_image.save("output/lena-512px-translate.bmp")
    translation_image.close()

    rotation_image = processor.rotation_image(70)
    rotation_image.show()
