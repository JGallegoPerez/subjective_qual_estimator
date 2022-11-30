import numpy as np
import cv2
import os
import random
import time
import matplotlib.pyplot as plt

#Takes a directory (string) and returns a list of the names (strings) of the images in it
def dir_to_im_names(directory):

    file_list = []
    for path in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, path)):
            file_list.append(path)
        # else:
        #     print("0 images in ", directory)

    return file_list





















