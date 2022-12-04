import utils 
import numpy as np
import cv2
import os
import random
import time
import matplotlib.pyplot as plt
import copy
import csv


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
        self.subframes_copies = Subframe_group(self.main_group.directory + "/" + "subframes_copies")
        self.subframes_copies.empty_dir()        
        #input_str = input("Enter the copy policy for non-superframes (4 values), as values separated by commas: ")
        input_str = "3,4,5,6"
        self.qual_policy_nonsuper = list(map(int,input_str.strip().split(",")))
        #input_str = input("Enter the copy policy for superframes (5 values), as values separated by commas: ")
        input_str = "8,10,15,30,40"
        self.qual_policy_super = list(map(int,input_str.strip().split(",")))
        self.csv_file = None
    
    #For now, the quality estimation consists in the number of copies for the stacking
    def qual_estimation(self):
        
        #Iterate through all included subframes
        included_dict = dict(filter( lambda elem: elem[1][0] != 0, self.subs_dict.items()  ))
        #print("\nincluded_dict: ", included_dict)
        num_copies = 0
        count_copies = 0 #To later calculate the stack weights of each subframe
        for i in included_dict.items():
            if i[1][1] == 0: #if the subframe is non-super
                num_copies =  self.qual_policy_nonsuper[(i[1][0]) - 1]
                # lst = self.subs_dict[i[0]]
                # lst.append(num_copies)
                # self.subs_dict[i[0]] = lst
            else: #if the subframe is super
                num_copies =  self.qual_policy_super[(i[1][1]) - 1]
            lst = self.subs_dict[i[0]]
            lst.append(num_copies)
            self.subs_dict[i[0]] = lst   
            count_copies += num_copies  
        #Stack weights
        for i in self.subs_dict.items():
            val_lst = i[1] #Value part of subs_dict (a list)
            thisframe_copies = val_lst[2] 
            val_lst.append(thisframe_copies / count_copies * 100) #In percentage                 

                
        #print("\nself.subs_dict: ", self.subs_dict)
        

    
    def end(self):
        # #Show histogram, statistics
        
        # #Create CSV file, inside main_group_dir
        # #For now, quality_estimation equals number of copies made for stacking
        fields = ['Image_name', 'First_rating', 'Superframe_rating', 'Quality_estimation', 'Stack_weight'] 
        rows = []
        for i in self.subs_dict.items():
            new_row = copy.deepcopy(i[1])   #List part of the dictionary (thus, no key)
            new_row.insert(0, i[0])
            rows.append(new_row)    
        filename = "subframes_rating.csv"
        with open(filename, 'w') as csvfile: 
            csvwriter = csv.writer(csvfile) 
            csvwriter.writerow(fields) 
            csvwriter.writerows(rows)

        #Make copies for stacking
        for i in self.subs_dict.items():
            #print("self.subs_dict.items(): ", self.subs_dict.items())
            #print("data array: ", i[1])
            num_copies = i[1][2]
            im_name = i[0]
            im_path_included = os.path.join(self.included.directory, im_name)
            img = cv2.imread(im_path_included)
            im_name_notif = i[0].split(".tif")[0]    
            for n in range(num_copies):
                cv2.imwrite(self.subframes_copies.directory + "/" + im_name_notif + "_copy_" + str(n) + ".tif", img)
                    
        
        
        
    def stack(self):
        pass
        # i_dir = self.included.directory
        
        # for i in range(len(self.included.im_name_list)):
        #     i_path = os.path.join(i_dir, self.included.im_name_list[i])
        #     image = cv2.imread(i_path,1).astype(np.float32) / 255
        #     if i == 0:
        #         stacked_image = image
        #     else:
        #         stacked_image += image
        #         stacked_image /= len(self.included.im_name_list)
        #         stacked_image = (stacked_image*255).astype(np.uint8)
        
        # cv2.imshow("Stacked", stacked_image)

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
        self.im_name_list = []
        dir = os.listdir(self.directory)
        if len(dir) == 0:
            print(self.directory + " was empty.")
        else:
            for f in os.listdir(self.directory):
                if os.path.isfile(os.path.join(self.directory, f)):
                    os.remove(os.path.join(self.directory, f))



class Display:
    disp_size = (500, 500) #This does not correspond to the pixel size of the image
    im_delay = 0.25
    #num_subs_practice = 2

    def __init__(self, session, subs_group, disp_type):
        self.session = session
        self.subs_group = subs_group #It's constructed from a Subs_group object
        self.subs_group.im_name_list = sorted(self.subs_group.im_name_list)
        self.disp_type = disp_type #Types: practice, preselect, rating, superframe
        if self.disp_type == "practice":
            self.instructions = f"You will see a series of subframes as practice. Press any key to show the next image.\nPress <q> to move on to PRESELECTION."
        elif self.disp_type == "preselect":
            #self.session = session
            self.instructions = "Select a substantial amount of subframes (e.g. 500-1500). Press <,> for rejecting and <.> for selecting.\nPress <q> to move on to RATING."
        elif self.disp_type == "rating":
            #self.session = session
            self.instructions = "Rate each image from 1 (worst quality) to 5 (best quality) by pressing 1-5 number keys on the keyboard."
        elif self.disp_type == "superframes":
            #self.session = session
            self.instructions = "Rate each image from 1 (worst quality) to 5 (best quality) by pressing 1-5 number keys on the keyboard."


    def run(self, random_order=True):
        #Get the list of the names of the images
        im_names = self.subs_group.im_name_list 
        if random_order:
            if self.disp_type == "practice":
                im_names_practice = copy.deepcopy(im_names)
                random.shuffle(im_names_practice)
                #im_names_practice = random.choices(im_names_practice, k=self.num_subs_practice)
            else:
                im_names_shuffled = copy.deepcopy(im_names)
                random.shuffle(im_names_shuffled)       
        print(self.instructions + "\n")

        if self.disp_type == "practice":
            counter = 0
            #while counter < len(im_names_practice):
            while True:   
                if counter == len(im_names_practice):
                    counter = 0 #Counter reset to 0 after a whole cycle             
                im_name = im_names_practice[counter]
                im_path = os.path.join(self.subs_group.directory, im_name)
                img = cv2.imread(im_path)
                img = cv2.resize(img, self.disp_size)
                cv2.imshow(im_path, img)
                pressed_key = cv2.waitKey(0) & 0xFF
                #print("key ord: ", pressed_key)
                print(f"{counter + 1} practice subframes shown as practice.")   
                cv2.destroyAllWindows()
                time.sleep(self.im_delay)     
                if pressed_key == ord('q'):
                    cv2.destroyAllWindows()
                    print("Practice terminated.")
                    break
                counter += 1
    
        elif self.disp_type == "preselect":
            counter = 0
            counter_selected = 0
            while counter < len(im_names): 
                im_name = im_names[counter]
                im_path = os.path.join(self.subs_group.directory, im_name)
                im_path_rejected = os.path.join(self.subs_group.directory + "/rejected/", im_name)
                im_path_preselect = os.path.join(self.subs_group.directory + "/included/", im_name)
                img = cv2.imread(im_path)
                img = cv2.resize(img, self.disp_size)
                cv2.imshow(im_path, img)
                pressed_key = cv2.waitKey(0) & 0xFF
                cv2.destroyAllWindows()
                time.sleep(self.im_delay)     
                if pressed_key == ord('q'):
                    cv2.destroyAllWindows()
                    print("Application terminated.")
                    break
                elif pressed_key == ord(','):
                    frame_include = False
                    self.session.subs_dict[im_name] = [0, 0, 0] # 0 indicates rejection
                    cv2.imwrite(im_path_rejected, img)
                    counter += 1
                elif pressed_key == ord('.'):
                    frame_include = True
                    self.session.subs_dict[im_name] = None #Frames not evaluated yet
                    self.session.included.im_name_list.append(im_name)
                    cv2.imwrite(im_path_preselect, img)
                    counter += 1
                    counter_selected += 1
                else:
                    print("Press <,> for rejection, <.> for preselection, or <q> to quit.")
                print(f"{counter} subframes shown. {counter_selected} subframes selected.") 

        elif self.disp_type == "rating":
            print("in rating")
            counter = 0
            while counter < len(im_names_shuffled): 
                im_name = im_names_shuffled[counter]
                im_path_included = os.path.join(self.subs_group.directory, im_name)
                im_path_super = os.path.join(self.subs_group.directory + "/superframes/", im_name)
                img = cv2.imread(im_path_included)
                img = cv2.resize(img, self.disp_size)
                cv2.imshow(im_path_included, img)
                pressed_key = cv2.waitKey(0) & 0xFF
                print(f"{counter + 1} subframes shown for rating.")   
                cv2.destroyAllWindows()
                time.sleep(self.im_delay)     
                if pressed_key == ord('q'):
                    cv2.destroyAllWindows()
                    #print("Application terminated.")
                    break
                elif pressed_key in [ord('1'), ord('2'), ord('3'), ord('4'), ord('5')]:
                    #The 0 below is the superframe score. For now, 0 for all subframes.
                    self.session.subs_dict[im_name] = [int(chr(pressed_key)), 0]
                    if pressed_key == ord('5'):
                        self.session.superframes.im_name_list.append(im_name)
                        cv2.imwrite(im_path_super, img)
                    counter += 1
                else:
                    print("Press keys 1-5 to rate the images, or <q> to quit.")     
                print(f"{counter} subframes shown in RATING.")       


        elif self.disp_type == "superframes":
            print("in superframes")
            counter = 0
            while counter < len(im_names_shuffled): 
                im_name = im_names_shuffled[counter]
                im_path = os.path.join(self.subs_group.directory, im_name)
                img = cv2.imread(im_path)
                img = cv2.resize(img, self.disp_size)
                cv2.imshow(im_path, img)
                pressed_key = cv2.waitKey(0) & 0xFF
                print(f"{counter + 1} subframes shown for superframes.")   
                cv2.destroyAllWindows()
                time.sleep(self.im_delay)     
                if pressed_key == ord('q'):
                    cv2.destroyAllWindows()
                    print("Application terminated.")
                    break
                elif pressed_key in [ord('1'), ord('2'), ord('3'), ord('4'), ord('5')]:
                    lst = self.session.subs_dict[im_name]
                    lst[1] = int(chr(pressed_key)) #The second element in subs_dict is the superframe rating
                    self.session.subs_dict[im_name] = lst
                    counter += 1
                else:
                    print("Press keys 1-5 to rate the images, or <q> to quit.")     
                print(f"{counter} subframes shown in SUPERFRAMES.")

                        










        









































