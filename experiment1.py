# -*- coding: utf-8 -*-
# Copyright (c) 2023 by Phuc Phan

import timeit
from PIL import Image
from datetime import datetime
from multiprocessing import Pool


def get_most_popular_color(image_path: str) -> tuple:
    """ Loads the path to an image and returns most prevalent color as a tuple:
        (the image_path, rgb-color, % of pixels with this color)
        NOTICE: This is unoptimized code: this is used as an example for demonstrating multiprocessing
        :type image_path: object
    """

    # 1. Load the image and pixels
    img = Image.open(image_path)
    pixels = img.load()

    # 2. Image details
    img_width, img_height = img.size  # Get the width and hight of the image for iterating over
    image_pixel_count = img_width * img_height

    # 3. Loop over all pixels, round the pixels and count them in a dict)
    rgb_count_dict: {tuple, int} = {}
    for x in range(img_width):
        for y in range(img_height):
            r, g, b = pixels[x, y]
            r = 10 * round(r/10)
            g = 10 * round(g/10)
            b = 10 * round(b/10)
            rgb = (r, g, b)
            if rgb not in rgb_count_dict.keys():
                rgb_count_dict[rgb] = 0
            rgb_count_dict[rgb] += 1

    # 4. Sort the rgb_count_dict by the count
    sorted_rgb_count_dict = {k: v for k, v in sorted(rgb_count_dict.items(), key=lambda item: item[1], reverse=True)}
    most_popular_rgb = next(iter(sorted_rgb_count_dict))
    most_popular_rgb_pixelcount = rgb_count_dict.pop(most_popular_rgb)
    cover = round(most_popular_rgb_pixelcount / image_pixel_count * 100, 2)

    # print(f"The most popular color in {image_path}\t{most_popular_rgb} covers {cover}%")

    return image_path, most_popular_rgb, cover


if __name__ == '__main__':

    image_paths = [
        'data/puppy-1.jpeg',
        'data/puppy-2.jpeg',
        'data/puppy-3.jpeg',
        'data/puppy-4.jpeg',
        'data/puppy-5.jpeg',
        'data/puppy-6.jpeg',
        'data/puppy-7.jpeg',
        'data/puppy-8.jpeg',
        'data/puppy-9.jpeg',
        'data/puppy-10.png'
    ]

    image_paths = [*image_paths, *image_paths]

    # TODO: Running consecutively
    # start = datetime.now()
    #
    # for img_path in image_paths:
    #     img_path, rgb, percentage = get_most_popular_color(image_path=img_path)
    #     print(f"The most popular color in {img_path}\t{rgb} covers {percentage}%")
    #
    # print('\nTime: ', datetime.now() - start)

    # TODO: Using map
    # start = datetime.now()
    #
    # results = map(get_most_popular_color, image_paths)
    # for img_path, rgb, percentage in list(results):
    #     print(f"The most popular color in {img_path}\t{rgb} covers {percentage}%")
    #
    # print('\nTime: ', datetime.now() - start)

    # TODO: Multiprocessing: Map
    start = datetime.now()
    with Pool() as mp_pool:
        results = mp_pool.map(get_most_popular_color, image_paths)
        for img_path, rgb, percentage in results:
            print(f"The most popular color in {img_path}\t{rgb} covers {percentage}%")

    print('\nTime: ', datetime.now() - start)

