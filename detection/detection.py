import cv2
import numpy as np
from typing import Tuple

def focus_overlay(img: np.array, working_image_size=0.5e6, high_pass_size=7, countours_stop=3) -> np.array:

    #1 image pre-processing
    img_ = resize_image_if_needed(img, expected_pixels=working_image_size)
    img2 = img_.copy()
    img3 = img_.copy()

    # convert to gray scale
    if img2.ndim == 3:
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    #2 high pass filter to find high local contrast areas
    blur = cv2.GaussianBlur(img2, (high_pass_size, high_pass_size), 0)
    high_pass = img2 - blur + 127 * np.ones(img2.shape, np.uint8)

    #cv2.imwrite('hp.jpg', high_pass)

    #3 get a mask
    overlay = mask_from_contours(high_pass)
    #cv2.imwrite('./ov.jpg', overlay)

    #4 median blue averaging to remove small patches
    #a
    # overlay = cv2.medianBlur(overlay, blur_size)
    #b
    # find_optimal_blur_size = False
    # if find_optimal_blur_size:
    #     optimal_blur_size(overlay_sweep)
    #c
    overlay, _ = apply_median_blur_recursively(overlay, stop_when_n_contours=countours_stop)
    #cv2.imwrite('./ov.jpg', overlay)

    # draw overlay
    to_overlay = np.transpose((overlay == 255).nonzero())
    for pair in to_overlay:
        img3[pair[0], pair[1], 2] = (img3[pair[0], pair[1], 2] + 255) / 2.

    return img3

def resize_image_if_needed(img: np.array, expected_pixels=2e6) -> np.array:
    
    # do not upscale, it introduces artefacts
    if img.shape[0] * img.shape[1] > 0.5e6:
        #2M pixels locks down
        #expected_pixels = expected_pixels * 2
        ratio2 = int(expected_pixels) / (img.shape[0] * img.shape[1])
        img_ = cv2.resize(img, (0, 0), fx=np.sqrt(ratio2), fy=np.sqrt(ratio2))
    else:
        img_ = img

    return img_

def optimal_blur_size(mask, max_search=301):
    
    _,ll = apply_median_blur_recursively(mask, max_iter=max_search)

    d2x = -1 * np.diff(np.array([l11[1] for l11 in ll]), n=2)
    d2x = d2x.tolist()
    d2x.insert(0,0)
    d2x.insert(0,0)

    out = [(lx[0], lx[1], d2x[ii]) for ii, lx in enumerate(ll)]

    return out

def apply_median_blur_recursively(img: np.array, max_iter=101, step=2, stop_when_n_contours=2) -> Tuple[np.array, list]:

    res = []
    for ii in range(1, max_iter, step):
        try: 
            img = cv2.medianBlur(img, ii)     # must be odd
            cnt = get_contours(img)
            res.append([ii, len(cnt)])
            print(ii, len(cnt))
        except Exception as e:
            print(f'opencv stops here {e}')
            break
        if len(cnt) <= stop_when_n_contours:
            print(f'limit number of {stop_when_n_contours} contours found')
            break

    print(f'last blur size: {res[-1][0]} found {res[-1][1]} contours')

    return img, res

def get_contours(img: np.array) -> list:
    
    if img.ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresholds = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresholds, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    return contours

def mask_from_contours(img: np.array) -> np.array:
    contours = get_contours(img)
    mask = np.zeros(img.shape, np.uint8)
    cv2.drawContours(mask, contours, -1, (255), -1)

    return mask


    # canny object detector
    #img_ = cv2.Canny(img, 200, 300)
