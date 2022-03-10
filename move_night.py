

import os
import glob #for loading images from a directory
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import cv2
import numpy as np
import logging

logging.getLogger().setLevel(logging.DEBUG)

IM_PATH_IN="/media/data1/tmp/snapshot/all-2021/*.jpg"
IM_PATH_OUT="/media/data1/tmp/snapshot/all-2021/night"

HUE_THREHOLD = 1

def avg_hue(rgb_image):
    # Convert image to HSV
    hsv = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2HSV)

    # Add up all the pixel values in the V channel
    sum_brightness = np.sum(hsv[:,:,2])
    sum_sat = np.sum(hsv[:,:,1])
    sum_hue = np.sum(hsv[:,:,0])

    area = rgb_image.shape[0]* rgb_image.shape[1]
    
    # find the avg
    avg = sum_hue/area
    logging.info("sum_brightness: %d, sum_sat: %d, sum_hue: %d", sum_brightness/area, sum_sat/area, sum_hue/area)
    
    return avg


for file in glob.glob(IM_PATH_IN):
    logging.info("File: %s", file)
    
    # Read in the image
    im = mpimg.imread(file)
    
    # Check if the image exists/if it's been correctly read-in
    if im is not None:
        hue = avg_hue(im)
        logging.info("avg_hue: %d", hue)
        if hue < HUE_THREHOLD:
            # move to the night folder
            file_name = os.path.basename(file)
            logging.info("Move file: %s", file_name)
            os.rename(file, os.path.join(IM_PATH_OUT, file_name))
