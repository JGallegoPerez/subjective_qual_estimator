import utils 
import numpy as np
import cv2
import os
import random
import time
import matplotlib.pyplot as plt
import copy


class Session:
    def __init__(self, main_group_dir):
        #The most important data structure. This dictionary contains the names of all images as keys, and the values are: pressed key, estimated quality and stacking weight.
        #The dictionary has entries added as the application progresses, so that it can be accessed anytime. 
        
        self.new_session = True 
        self.subs_dict = {}
        self.main_group = Subframe_group(main_group_dir) #An object from Subframe_group will be assigned
        self.rejected = Subframe_group(self.main_group.directory + "/" + "rejected")
        self.rejected.empty_dir()
        self.included = Subframe_group(self.main_group.directory + "/" + "included")
        self.included.empty_dir()
        self.superframes = Subframe_group(self.main_group.directory + "/" + "included" + "/" + "superframes")
        self.superframes.empty_dir()





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
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.directory = directory
        #self.im_list = None
        self.im_name_list = utils.dir_to_im_names(self.directory)
        self.stack = None

    def empty_dir(self):
        self.im_name_list = ""
        dir = os.listdir(self.directory)
        if len(dir) == 0:
            print(self.directory + " was empty.")
        else:
            for f in os.listdir(self.directory):
                if os.path.isfile(os.path.join(self.directory, f)):
                    os.remove(os.path.join(self.directory, f))









class Display:

    disp_size = (1000, 1000) #This does not correspond to the pixel size of the image
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
        print("random_order: ", random_order)
        im_names = self.subs_group.im_name_list
        print(im_names[:3])
        if random_order:
            if self.disp_type == "practice":
                im_names_practice = copy.deepcopy(im_names)
                im_names_practice = random.choices(im_names_practice, k=self.num_subs_practice)
            else:
                im_names_shuffled = copy.deepcopy(im_names)
                random.shuffle(im_names_shuffled)       

        print(self.instructions + "\n")

        if self.disp_type == "practice":
            counter = 0
            while counter < self.num_subs_practice:
                
                im_name = im_names_practice[counter]
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
            while counter < 5: #test
                im_name = im_names[counter]
                im_path = os.path.join(self.subs_group.directory, im_name)
                im_path_rejected = os.path.join(self.subs_group.directory + "/rejected/", im_name)
                im_path_preselect = os.path.join(self.subs_group.directory + "/included/", im_name)
                img = cv2.imread(im_path)
                img = cv2.resize(img, self.disp_size)
                cv2.imshow(im_path, img)
                pressed_key = cv2.waitKey(0) & 0xFF
                print(f"{counter + 1} subframes shown.")   
                cv2.destroyAllWindows()
                time.sleep(self.im_delay)     
                
                if pressed_key == ord('q'):
                    cv2.destroyAllWindows()
                    print("Application terminated.")
                    break
                elif pressed_key == ord(','):
                    frame_include = False
                    self.session.subs_dict[im_name] = [0] # 0 indicates rejection
                    cv2.imwrite(im_path_rejected, img)
                    counter += 1
                elif pressed_key == ord('.'):
                    frame_include = True
                    self.session.subs_dict[im_name] = None #Frames not evaluated yet
                    cv2.imwrite(im_path_preselect, img)
                    counter += 1
                else:
                    print("Press <,> for rejection, <.> for preselection, or <q> to quit.")


        # elif self.disp_type == "rating":
        #     counter = 0
        #     while counter < 5: #test
        #         im_name = im_names[counter]
        #         im_path = os.path.join(self.subs_group.directory, im_name)
        #         im_path_rejected = os.path.join(self.subs_group.directory + "/rejected/", im_name)
        #         im_path_preselect = os.path.join(self.subs_group.directory + "/included/", im_name)
        #         img = cv2.imread(im_path)
        #         img = cv2.resize(img, self.disp_size)
        #         cv2.imshow(im_path, img)
        #         pressed_key = cv2.waitKey(0) & 0xFF
        #         print(f"{counter + 1} subframes shown.")   
        #         cv2.destroyAllWindows()
        #         time.sleep(self.im_delay)     
                
        #         if pressed_key == ord('q'):
        #             cv2.destroyAllWindows()
        #             print("Application terminated.")
        #             break
        #         elif pressed_key == ord(','):
        #             frame_include = False
        #             self.session.subs_dict[im_name] = [0] # 0 indicates rejection
        #             cv2.imwrite(im_path_rejected, img)
        #             counter += 1
        #         elif pressed_key == ord('.'):
        #             frame_include = True
        #             self.session.subs_dict[im_name] = None #Frames not evaluated yet
        #             cv2.imwrite(im_path_preselect, img)
        #             counter += 1
        #         else:
        #             print("Press <,> for rejection, <.> for preselection, or <q> to quit.")                




                        










        











































