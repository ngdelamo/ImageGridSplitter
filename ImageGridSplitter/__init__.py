# ----------------------------------------------------------------------------
# Copyright 2014 Nacho G. del Amo (https://github.com/ngdelamo)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------------

__author__ = 'ngdelamo'

import sys
import os
import argparse

from PIL import Image

DEFAULT_MAX_WIDTH = 512
DEFAULT_MAX_HEIGHT = 512
DEFAULT_MIN_WIDTH = 1024
DEFAULT_MIN_HEIGHT = 1024
DEFAULT_DELETE = False


def rel_to_abs_path(path):
    return os.path.abspath(os.path.join(os.getcwd(), path))


def img_grid_split(input_files, maxwidth=DEFAULT_MAX_WIDTH, maxheight=DEFAULT_MAX_HEIGHT, minwidth=DEFAULT_MIN_WIDTH, minheight=DEFAULT_MIN_HEIGHT, delete=DEFAULT_DELETE):
    # Process images
    for input_file in input_files:
        # Check input file
        input_file = rel_to_abs_path(input_file)
        if not os.path.exists(input_file):
            msg = 'Input file "{input_file}" does not exist'.format(input_file=input_file)
            print(msg, file=sys.stderr)
            continue

        # Try to read the input file as an image
        try:
            image = Image.open(input_file)
        except IOError:
            msg = 'Input file "{input_file}" does not contain a valid image format'.format(input_file=input_file)
            print(msg, file=sys.stderr)
            continue

        # Ignore images smaller than minwidth x minheight
        if image.size[0] < minwidth and image.size[1] < minheight:
            continue

        # Split images
        row = 0
        for bottom in range(0, image.size[1], maxheight):
            bottom = image.size[1] - bottom
            y_distance_to_end = bottom
            top = bottom - min(maxheight, y_distance_to_end)
            col = 0
            for left in range(0, image.size[0], maxwidth):
                x_distance_to_end = image.size[0] - left
                right = left + min(maxwidth, x_distance_to_end)

                box = (left, top, right, bottom)
                sub_image = image.crop(box)
                output_file = "{f_name}-{row}-{col}{ext}".format(f_name=os.path.splitext(input_file)[0], row=row,
                                                                 col=col, ext=os.path.splitext(input_file)[1])
                try:
                    sub_image.save(output_file)
                except IOError:
                    msg = 'Output file "{output_file}" could not be saved'.format(output_file=output_file)
                    print(msg, file=sys.stderr)
                col += 1
            row += 1

        # Remove images
        if delete:
            os.remove(input_file)


def main():
    # Create the argument parser and define accepted arguments
    parser = argparse.ArgumentParser(
        description='Split images bigger than a certain size into a grid of smaller sub-images. Sub-images are named '
                    'as <original_image_name>-<row>-<col>.<ext>, where <row> and <col> start at (0,0) and indicate '
                    'the bottom-left sub-image. For example, a 1024x1024 image named "image.png" would be splitted '
                    'into 4 images of size 512x512, named "image-0-0.png", "image-0-1.png", "image-1-0.png" and '
                    '"image-1-1.png", where "image-0-0.png" is the sub-image at the bottom-left, "image-0-1.png" is '
                    'the sub-image at the bottom-right, "image-1-0.png" is the sub-image at the top-left, '
                    'and "image-1-1.png" is the sub-image at the top-right.')
    parser.add_argument('input_files', nargs='+', help='A list of input image files')
    parser.add_argument('-Mw', '--maxwidth', type=int, default=DEFAULT_MAX_WIDTH,
                        help='The max width of the sub-images (defaults to {default}px)'.format(
                            default=DEFAULT_MAX_WIDTH))
    parser.add_argument('-Mh', '--maxheight', type=int, default=DEFAULT_MAX_HEIGHT,
                        help='The max height of the sub-images (defaults to {default}px)'.format(
                            default=DEFAULT_MAX_HEIGHT))
    parser.add_argument('-mw', '--minwidth', type=int, default=DEFAULT_MIN_WIDTH,
                        help='The min width of the image to split it into sub-images (defaults to {default}px)'.format(
                            default=DEFAULT_MIN_WIDTH))
    parser.add_argument('-mh', '--minheight', type=int, default=DEFAULT_MIN_HEIGHT,
                        help='The min height of the image to split it into sub-images (defaults to {default}px)'.format(
                            default=DEFAULT_MIN_HEIGHT))
    parser.add_argument('-d', '--delete', default=DEFAULT_DELETE, action='store_true',
                        help='Delete the original image once it has been splitted (defaults to {default})'.format(
                            default=DEFAULT_DELETE))

    # Parse arguments
    args = parser.parse_args()

    # Call main function
    img_grid_split(args.input_files, args.maxwidth, args.maxheight, args.minwidth, args.minheight, args.delete)