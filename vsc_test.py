
import numpy as np
import cv2
import os
import random
import time
import matplotlib.pyplot as plt

gui_active = True
main_dir = "images"
preselec_dir = "images/preselected"
rated_dir = "images/preselected/rated"
super_rated_dir = "images/preselected/rated/super_rated"
results_dir = "images/results"
num_preselect = 300
im_key_dict = {} #keys: image name; values: lists with 4 or 5 entries (keyboard rating, number of copies, 'regular'/'super', quality)
csv_dict = {} #keys: image name; values: rating ("fake" 6-10 for superframes)


#State subjective definition of image quality
qual_def = "PLANET MUST HAVE GOOD SHAPE. AND IT MUST BE SHARP. 'q' to quit."
#qual_def = input("State your subjective definition of image quality: ")

print(qual_def)


def show_image(im_path):
    preselect = False
    keep_showing = True
    # read a colour image from the working directory
    img = cv2.imread(im_path)
    img = cv2.resize(img,(400,400))
    
    # display the original image #
    cv2.imshow(im_path, img)
    key = cv2.waitKey(0) & 0xFF
    #print("key is ", key)
    # Read from keyboard
    if key == ord('q'):
        #print("key is ", str(key))  
        keep_showing = False  
        cv2.destroyAllWindows()
    if key ==  ord(','):
        #print("Key is: < (reject frame)")    
        preselect = False
    elif key ==  ord('.'):
        #print("Key is: > (include frame)")  
        preselect = True
    #print("key is ", key)
    cv2.destroyAllWindows()
    time.sleep(0.5)
    return preselect, keep_showing, key




#mode: "random", "preselect", "im_rating", "super_im_rating"
def run_gui(mode):
    global gui_active
    global im_key_dict
    global csv_dict
    global main_dir
    global preselec_dir
    global rated_dir
    global super_rated_dir
    global results_dir
    copy_policy = [1,1,2,4,8]
    super_copy_policy = [1,1,2,3,5] #To add (multiply) on top of what had already been copied
    counter = 0

    #Make directories and subdirectories
    try:
        rated_dir = str(rated_dir)
        os.makedirs(rated_dir)
        print("rating_dir: " + rated_dir)
        super_rated_dir = str(super_rated_dir)
        os.makedirs(super_rated_dir)
        print("super_rating_dir: " + super_rated_dir)
    except FileExistsError:
        print("File already exists")

    file_list = []
    for path in os.listdir(main_dir):
        if os.path.isfile(os.path.join(main_dir, path)):
            #file_list.append(input_path + "/" + path)
            file_list.append(path)

    if mode == "random":
        print("Mode: practice")
        random_list = random.choices(file_list, k=20)
        while(gui_active):
            img = cv2.imread(main_dir + "/" + random_list[counter])
            selec, keep_showing, _ = show_image(main_dir + "/" + random_list[counter])
            if keep_showing == False:
                break
            print(str(counter+1) + " frames shown.")
            counter += 1
            if counter >= len(random_list):
                gui_active = False
        #cv2.destroyAllWindows()
    gui_active = True
    
    if mode == "preselect":
        print("Mode: preselection")
        #First, randomize all elements in list 
        random.shuffle(file_list)
        #Copy files into another folder
        preselect_counter = 0
        while(gui_active):
            img = cv2.imread(main_dir + "/" + file_list[counter])
            selec, keep_showing, _ = show_image(main_dir + "/" + file_list[counter])
            #cv2.destroyAllWindows()

            if keep_showing == False:
                break
            if selec:
                cv2.imwrite(preselec_dir + "/" + file_list[counter], img)
                preselect_counter += 1
                #+cv2.destroyAllWindows()
            else:
                csv_dict[file_list[counter]] = 0
            print(str(counter+1) + " frames shown.")
            counter += 1
            if counter >= len(file_list) or preselect_counter >= num_preselect:
                gui_active = False
    gui_active = True


    if mode == "im_rating":
        print("Mode: image rating (scores 1-5)")
        #The new list to draw images from is in "preselected" folder
        selec_list = []
        for path in os.listdir(preselec_dir):
            if os.path.isfile(os.path.join(preselec_dir, path)):
                #file_list.append(input_path + "/" + path)
                selec_list.append(path)
        #Randomize all elements in this list 
        random.shuffle(selec_list)

        im_key_dict = dict.fromkeys(selec_list)
        while(gui_active):
            img = cv2.imread(preselec_dir + "/" + selec_list[counter])
            _ , keep_showing , key = show_image(preselec_dir + "/" + selec_list[counter])
            if keep_showing == False:
                break
            #Assign the corresponding pressed key to each image, in a dictionary
            im_key_dict[selec_list[counter]] = [int(key - 48)]
            csv_dict[selec_list[counter]] = int(key - 48)
            print(str(counter+1) + "/" + str(len(selec_list)) + " frames shown.")
            counter += 1
            if counter >= len(selec_list):
               gui_active = False
        #qual_function(im_key_dict, "simple_copies") 
        copy_saver(im_key_dict, preselec_dir, rated_dir, copy_policy)
    gui_active = True



    if mode == "super_rating":
        print("Mode: super frames rating (scores 1-5)")
        #The new list to draw images from is in "rated" folder
        selec_list = []
        for path in os.listdir(rated_dir):
            if os.path.isfile(os.path.join(rated_dir, path)):
                selec_list.append(path)
        #Randomize all elements in this list 
        random.shuffle(selec_list)

        im_key_dict = dict.fromkeys(selec_list)
        while(gui_active):
            img = cv2.imread(rated_dir + "/" + selec_list[counter])
            _ , keep_showing , key = show_image(rated_dir + "/" + selec_list[counter])
            if keep_showing == False:
                break
            #Assign the corresponding pressed key to each image, in a dictionary
            im_key_dict[selec_list[counter]] = [int(key - 48)]
            csv_dict[selec_list[counter]] = int(key - 43)
            print(str(counter+1) + "/" + str(len(selec_list)) + " frames shown.")
            counter += 1
            if counter >= len(selec_list):
               gui_active = False
        #qual_function(im_key_dict, "simple_copies") 
        copy_saver(im_key_dict, rated_dir, rated_dir, super_copy_policy, super_frames=True)
    gui_active = True


    
    if mode == "random":
        print("\nPractice finished.")   
        time.sleep(2)

    if mode == "preselect":
        print("\nPreselection finished. " + str(preselect_counter) + " subframes included.")  
        time.sleep(1)

    if mode == "im_rating":
        print("\nRating finished.")
        #qual_function(im_key_dict, "simple_mul")  


def qual_function(file_dict, mode, super_frame=False):
    
    if mode == "simple_copies":
        print("Quality function: keyboard input")
        #Adds quality estimation inside the dictionary
        for i in range(len(list(file_dict))):
            val = list(file_dict.values())[i]
            if super_frame:
                val[0] += 5 #(The user never pressed values beyond 5; but here, for superframes, 1-5 keys will appear as 6-10)
            val.append(val[0])

    #Plot a histogram of the data as inputted so far
    vals = np.array(list(file_dict.values())).flatten()
    # Creating histogram
    fig, ax = plt.subplots(figsize =(10, 7))
    ax.hist(vals, bins = [1,2,3,4,5,6,7,8,9,10,11])
 
    # Show plot
    plt.show()


    #Returns a dictionary of the files with their corresponding quality measure
    return 0




#Takes the output of qual_function and makes copies accordingly in the specified directory. Also, CSV file with ratings. 
def copy_saver(file_dict, input_dir, output_dir, copy_policy, super_frames=False): #copy_policy is a list containing the factors by which, correspondingly, the amounts of frames in each bin are multiplied and copied
    for i in range(len(list(file_dict))):
        im = list(file_dict)[i]
        val = list(file_dict.values())[i]
        n_copies = copy_policy[int(val[0] - 1)]
        val.append(n_copies)              
        #Copy the files into output_dir
        for i in range(n_copies):
            # if not super_frames:
            #     ending_str = "_copy_" + str(i)
            # else:
            #     ending_str = "_super_" + str(i)
            img = cv2.imread(input_dir + "/" + im)
            # print("ending_string: ", ending_str)
            # im = im.split('.tif')[0]
            # print("im: ", im)
            # cv2.imwrite(output_dir + "/" + im + ending_str + ".tif", img)
            cv2.imwrite(output_dir + "/" + im + str(i) + ".tif", img)
            
    



start_time = time.time()
######## PRELIMINARY SELECTION OF FRAMES ###########

run_gui("random")
cv2.destroyAllWindows()
time.sleep(1)
run_gui("preselect")
cv2.destroyAllWindows()
time.sleep(2)

######## FIRST RATING ##############################

run_gui("im_rating")
cv2.destroyAllWindows()
time.sleep(1)

# ######## SUPER FRAMES RATING #######################
# run_gui("super_rating")
# cv2.destroyAllWindows()
# time.sleep(1)


qual_function(im_key_dict, "simple_copies", super_frame=False) 

elapsed_time = time.time() - start_time
print('Execution time:', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))

#rint("im_key_dict: ", im_key_dict)
for key in csv_dict:
    print(key, ' : ', csv_dict[key])




