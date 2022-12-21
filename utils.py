
import cv2
import os
import matplotlib.pyplot as plt
import csv
from tempfile import NamedTemporaryFile
import shutil


#Takes a directory (string) and returns a list of the names (strings) of the images in it
def dir_to_im_names(directory):
    file_list = []
    for path in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, path)):
            file_list.append(path)
    return file_list


def qual_estimation(histogram=True, ask_policies=True, copies_stack=True, copy_dir=None):
    assert os.path.isfile("subs_ratings.csv"), """ERROR: There is no subs_ratings.csv file. 
    You must go through one session or copy one in the main directory."""
            
    if ask_policies:
        input_str = input("Enter the copy weights (4) for the regular frames, separated by commas: ")
        pol_nonsuper = list(map(int,input_str.strip().split(",")))
        input_str = input("Enter the copy weights (5) for the superframes, separated by commas: ")
        pol_super = list(map(int,input_str.strip().split(",")))
    else:
        pol_nonsuper = [2,3,3,4]
        pol_super = [5,6,7,8,9]
    
    #Update Quality_estimation in the CSV file
    csv_name = "subs_ratings.csv"
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    equiv_subs = 0 #To calculate the equivalent number of subframes stacked
    sum_copies = 0 #To calculate the stack weight of each subframe
    rejected = 0 #Rejected frames
    regular = 0 #Regular frames
    superframes = 0
    orig_subs_stack = 0 #To count total of original stacked images
    first_ratings_lst = []
    superframes_lst = []

    fields = []
    with open(csv_name, 'r') as csvfile:
        reader_temp = csv.DictReader(csvfile)
        fields = reader_temp.fieldnames #Get the field names
        csvfile.close()

    with open(csv_name, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)
        num_copies_set = set()
        for row in reader:
            if row.get('First_rating') != 'First_rating': #We skip the fields
                regular_rating = int(row.get('First_rating'))
                first_ratings_lst.append(regular_rating)
                num_copies = 0
                superframes_rating = int(row.get('Superframe_rating'))
                superframes_lst.append(superframes_rating)
                if regular_rating == -1:
                    rejected += 1
                elif regular_rating < 5 and regular_rating != -1:
                    num_copies = pol_nonsuper[regular_rating-1]
                    num_copies_set.add(num_copies)
                    regular += 1
                    orig_subs_stack += 1
                elif regular_rating == 5:
                    num_copies = pol_super[superframes_rating-1]
                    num_copies_set.add(num_copies)
                    superframes += 1
                    orig_subs_stack += 1
                row['Quality_estimation'], row['Stack_weight'] = num_copies, 0
                sum_copies += num_copies #For Stack_weight later
            row = {'Image_name': row['Image_name'], 'First_rating': row['First_rating'], 'Superframe_rating': row['Superframe_rating'], 'Quality_estimation': row['Quality_estimation'], 'Stack_weight': row['Stack_weight']}
            writer.writerow(row)
    shutil.move(tempfile.name, csv_name)
    max_copies = max(num_copies_set)
        
    #Update Stack_weight for each frame. Also, copy images to stack.
    csv_name = "subs_ratings.csv"
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    stacked_lst = [] #For the stacking method
    with open(csv_name, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)
        stack_weights_set = set()
        equiv_subs = 0
        for row in reader:
            if row.get('First_rating') != 'First_rating':
                num_copies = int(row.get('Quality_estimation'))
                row['Stack_weight'] = (num_copies / sum_copies) * 100
                stack_weights_set.add(row['Stack_weight'])
                #Estimate equivalent number of frames:
                equiv_subs +=  (num_copies / max_copies)
                #Copy images for stack
                if copies_stack and copy_dir != None:
                    img_name = row['Image_name']
                    img_name_no_tif = img_name.split(".tif")[0]
                    img = cv2.imread("images/" + img_name) #The name is the same as the path, because img is in the main directory
                    for i in range(num_copies):
                        stack_img_path = copy_dir + "/" + img_name_no_tif + "_copy_" + str(i) + ".tif"
                        stacked_lst.append(stack_img_path) #For the stacking method
                        cv2.imwrite(stack_img_path, img)
            row = {'Image_name': row['Image_name'], 'First_rating': row['First_rating'], 'Superframe_rating': row['Superframe_rating'], 'Quality_estimation': row['Quality_estimation'], 'Stack_weight': row['Stack_weight']}
            writer.writerow(row)
    shutil.move(tempfile.name, csv_name)
    max_stack_weights = max(stack_weights_set)
    print("\n-----------------SESSION INFO-----------------")
    print("Total subframes viewed: ", (rejected + orig_subs_stack))
    print(" -Rejected: ", rejected)
    print(" -Included: ", orig_subs_stack)
    print("   -regular subframes: ", regular)
    print("   -superframes: ", superframes)
    print("Total copies: ", sum_copies)
    print("Equivalent original subframes: {:0.2f} (out of {})".format(equiv_subs, orig_subs_stack))
    print(" -Highest stack weight: \n", max_stack_weights)
    
    if histogram:
        #Histogram for all frames
        _, _, patches = plt.hist(first_ratings_lst, [1,2,3,4,5,6], label="all subframes", align="left")
        #Histogram for superframes
        _, _, patches = plt.hist(superframes_lst, [1,2,3,4,5,6], label="only superframes", align="left")
        plt.legend()
        plt.title("RATINGS DISTRIBUTION")
        plt.ylabel("Count")
        plt.xlabel("Rating")
        plt.show()  
    



