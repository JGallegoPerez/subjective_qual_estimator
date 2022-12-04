

import sqe




images_main_dir = "images" #This directory must exist and contain all images
preselect_dir = "images/dir" #This directory and its subdirectories are programatically created





#Initiate session
session = sqe.Session(images_main_dir)
images_main = sqe.Subframe_group(images_main_dir)

#Show random images from the images directory as first practice. Then, preselection.
print("START PRACTICE OF PRESELECTION.")
disp1 = sqe.Display(session, images_main, "practice")
disp1.run(random_order=True)
print("START PRESELECTION.")
disp2 = sqe.Display(session,  images_main, "preselect")
disp2.run(random_order=False) #The display progresses from best to worst subframes

#Random images to practice on preselected frames. Then, rating.
print("START PRACTICE OF RATING.")
disp3 = sqe.Display(session, session.included, "practice")
disp3.run(random_order=True)
print("START RATING.")
disp4 = sqe.Display(session, session.included, "rating")
disp4.run(random_order=True)

#Random images to practice on superframes. Then, rating superframes
print("START PRACTICE OF RATING SUPERFRAMES.")
disp5 = sqe.Display(session, session.superframes, "practice")
disp5.run(random_order=True)
print("START RATING SUPERFRAMES.")
disp6 = sqe.Display(session, session.superframes, "superframes")
disp6.run(random_order=True)

session.qual_estimation()
session.end()
















