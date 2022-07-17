import sys
import numpy as np
import cv2
import time
import os
import threading
import pytesseract
import imutils
from picamera import PiCamera
import skimage.filters as filters




def image_enhancement(img):
    # Rescale the image, if needed.
    # fx scale factor along the horizontal axis = 1.5
    # fy scale factor along the vertical axis= 1.5
    img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)

    # Converting to gray scale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Removing Shadows
    # r,g.b split in list
    rgb_planes = cv2.split(img)
    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
        # removing salt and pepper by median filter
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        result_planes.append(diff_img)

    # merging the r g b plains again in one image
    img = cv2.merge(result_planes)
    cv2.imwrite("1_dialation_and_medianblur.jpg", img)

    # applying closing (dilation then erosion) to close small holes
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)  # increases the white region in the image
    img = cv2.erode(img, kernel, iterations=1)  # erodes away the boundaries of foreground object
    cv2.imwrite("2_after_closing.jpg", img)
    # blur
    blurred_dilation = cv2.GaussianBlur(img, (91, 91), 0)
    cv2.imwrite("3_after_gaussian_blur.jpg", blurred_dilation)
    # divide gray by morphology image
    division = cv2.divide(img, blurred_dilation, scale=255)
    cv2.imwrite("4_after_dividing_gray.jpg", division)
    # sharpening
    sharp = filters.unsharp_mask(division, radius=11, amount=11, multichannel=False, preserve_range=False)
    sharp = (255 * sharp).clip(0, 255).astype(np.uint8)
    cv2.imwrite("5_after_sharpening.jpg", sharp)

    # Apply threshold to get image with only b&w
    # convert to binary image
    img = cv2.threshold(sharp, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # Save the filtered image in the output directory
    # save_path = os.path.join(output_path, file_name + "filter___" + str('as') + ".png")
    cv2.imwrite("6_thresholded.jpg", img)
    return img



