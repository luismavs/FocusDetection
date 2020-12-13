import sys
import argparse
import logging
import pathlib
import json
import cv2

from detection.detection import focus_overlay

def parse_args():
    parser = argparse.ArgumentParser(description='run blur detection on a single image')
    parser.add_argument('-i', '--images', type=str, nargs='+', required=True, help='directory of images')
    parser.add_argument('-s', '--save-path', type=str, default=None, help='path to save output')

    parser.add_argument('-v', '--verbose', action='store_true', help='set logging level to debug')
    parser.add_argument('-d', '--display', action='store_true', help='display images')

    return parser.parse_args()


def find_images(image_paths, img_extensions=['.jpg', '.png', '.jpeg']):
    img_extensions += [i.upper() for i in img_extensions]

    for path in image_paths:
        path = pathlib.Path(path)

        if path.is_file():
            if path.suffix not in img_extensions:
                logging.info(f'{path.suffix} is not an image extension! skipping {path}')
                continue
            else:
                yield path

        if path.is_dir():
            for img_ext in img_extensions:
                yield from path.rglob(f'*{img_ext}')

    return

if __name__ == '__main__':
    assert sys.version_info >= (3, 6), sys.version_info
    args = parse_args()

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level)

    if args.save_path is not None:
        save_path = pathlib.Path(args.save_path)
    else:
        save_path = None

    results = []

    for image_path in find_images(args.images):
        image = cv2.imread(str(image_path))
        if image is None:
            logging.warning(f'warning! failed to read image from {image_path}; skipping!')
            continue

        logging.info(f'processing {image_path}')
        img = focus_overlay(image)

        imname_ = str(image_path).split('/')[-1]
        impath = '/'.join(str(image_path).split('/')[:-1])
        imname = imname_.split('.')[0] + '_focus' + '.' + imname_.split('.')[1]

        if save_path is None:
            cv2.imwrite( str(pathlib.Path(impath) / imname), img)
        else:
            cv2.imwrite( str(save_path / imname), img)

        # if args.display:
        #     cv2.imshow('input', image)

