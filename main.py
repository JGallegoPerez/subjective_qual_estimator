

import sqe




images_main_dir = "images" #This directory must exist and contain all images
preselect_dir = "images/dir" #This directory and its subdirectories are programatically created





#Show random images from the images directory 


images_main = sqe.Subframe_group(images_main_dir)
disp = sqe.Display(images_main, "practice")
disp.run()


#print(images_main.im_name_list)

















