import utils 
import numpy as np
import cv2
import os
import random
import time
import matplotlib.pyplot as plt


class Session:
    def __init__(self):
        #The most important data structure. This dictionary contains the names of all images as keys, and the values are: pressed key, estimated quality and stacking weight.
        #The dictionary has entries added as the application progresses, so that it can be accessed anytime. 
        self.subs_dict = {}



class Subframe:

    def __init__(self, im, name, directory):
        self.im = im
        self.name = name
        self.directory = directory 
        self.path = "" #From directory and name
        self.pressed_key = 0 #Key pressed from keyboard  
        self.est_qual = 0 #Estimated quality
        self.frame_type = "before_eval" #Types: before_eval, discarded, preselected, regular, super






class Subframe_group:

    def __init__(self, directory):
        self.directory = directory
        #self.im_list = None
        self.im_name_list = utils.dir_to_im_names(self.directory)
        self.stack = None

    







class Display:

    disp_size = (400, 400) #This does not correspond to the pixel size of the image
    im_delay = 0.25
    num_subs_practice = 2

    def __init__(self, session, subs_group, disp_type):
        self.session = session
        self.subs_group = subs_group 
        self.disp_type = disp_type #Types: practice, preselect, rating
        if self.disp_type == "practice":
            self.instructions = f"You will see a series of subframes ({self.num_subs_practice}) as practice. Press any key to show the next image."
        elif self.disp_type == "preselect":
            #self.session = session
            self.instructions = "Reject or select each image. Press <,> for rejecting and <.> for selecting."
        elif self.disp_type == "rating":
            #self.session = session
            self.instructions = "Rate each image from 1 (worst quality) to 5 (best quality) by pressing 1-5 number keys on the keyboard."
        


    def run(self, random_order=True):
        #Get the list of the names of the images
        im_names = self.subs_group.im_name_list
        if random_order:
            if self.disp_type == "practice":
                im_names = random.choices(im_names, k=self.num_subs_practice)
            else:
                random.shuffle(im_names)

        print(self.instructions + "\n")

        if self.disp_type == "practice":
            counter = 0
            while counter < self.num_subs_practice:
                
                im_name = im_names[counter]
                im_path = os.path.join(self.subs_group.directory, im_name)
                img = cv2.imread(im_path)
                img = cv2.resize(img, self.disp_size)
                cv2.imshow(im_path, img)
                pressed_key = cv2.waitKey(0) & 0xFF
                print(f"{counter + 1}/{self.num_subs_practice} practice subframes shown")   
                cv2.destroyAllWindows()
                time.sleep(self.im_delay)     
                
                if pressed_key == ord('q'):
                    cv2.destroyAllWindows()
                    print("Application terminated")
                    break

                counter += 1


        elif self.disp_type == "preselect":
            counter = 0
            frame_include = False
            while counter < 5: #test
                im_name = im_names[counter]
                im_path = os.path.join(self.subs_group.directory, im_name)
                img = cv2.imread(im_path)
                img = cv2.resize(img, self.disp_size)
                cv2.imshow(im_path, img)
                pressed_key = cv2.waitKey(0) & 0xFF
                print(f"{counter + 1} subframes shown")   
                cv2.destroyAllWindows()
                time.sleep(self.im_delay)     
                
                if pressed_key == ord('q'):
                    cv2.destroyAllWindows()
                    print("Application terminated")
                    break
                elif pressed_key == ord(','):
                    frame_include = False
                    self.session.subs_dict[im_name] = [0]



                counter += 1




                        










        











































