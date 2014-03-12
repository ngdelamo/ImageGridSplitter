__author__ = 'ngdelamo'

import sys
import os
import argparse

from PIL import Image


def rel_to_abs_path(path):
    return os.path.abspath(os.path.join(os.getcwd(), path))


def img_grid_split():
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
    parser.add_argument('-mw', '--maxwidth', type=int, default=512,
                        help='The max width of the sub-images (defaults to 512px)')
    parser.add_argument('-mh', '--maxheight', type=int, default=512,
                        help='The max height of the sub-images (defaults to 512px)')

    # Parse arguments
    args = parser.parse_args()

    # Process images
    for input_file in args.input_files:
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

        # Ignore images smaller than maxwidth x maxheight
        if image.size[0] < args.maxwidth and image.size[1] < args.maxheight:
            continue

        # Split images
        row = 0
        for y in range(0, image.size[1], step=args.maxheight):
            y_distance_to_end = image.size[1] - y
            height = min(args.maxheight, y_distance_to_end)
            col = 0
            for x in range(0, image.size[0], step=args.maxwidth):
                x_distance_to_end = image.size[0] - x
                width = min(args.maxwidth, x_distance_to_end)

                sub_image = image.crop(x, y, width, height)
                output_file = "{f_name}-{row}-{col}.{ext}".format(f_name=os.path.splitext(input_file)[0], row=row,
                                                                  col=col, ext=os.path.splitext(input_file)[1])
                try:
                    sub_image.save(output_file)
                except IOError:
                    msg = 'Output file "{output_file}" could not be saved'.format(output_file=output_file)
                    print(msg, file=sys.stderr)
                col += 1
            row += 1