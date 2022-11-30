

import sqe




images_main_dir = "images" #This directory must exist and contain all images
preselect_dir = "images/dir" #This directory and its subdirectories are programatically created




#Show random images from the images directory 

session = sqe.Session(images_main_dir)
images_main = sqe.Subframe_group(images_main_dir)
disp1 = sqe.Display(session, images_main, "practice")
disp1.run()
disp2 = sqe.Display(session,  images_main, "preselect")
disp2.run(random_order=False)


print(session.subs_dict)

#print(images_main.im_name_list)

















