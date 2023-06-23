import sys
import glob
import os
from os import path
from convert_data import convert_data






def read_data(patient_folder, save_path):
    """
        Read the relevant data from the specific patient folder
        For now it's only the mesh and car file

    Args:
        patient_folder (str): Name of Patient Folder in the given directory.
                            (CARTO 3D specific export)
        save_path (str): Path where the converted data will be stored
    """
    
    
    
    
    

    
    previous_dir = os.getcwd()    # Store working directory for later use
    os.chdir(patient_folder)

    # Check if "Study 1" folder exists and open it
    dir_content = os.listdir()
    if len(dir_content) == 0:
        print("\nWARNING: The folder  ", patient_folder, "  is empty.")
        sys.exit("\t Please check the exported patient data file.")

    for i in range(len(dir_content)):
        if dir_content[i] == 'Study 1':
            os.chdir(dir_content[i])
            break
        elif i == len(dir_content) - 1:
            print("\nWARNING: No folder 'Study 1' found in\n\t   ", patient_folder)
            sys.exit("\t Please check the exported patient data file.")
    

    # Open mesurement folder, which should be the only folder in this directory

    # check and error warning if there are more then one folders or none
    dir_path = os.getcwd()
    subs = glob.glob(dir_path + "/*/")
    len_subs = len(subs)
    if len_subs == 0:
        print("\nWARNING: No 'Export_Study..' folder found for\n\t   ", \
            patient_folder)
        sys.exit("\t Please check the exported patient data file.")

    elif len_subs > 1:
        print("\nWARNING: More than one folder found under 'Study 1' for\n\t   ", \
            patient_folder)
        print("\nPlease select one of the %i following folders and type in the number: " \
               %len_subs)

        trunc_subs = [ sub.replace(dir_path + "\\", '') for sub in subs]
        [print(sub) for sub in trunc_subs]

        # If the input is not correct, repeat request
        which_folder = 0
        try:
            which_folder = int(input())
        except ValueError:
            print("\nNo valid integer input")

        while which_folder==0 or which_folder> len_subs:
            print("\nNo valid input number, try again: ")
            try:
                which_folder = int(input())
            except ValueError:
                print("\nNo valid integer input, try again: ")
        #jump to given folder        
        os.chdir(subs[which_folder-1])

    else:
        dir_content = os.listdir()
        for i in range(len(dir_content)):
            if path.isdir(dir_content[i]) == 1:
                os.chdir(dir_content[i])
                break


    # Check number of mesh and car files and do not proceed when they differ
    dir_content = os.listdir()
    number_of_mesh = len([i for i in dir_content if 'mesh' in i])
    number_of_car = len([i for i in dir_content if 'car' in i])
    if number_of_mesh != number_of_car:
        print("\nERROR:  Different number of mesh and car files for\n\t  ", \
              patient_folder)
        sys.exit("\tPlease check the exported patient data file.")


    # Search the desired .mesh files and covert the data
    mesh_count = 0
    for i in range(len(dir_content)):
        if 'mesh' in dir_content[i]:
            mesh_count += 1
            convert_data(dir_content[i], 0, save_path, mesh_count)


    # Search the desired .car files and covert the data
    car_count = 0
    for i in range(len(dir_content)):
        if 'car' in dir_content[i]:
            car_count += 1
            convert_data(dir_content[i], 1, save_path, car_count)



    #PREVIOUS VERSION WHERE WE ASKED FOR ONE OF THE MESHES
    {
        # # Ask for the desired mesh_data if there are multiple
        # if number_of_mesh > 1:
        #     print("\nThere are several meshes for the patient \n'%s'\n" \
        #           "Please select one of the %i meshes and type in the number: " \
        #            %(patient_folder, number_of_mesh))

        #     # If the input is not correct, repeat request
        #     which_data = 0
        #     try:
        #         which_data = int(input())
        #     except ValueError:
        #         print("\nNo valid integer input")

        #     while which_data==0 or which_data>number_of_mesh:
        #         print("\nNo valid input number, try again: ")
        #         try:
        #             which_data = int(input())
        #         except ValueError:
        #             print("\nNo valid integer input, try again: ")
        # else:
        #     which_data = 1


        # # Search the desired .mesh files and covert the data
        # mesh_count = 0
        # for i in range(len(dir_content)):
        #     if 'mesh' in dir_content[i]:
        #         mesh_count += 1
        #         if mesh_count == which_data:
        #             convert_data(dir_content[i], 0, save_path)


        # # Search the desired .car files and covert the data
        # car_count = 0
        # for i in range(len(dir_content)):
        #     if 'car' in dir_content[i]:
        #         car_count += 1
        #         if car_count == which_data:
        #             convert_data(dir_content[i], 1, save_path)
    }

    # Go back to previous directory once work is done here
    os.chdir(previous_dir)
