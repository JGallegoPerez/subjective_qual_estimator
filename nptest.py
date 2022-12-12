import numpy as np
import cv2
import os
import random
import time
import matplotlib.pyplot as plt
import copy
import csv
from matplotlib.image import imread
from PIL import Image
import csv

csv_path = 'subs_ratings.csv'

with open(csv_path, 'r') as read_obj:
    csv_reader = csv.reader(read_obj)
    list_of_csv = list(csv_reader)

in_path = ''
out_path = ''
num_copies = 0

count_list = []
count_copies = []
for i in list_of_csv:
    if len(i) > 0 and i is not list_of_csv[0]:
        im_name = i[0]
        im_name_notif = im_name.split(".tif")[0] 
        in_path = os.path.join('images/', im_name)
        count_list.append(int(i[1]))
        count_copies.append(int(i[3]))

                    #####################Histogram fixed##########################################
                    # data = count_list
                    # _, _, patches = plt.hist(data, [0,1,2,3,4,5,6], align="left")
                    # plt.show()
                    ##############################################################################

                    #Calculating equivalent number of subframes stacked
                    #print("count_copies: ", count_copies[:10])
                    # copies_arr = np.array(count_copies)
                    # copy_max = np.max(copies_arr)

                    # subs_equival = np.sum(copies_arr / copy_max)
                    # print('subs_equival: ', subs_equival)
        im = cv2.imread(in_path)
        
        #num_copies = int(i[3])
        if int(i[1]) == -1: #We dont want weird negative numbers...
            num_copies = 0
        else:
            num_copies = 5 + int(i[1]) + int(i[2])      #new "formula"
        # if num_copies == 40:
        #     num_copies = 60
        # elif num_copies == 30:
        #     num_copies = 40
        # elif num_copies == 15:
        #     num_copies = 20
        # elif num_copies == 10:
        #     num_copies = 15
        # elif num_copies == 8:
        #     num_copies = 10
        # elif num_copies == 6:
        #     num_copies = 10
            
        for n in range(num_copies):
            out_path = 'images/copies_fixed/' + im_name_notif + "_copy_" + str(n) + ".tif"

            cv2.imwrite(out_path, im)
            #print('inside for')
            #print("im shape: ", im.shape)
        # if int(i[1]) != 0:
        #     out_path = 'images/copies_fixed2/' + im_name_notif + ".tif"
        #     cv2.imwrite(out_path, im)
#print(list_of_csv)

csv_arr = np.array(list_of_csv)

print("csv_arr shape: ", csv_arr.shape)






# im_path1 = "images/subframes_copies/00001_2022-11-19-1852_7-T-RGB-Mars_f03713_copy_0.tif"
# im_path2 = "images/subframes_copies/00001_2022-11-19-1852_7-T-RGB-Mars_f03713_copy_0.tif"
# im_path3 = "images/subframes_copies/00001_2022-11-19-1852_7-T-RGB-Mars_f03713_copy_0.tif"
# im_path4 = "images/subframes_copies/00001_2022-11-19-1852_7-T-RGB-Mars_f03713_copy_0.tif"


# #read the images
# img1 = cv2.imread(im_path1)
# img2 = cv2.imread(im_path2)
# img3 = cv2.imread(im_path3)

# file_list = []
# for f in os.listdir("images/subframes_copies/tests"):
#     if os.path.isfile(os.path.join("images/subframes_copies/tests", f)):
#         file_list.append("images/subframes_copies/tests/" + f)

#tests########
# print(file_list[0])
# test = cv2.imread(file_list[0])
# cv2.imshow("test", test)
# pressed_key = cv2.waitKey(0) & 0xFF

#add(or blend) the images
#result = cv2.addWeighted(img1, 0.3, img2, 0.7, 0)

# w1 = 0.5 #Most of the weight
# w2 = 0.5
# stacked_im = cv2.imread(file_list[0]) #stacked_im is initialized with the first image
# new_to_stack = cv2.imread(file_list[0]) #same
# for i in range(len(file_list)):
    
#     w1 = (i+1)/(i+2)
#     w2 = 1 - w1
#     #print(f"w1: {w1}, w2: {w2}")
#     new_to_stack = cv2.imread(file_list[i]) #same
#     stacked_im = cv2.addWeighted(stacked_im, w1, new_to_stack, w2, 0)
    
# cv2.imshow("stacked_im", stacked_im)
# pressed_key = cv2.waitKey(0) & 0xFF     
    
# cv2.imwrite("images/subframes_copies/tests/stacked_im/stacked_im.tif", stacked_im)





