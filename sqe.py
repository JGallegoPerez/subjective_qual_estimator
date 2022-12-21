import utils 
import numpy as np
import cv2
import os
import random
import time
import copy
import csv
from tempfile import NamedTemporaryFile
import shutil


class Session:
    def __init__(self, main_group_dir):
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
        input_str = "0,0,0,0"
        self.qual_policy_nonsuper = list(map(int,input_str.strip().split(",")))
        input_str = "0,0,0,0,0"
        self.qual_policy_super = list(map(int,input_str.strip().split(",")))
        #Create CSV file (only with the fields for now)
        #First_rating: -1 indicates rejected, 0 included (not rated yet). 
        self.fields = ['Image_name', 'First_rating', 'Superframe_rating', 'Quality_estimation', 'Stack_weight'] 
        with open("subs_ratings.csv", 'w') as self.csvfile: 
            self.csvwriter = csv.writer(self.csvfile) 
            self.csvwriter.writerow(self.fields) 
            self.csvfile.close()
        self.csv_file = None


    #To numpy array, with rows: ['Image_name', 'First_rating', 'Superframe_rating', 'Quality_estimation', 'Stack_weight']
    def csv_to_arr(self, csv_path): 
        with open(csv_path, 'r') as read_obj:
            csv_reader = csv.reader(read_obj)
            list_of_csv = list(csv_reader)
        lst = []
        for i in list_of_csv:
            if len(i) > 0 and i is not list_of_csv[0]:
                lst.append(i)
        arr = np.array(lst)
        arr = arr[:,1:].astype('int')
        return arr  #arr is a numpy 2D array

    #Returns the stage in which the last session was saved
    def saved_stage(self, arr): #arr is a numpy 2D array of ints. The first column (names) was excluded.
        stage = ''
        if arr.shape[0] == 0 or np.all(arr[:,0] <= 0):
            stage = 'preselect'
        elif np.any(arr[:,0] > 0) and np.all(arr[:,1] == 0):
            stage = 'rating'
        elif np.any(arr[:,1] != 0):
            stage = 'superframes'
        return stage

    #Updates any entry in the CSV file. "input" is the new rating assigned to a given image. 
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
                        row['First_rating'], row['Superframe_rating'], row['Quality_estimation'], row['Stack_weight'] = row['First_rating'], input, 0, 0
                    row = {'Image_name': row['Image_name'], 'First_rating': row['First_rating'], 'Superframe_rating': row['Superframe_rating'], 'Quality_estimation': row['Quality_estimation'], 'Stack_weight': row['Stack_weight']}
                    writer.writerow(row)
            shutil.move(tempfile.name, csv_name)

        
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
            else:
                im_names_shuffled = copy.deepcopy(im_names)
                random.shuffle(im_names_shuffled)       
        print(self.instructions + "\n")

        if self.disp_type == "practice":
            counter_practice = 0
            while True:   
                if counter_practice == len(im_names_practice):
                    counter_practice = 0 #Counter reset to 0 after a whole cycle 
                assert len(im_names_practice) > 0, f"len of im_names_practice is 0"       
                im_name = im_names_practice[counter_practice]
                im_path = os.path.join(self.subs_group.directory, im_name)
                img = cv2.imread(im_path)
                img = cv2.resize(img, self.disp_size)
                #img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE) 
                cv2.imshow(im_path, img)
                pressed_key = cv2.waitKey(0) & 0xFF
                print(f"<PRACTICE MODE> {counter_practice + 1} subframes shown.")   
                cv2.destroyAllWindows()
                time.sleep(self.im_delay)     
                if pressed_key == ord('m'):
                    cv2.destroyAllWindows()
                    break
                counter_practice += 1
    
        elif self.disp_type == "preselect":
            while self.counter_preselec < len(im_names): 
                im_name = im_names[self.counter_preselec]
                im_path = os.path.join(self.subs_group.directory, im_name)
                im_path_rejected = os.path.join(self.subs_group.directory + "/rejected/", im_name)
                im_path_preselect = os.path.join(self.subs_group.directory + "/included/", im_name)
                img = cv2.imread(im_path)
                img = cv2.resize(img, self.disp_size)
                #img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
                cv2.imshow(im_path, img)
                pressed_key = cv2.waitKey(0) & 0xFF
                cv2.destroyAllWindows()
                time.sleep(self.im_delay)     
                if pressed_key == ord('m'):
                    cv2.destroyAllWindows()
                    break
                elif pressed_key == ord(','):
                    self.session.subs_dict[im_name] = [0, 0, 0] # 0 indicates rejection
                    cv2.imwrite(im_path_rejected, img)
                    self.counter_preselec += 1
                    self.session.write_to_csv(im_name, -1, 'preselect')
                elif pressed_key == ord('.'):
                    self.session.subs_dict[im_name] = None #Frames not evaluated yet
                    self.session.included.im_name_list.append(im_name)
                    cv2.imwrite(im_path_preselect, img)
                    self.counter_preselec += 1
                    self.counter_selected += 1
                    self.session.write_to_csv(im_name, 0, 'preselect')
                else:
                    print("Press <,> for rejection, <.> for preselection, or <m> to return to menu.")
                print(f"<PRESELECTION MODE> {self.counter_preselec} subframes shown. {self.counter_selected} subframes selected.") 

        elif self.disp_type == "rating":
            while self.counter_reg_rating < len(im_names_shuffled): 
                im_name = im_names_shuffled[self.counter_reg_rating]
                im_path_included = os.path.join(self.subs_group.directory, im_name)
                im_path_super = os.path.join(self.subs_group.directory + "/superframes/", im_name)
                img = cv2.imread(im_path_included)
                img = cv2.resize(img, self.disp_size)
                #img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
                cv2.imshow(im_path_included, img)
                pressed_key = cv2.waitKey(0) & 0xFF
                print(f"<REGULAR RATING MODE> {self.counter_reg_rating + 1}/{len(im_names_shuffled)} regular subframes rated.")   
                cv2.destroyAllWindows()
                time.sleep(self.im_delay)     
                if pressed_key == ord('m'):
                    cv2.destroyAllWindows()
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
            if self.counter_reg_rating == len(im_names_shuffled):
                print("--------------------REGULAR RATING finished--------------------")     

        elif self.disp_type == "superframes":
            while self.counter_superframes < len(im_names_shuffled): 
                im_name = im_names_shuffled[self.counter_superframes]
                im_path = os.path.join(self.subs_group.directory, im_name)
                img = cv2.imread(im_path)
                img = cv2.resize(img, self.disp_size)
                #img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
                cv2.imshow(im_path, img)
                pressed_key = cv2.waitKey(0) & 0xFF
                print(f"<SUPERFRAME RATING MODE> {self.counter_superframes + 1}/{len(im_names_shuffled)} superframes rated.")   
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
            if self.counter_superframes == len(im_names_shuffled):
                print("--------------------SUPERFRAMES RATING finished--------------------")

                        
