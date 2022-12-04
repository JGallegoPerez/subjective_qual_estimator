

import sqe




images_main_dir = "images" #This directory must exist and contain all images
preselect_dir = "images/dir" #This directory and its subdirectories are programatically created




#Show random images from the images directory 

session = sqe.Session(images_main_dir)

images_main = sqe.Subframe_group(images_main_dir)
disp1 = sqe.Display(session, images_main, "practice")
disp1.run()
disp2 = sqe.Display(session,  images_main, "preselect")
disp2.run(random_order=False) #The display progresses from best to worst subframes
disp3 = sqe.Display(session, session.included, "rating")
disp3.run(random_order=True)
disp4 = sqe.Display(session, session.superframes, "superframes")
disp4.run(random_order=True)
session.qual_estimation()
session.end()
















