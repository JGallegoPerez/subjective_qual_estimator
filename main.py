import sqe
import utils


images_main_dir = "images" #This directory must exist and contain all images
preselect_dir = "images/dir" #This directory and its subdirectories are programatically created
copies_dir = "images/subframes_copies" #Where the copies for stacking are saved

def run_application():
    run = True
    preselect_been = False #Has been in preselect phase
    preselect_finished = False #Preselection phase finished
    regular_been = False #Has been in regular phase
    regular_finished = False #Same for regular rating
    superframes_been = False #Has been in superframe phase
    superframes_finished = False #Same for superframe rating

    while run: 
         
        mode = 'm' #mode menu
        while True:
            while mode not in {'b', 'n', 'p', 'c', 'q', 'x'} or mode == 'm':
                mode = input("""  MENU:\n
                    Enter 'b' to begin.
                    Enter 'n' to move to the next stage.
                    Enter 'p' to practice. You will practice with subframes from the current evaluation group.
                    Enter 'c' to stop practicing and continue.
                    Enter 'q' for quality estimation and copying subframes.
                    Enter 'x' to exit or finish application. The data will be saved if the session has not finished yet. 
                    """)
            
            if mode == 'b':
                session = sqe.Session(images_main_dir)
                images_main = session.main_group
                images_included = session.included
                images_superframes = session.superframes
                present_framegroup = images_main #Varies throughout the session
                
            if mode == 'x':
                run = False
                break
            if mode in {'p', 'c'}:
                mode = 'm'
            
            if preselect_been == True and mode == 'n':
                preselect_finished = True
            if regular_been == True and mode == 'n':
                regular_finished = True
            if superframes_been == True and mode == 'n':
                superframes_finished = True    

            if mode in {'b', 'p'}:
                print("--------------------PRACTICE mode--------------------")
                disp1 = sqe.Display(session, present_framegroup, "practice")
                disp1.run(random_order=True)
                mode = 'm' 

            if not preselect_finished and mode in {'n', 'c'}:                  
                if not preselect_been:
                    disp2 = sqe.Display(session,  present_framegroup, "preselect")
                    print("--------------------PRESELECTION begins--------------------")
                preselect_been = True
                disp2.run(random_order=False) # "random_order=False"-> The display progresses from best to worst subframes  
                mode = 'm' 
                
            if not regular_finished and mode in {'n', 'c'}:
                present_framegroup = images_included
                if not regular_been:
                    disp3 = sqe.Display(session,  present_framegroup, "rating")
                    print("--------------------REGULAR RATING begins--------------------")
                disp3.run(random_order=True) #The display progresses from best to worst subframes  
                regular_been = True
                mode = 'm'    
                
            if not superframes_finished and mode in {'n', 'c'}:
                present_framegroup = images_superframes
                if not superframes_been:
                    disp4 = sqe.Display(session,  present_framegroup, "superframes")
                    print("--------------------SUPERFRAMES RATING begins--------------------")
                disp4.run(random_order=True) #The display progresses from best to worst subframes  
                superframes_been = True
                mode = 'm'   
                
            if mode == 'q':
                #Quality estimation
                utils.qual_estimation(ask_policies=False, copies_stack=True, copy_dir=copies_dir)
                mode = 'm'



if __name__ == "__main__":
    
    run_application()


