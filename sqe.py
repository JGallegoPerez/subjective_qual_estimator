import utils 
import numpy as np
import cv2
import os
import random
import time
import matplotlib.pyplot as plt
import copy
import csv
from tempfile import NamedTemporaryFile
import shutil


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
        input_str = "3,4,5,6"
        self.qual_policy_nonsuper = list(map(int,input_str.strip().split(",")))
        input_str = "8,10,15,30,40"
        self.qual_policy_super = list(map(int,input_str.strip().split(",")))
        #Create CSV file (only with the fields for now)
        #First_rating: -1 indicates rejected, 0 included (not rated yet). 
        self.fields = ['Image_name', 'First_rating', 'Superframe_rating', 'Quality_estimation', 'Stack_weight'] 
        with open("subs_ratings.csv", 'w') as self.csvfile: 
            self.csvwriter = csv.writer(self.csvfile) 
            self.csvwriter.writerow(self.fields) 
            self.csvfile.close()
        self.csv_file = None

    def write_to_csv(self, file_name, input, mode):
        new_row = []
        if mode == 'preselect':
            new_row = [file_name, input, 0, 0, 0]
            with open("subs_ratings.csv", 'a') as self.csvfile: 
                self.csvwriter = csv.writer(self.csvfile) 
                self.csvwriter.writerow(new_row) 
                self.csvfile.close()
        if mode == 'rating':
            csv_name = "subs_ratings.csv"
            tempfile = NamedTemporaryFile(mode='w', delete=False)
            with open(csv_name, 'r') as csvfile, tempfile:
                reader = csv.DictReader(csvfile, fieldnames=self.fields)
                writer = csv.DictWriter(tempfile, fieldnames=self.fields)
                for row in reader:
                    if row['Image_name'] == str(file_name):
                        print('updating row ', row['Image_name'])
                        row['First_rating'], row['Superframe_rating'], row['Quality_estimation'], row['Stack_weight'] = input, 0, 0, 0
                    row = {'Image_name': row['Image_name'], 'First_rating': row['First_rating'], 'Superframe_rating': row['Superframe_rating'], 'Quality_estimation': row['Quality_estimation'], 'Stack_weight': row['Stack_weight']}
                    writer.writerow(row)
            shutil.move(tempfile.name, csv_name)
        if mode == 'superframes':
            csv_name = "subs_ratings.csv"
            tempfile = NamedTemporaryFile(mode='w', delete=False)
            with open(csv_name, 'r') as csvfile, tempfile:
                reader = csv.DictReader(csvfile, fieldnames=self.fields)
                writer = csv.DictWriter(tempfile, fieldnames=self.fields)
                for row in reader:
                    if row['Image_name'] == str(file_name):
                        print('updating row ', row['Image_name'])
                        row['First_rating'], row['Superframe_rating'], row['Quality_estimation'], row['Stack_weight'] = row['First_rating'], input, 0, 0
                    row = {'Image_name': row['Image_name'], 'First_rating': row['First_rating'], 'Superframe_rating': row['Superframe_rating'], 'Quality_estimation': row['Quality_estimation'], 'Stack_weight': row['Stack_weight']}
                    writer.writerow(row)
            shutil.move(tempfile.name, csv_name)


    def show_stats(self):
        csv_path = 'subs_ratings.csv'
        with open(csv_path, 'r') as read_obj:
            csv_reader = csv.reader(read_obj)
            list_of_csv = list(csv_reader)
            print(list_of_csv)
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

        #Calculating equivalent number of subframes stacked
        copies_arr = np.array(count_copies)
        copy_max = np.max(copies_arr)
        subs_equival = np.sum(copies_arr / copy_max)
        print('Equivalent number of stacked subframes: ', subs_equival)

        #Histogram
        data = count_list
        _, _, patches = plt.hist(data, [0,1,2,3,4,5,6], align="left")
        plt.show()




    def end(self):   #############################     ZOMBIE CODE  ################
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

    
    #For now, the quality estimation consists in the number of copies for the stacking
    def qual_estimation(self):
        
        #Iterate through all included subframes
        included_dict = dict(filter( lambda elem: elem[1][0] != 0, self.subs_dict.items()  ))
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
    disp_size = (600, 600) #This does not correspond to the pixel size of the image
    im_delay = 0.25
    #num_subs_practice = 2

    def __init__(self, session, subs_group, disp_type):
        self.session = session
        self.subs_group = subs_group #It's constructed from a Subs_group object
        self.subs_group.im_name_list = sorted(self.subs_group.im_name_list)
        self.disp_type = disp_type #Types: practice, preselect, rating, superframe
        if self.disp_type == "practice":
            self.instructions = f"You will see a series of subframes as practice. Press any key to show the next image.\nPress 'm' to return to menu."
        elif self.disp_type == "preselect":
            self.instructions = "Select a substantial amount of subframes (e.g. 500-1500). Press <,> for rejecting and <.> for selecting.\nPress 'm' to return to menu."
        elif self.disp_type == "rating":
            self.instructions = "Rate each image from 1 (worst quality) to 5 (best quality) by pressing 1-5 number keys on the keyboard."
        elif self.disp_type == "superframes":
            self.instructions = "Rate each image from 1 (worst quality) to 5 (best quality) by pressing 1-5 number keys on the keyboard."
        self.counter_preselec = 0
        self.counter_selected = 0
        self.counter_reg_rating = 0
        self.counter_superframes = 0

    def run(self, random_order=True):  
        
        #Get the list of the names of the images
        im_names = self.subs_group.im_name_list 
        assert len(im_names) > 0, f"len(im_names) is 0" 
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
            counter_practice = 0
            #while counter < len(im_names_practice):
            while True:   
                if counter_practice == len(im_names_practice):
                    counter_practice = 0 #Counter reset to 0 after a whole cycle 
                assert len(im_names_practice) > 0, f"len of im_names_practice is 0"       
                im_name = im_names_practice[counter_practice]
                im_path = os.path.join(self.subs_group.directory, im_name)
                img = cv2.imread(im_path)
                img = cv2.resize(img, self.disp_size)
                img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE) 
                cv2.imshow(im_path, img)
                pressed_key = cv2.waitKey(0) & 0xFF
                #print("key ord: ", pressed_key)
                print(f"{counter_practice + 1} practice subframes shown as practice.")   
                cv2.destroyAllWindows()
                time.sleep(self.im_delay)     
                if pressed_key == ord('m'):
                    cv2.destroyAllWindows()
                    break
                counter_practice += 1
    
        elif self.disp_type == "preselect":
            #counter = 0
            #counter_selected = 0
            while self.counter_preselec < len(im_names): 
                im_name = im_names[self.counter_preselec]
                im_path = os.path.join(self.subs_group.directory, im_name)
                im_path_rejected = os.path.join(self.subs_group.directory + "/rejected/", im_name)
                im_path_preselect = os.path.join(self.subs_group.directory + "/included/", im_name)
                img = cv2.imread(im_path)
                img = cv2.resize(img, self.disp_size)
                img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
                cv2.imshow(im_path, img)
                pressed_key = cv2.waitKey(0) & 0xFF
                cv2.destroyAllWindows()
                time.sleep(self.im_delay)     
                if pressed_key == ord('m'):
                    cv2.destroyAllWindows()
                    break
                elif pressed_key == ord(','):
                    frame_include = False
                    self.session.subs_dict[im_name] = [0, 0, 0] # 0 indicates rejection
                    cv2.imwrite(im_path_rejected, img)
                    self.counter_preselec += 1
                    self.session.write_to_csv(im_name, -1, 'preselect')
                elif pressed_key == ord('.'):
                    frame_include = True
                    self.session.subs_dict[im_name] = None #Frames not evaluated yet
                    self.session.included.im_name_list.append(im_name)
                    cv2.imwrite(im_path_preselect, img)
                    self.counter_preselec += 1
                    self.counter_selected += 1
                    self.session.write_to_csv(im_name, 0, 'preselect')
                else:
                    print("Press <,> for rejection, <.> for preselection, or <m> to return to menu.")
                print(f"{self.counter_preselec} subframes shown. {self.counter_selected} subframes selected.") 

        elif self.disp_type == "rating":
            while self.counter_reg_rating < len(im_names_shuffled): 
                im_name = im_names_shuffled[self.counter_reg_rating]
                im_path_included = os.path.join(self.subs_group.directory, im_name)
                im_path_super = os.path.join(self.subs_group.directory + "/superframes/", im_name)
                img = cv2.imread(im_path_included)
                img = cv2.resize(img, self.disp_size)
                img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
                cv2.imshow(im_path_included, img)
                pressed_key = cv2.waitKey(0) & 0xFF
                print(f"{self.counter_reg_rating + 1} subframes shown for rating.")   
                cv2.destroyAllWindows()
                time.sleep(self.im_delay)     
                if pressed_key == ord('m'):
                    cv2.destroyAllWindows()
                    #print("Application terminated.")
                    break
                elif pressed_key in [ord('1'), ord('2'), ord('3'), ord('4'), ord('5')]:
                    #The 0 below is the superframe score. For now, 0 for all subframes.
                    self.session.subs_dict[im_name] = [int(chr(pressed_key)), 0]
                    self.session.write_to_csv(im_name, int(chr(pressed_key)), 'rating')
                    if pressed_key == ord('5'):
                        self.session.superframes.im_name_list.append(im_name)
                        cv2.imwrite(im_path_super, img)
                    self.counter_reg_rating += 1
                else:
                    print("Press keys 1-5 to rate the images, or <m> to return to menu.")     
                print(f"{self.counter_reg_rating} subframes shown in RATING.")       


        elif self.disp_type == "superframes":
            while self.counter_superframes < len(im_names_shuffled): 
                im_name = im_names_shuffled[self.counter_superframes]
                im_path = os.path.join(self.subs_group.directory, im_name)
                img = cv2.imread(im_path)
                img = cv2.resize(img, self.disp_size)
                img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
                cv2.imshow(im_path, img)
                pressed_key = cv2.waitKey(0) & 0xFF
                print(f"{self.counter_superframes + 1} subframes shown for superframes.")   
                cv2.destroyAllWindows()
                time.sleep(self.im_delay)     
                if pressed_key == ord('m'):
                    cv2.destroyAllWindows()
                    break
                elif pressed_key in [ord('1'), ord('2'), ord('3'), ord('4'), ord('5')]:
                    lst = self.session.subs_dict[im_name]
                    lst[1] = int(chr(pressed_key)) #The second element in subs_dict is the superframe rating
                    self.session.write_to_csv(im_name, int(chr(pressed_key)), 'superframes')
                    self.session.subs_dict[im_name] = lst
                    self.counter_superframes += 1
                else:
                    print("Press keys 1-5 to rate the images, or <m> to return to menu.")     
                print(f"{self.counter_superframes} subframes shown in SUPERFRAMES.")

                        

  








        







































